"""
KuroNeko v1 — 2B Parametre Decoder-Only Transformer

Mimari Ozellikler:
    - 32 katman, hidden dim 2048
    - GQA: 16 attention head, 4 KV head (4:1 group ratio)
    - RoPE positional encoding (base=10000)
    - SwiGLU aktivasyon (gate + silu)
    - Context window: 4096 token
    - Vocab: 64K token
    - Toplam parametre: ~2B

Moduler Tasarim:
    - Her katman (KuroNekoTransformerLayer) bagimsiz modul
    - Expert eklenebilirlik icin Mixture-of-Experts hook noktasi
    - Config sinifi ile tum hiperparametreler merkezi yonetilir

Kullanim:
    >>> from kuroneko_v1 import KuroNekoConfig, KuroNekoModel
    >>> config = KuroNekoConfig()
    >>> model = KuroNekoModel(config)
    >>> print(f"Parametre: {model.num_params / 1e9:.2f}B")

Test:
    >>> import torch
    >>> ids = torch.randint(0, 64000, (2, 128))
    >>> out = model(ids)
    >>> assert out.shape == (2, 128, 64000)
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger("kuroneko.model")


# ---------------------------------------------------------------------------
# Yapilandirma
# ---------------------------------------------------------------------------
@dataclass
class KuroNekoConfig:
    """KuroNeko v1 model yapilandirmasi.

    Tum hiperparametreler bu sinif uzerinden yonetilir.
    Yeni katman veya expert eklemek icin bu sinifi genisletin.

    Attributes:
        vocab_size: Token sozluk boyutu.
        hidden_dim: Gizli katman boyutu (d_model).
        num_layers: Transformer katman sayisi.
        num_heads: Query attention head sayisi.
        num_kv_heads: Key/Value head sayisi (GQA).
        intermediate_size: FFN intermediate boyutu (SwiGLU icin 2x hidden).
        context_length: Maksimum baglam uzunlugu.
        rope_theta: RoPE taban frekansi.
        rms_norm_eps: RMSNorm epsilon degeri.
        dropout: Dropout orani.
        tie_weights: Embedding ve output weight paylasimi.
        num_experts: MoE icin expert sayisi (0 = MoE kapali).
        top_k_experts: MoE icin aktif expert sayisi.
    """

    vocab_size: int = 64_000
    hidden_dim: int = 2048
    num_layers: int = 32
    num_heads: int = 16
    num_kv_heads: int = 4
    intermediate_size: int = 5632
    context_length: int = 4096
    rope_theta: float = 10_000.0
    rms_norm_eps: float = 1e-5
    dropout: float = 0.0
    tie_weights: bool = True
    num_experts: int = 0
    top_k_experts: int = 2

    def __post_init__(self) -> None:
        """Gecerlilik kontrolleri."""
        if self.hidden_dim % self.num_heads != 0:
            raise ValueError(
                f"hidden_dim ({self.hidden_dim}) num_heads ({self.num_heads}) "
                f"ile bolunmeli"
            )
        if self.num_heads % self.num_kv_heads != 0:
            raise ValueError(
                f"num_heads ({self.num_heads}) num_kv_heads ({self.num_kv_heads}) "
                f"ile bolunmeli"
            )
        if self.num_experts > 0 and self.num_experts < self.top_k_experts:
            raise ValueError(
                f"num_experts ({self.num_experts}) >= top_k_experts "
                f"({self.top_k_experts}) olmali"
            )

    @property
    def head_dim(self) -> int:
        """Tek head boyutu."""
        return self.hidden_dim // self.num_heads

    @property
    def groups(self) -> int:
        """GQA grup sayisi."""
        return self.num_heads // self.num_kv_heads


# ---------------------------------------------------------------------------
# RoPE Positional Encoding
# ---------------------------------------------------------------------------
class RoPE(nn.Module):
    """Rotary Positional Encoding (RoPE).

    Query ve key vektorelere pozisyon bilgisi enjekte eder.
    Precompute edilen cos/sin buffer'i ile verimli calisir.

    Args:
        head_dim: Tek attention head boyutu.
        max_len: Maksimum pozisyon sayisi.
        theta: Taban frekansi (default 10000).
    """

    def __init__(self, head_dim: int, max_len: int, theta: float = 10_000.0) -> None:
        super().__init__()
        self.head_dim = head_dim

        # Frekans hesaplama: 1 / (theta^(2i/d))
        inv_freq = 1.0 / (theta ** (torch.arange(0, head_dim, 2).float() / head_dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)

        # Pozisyon indeksleri
        positions = torch.arange(max_len, dtype=torch.float)
        self.register_buffer("positions", positions, persistent=False)

        # Cos/sin buffer precompute
        self._cos_cache: Optional[torch.Tensor] = None
        self._sin_cache: Optional[torch.Tensor] = None
        self._build_cache(max_len)

    def _build_cache(self, seq_len: int) -> None:
        """Cos/sin cache olustur.

        Args:
            seq_len: Cache'lenecek maksimum uzunluk.
        """
        t = self.positions[:seq_len]
        freqs = torch.outer(t, self.inv_freq)  # (seq_len, head_dim/2)
        emb = torch.cat([freqs, freqs], dim=-1)  # (seq_len, head_dim)
        self._cos_cache = emb.cos().unsqueeze(0).unsqueeze(0)
        self._sin_cache = emb.sin().unsqueeze(0).unsqueeze(0)

    def _ensure_cache(self, seq_len: int) -> None:
        """Cache yetersizse yeniden olustur.

        Args:
            seq_len: Istenen uzunluk.
        """
        if self._cos_cache is None or self._cos_cache.shape[-2] < seq_len:
            self._build_cache(seq_len)

    @staticmethod
    def _rotate_half(x: torch.Tensor) -> torch.Tensor:
        """Vektörün yarısını döndür.

        Args:
            x: (..., d) tensor.

        Returns:
            (..., d) döndürülmüş tensor.
        """
        d = x.shape[-1] // 2
        return torch.cat([-x[..., d:], x[..., :d]], dim=-1)

    def forward(
        self, q: torch.Tensor, k: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """RoPE uygula.

        Args:
            q: (batch, heads, seq_len, head_dim) query tensor.
            k: (batch, kv_heads, seq_len, head_dim) key tensor.

        Returns:
            (q_rotated, k_rotated) RoPE uygulanmış tensorler.
        """
        seq_len = q.shape[2]
        self._ensure_cache(seq_len)

        cos = self._cos_cache[:, :, :seq_len, :].to(q.device)
        sin = self._sin_cache[:, :, :seq_len, :].to(q.device)

        q_rot = q * cos + self._rotate_half(q) * sin
        k_rot = k * cos + self._rotate_half(k) * sin

        return q_rot, k_rot


# ---------------------------------------------------------------------------
# Grouped-Query Attention (GQA)
# ---------------------------------------------------------------------------
class GroupedQueryAttention(nn.Module):
    """Grouped-Query Attention modulu.

    GQA: Her KV head, birden fazla Q head'e hizmet eder.
    Bellek tasarrufu saglar, inference hizini artirir.

    Args:
        config: KuroNekoConfig.
        rope: Paylasimli RoPE modulu.
    """

    def __init__(self, config: KuroNekoConfig, rope: RoPE) -> None:
        super().__init__()
        self.config = config
        self.rope = rope
        self.num_heads = config.num_heads
        self.num_kv_heads = config.num_kv_heads
        self.head_dim = config.head_dim
        self.groups = config.groups

        # Projeksiyon katmanlari
        self.wq = nn.Linear(config.hidden_dim, config.num_heads * config.head_dim, bias=False)
        self.wk = nn.Linear(config.hidden_dim, config.num_kv_heads * config.head_dim, bias=False)
        self.wv = nn.Linear(config.hidden_dim, config.num_kv_heads * config.head_dim, bias=False)
        self.wo = nn.Linear(config.num_heads * config.head_dim, config.hidden_dim, bias=False)

        self.dropout = nn.Dropout(config.dropout)

    def _repeat_kv(self, x: torch.Tensor) -> torch.Tensor:
        """KV head'leri Q head sayisina genislet.

        Args:
            x: (batch, kv_heads, seq_len, head_dim)

        Returns:
            (batch, num_heads, seq_len, head_dim)
        """
        if self.groups == 1:
            return x
        return x.unsqueeze(2).expand(-1, -1, self.groups, -1, -1).reshape(
            x.shape[0], self.num_heads, x.shape[2], self.head_dim
        )

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Ileri gecis.

        Args:
            x: (batch, seq_len, hidden_dim) giris.
            mask: (seq_len, seq_len) causal mask (optional).

        Returns:
            (batch, seq_len, hidden_dim) cikis.
        """
        batch, seq_len, _ = x.shape

        q = self.wq(x).view(batch, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.wk(x).view(batch, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.wv(x).view(batch, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)

        # RoPE uygula
        q, k = self.rope(q, k)

        # KV repeat (GQA)
        k = self._repeat_kv(k)
        v = self._repeat_kv(v)

        # Scaled dot-product attention
        scale = 1.0 / math.sqrt(self.head_dim)
        attn = torch.matmul(q, k.transpose(-2, -1)) * scale

        # Causal mask
        if mask is None:
            mask = torch.triu(
                torch.ones(seq_len, seq_len, device=x.device, dtype=torch.bool),
                diagonal=1,
            )
        attn = attn.masked_fill(mask, float("-inf"))

        attn = F.softmax(attn, dim=-1)
        attn = self.dropout(attn)

        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, -1)

        return self.wo(out)


# ---------------------------------------------------------------------------
# SwiGLU Feed-Forward Network
# ---------------------------------------------------------------------------
class SwiGLU(nn.Module):
    """SwiGLU aktivasyonlu FFN.

    Gate mekanizmali: silu(xW1) * (xW2)
    Llama 2 / Mistral / Mistral tarzi modellerde kullanilir.

    Args:
        config: KuroNekoConfig.
    """

    def __init__(self, config: KuroNekoConfig) -> None:
        super().__init__()
        self.w1 = nn.Linear(config.hidden_dim, config.intermediate_size, bias=False)
        self.w2 = nn.Linear(config.intermediate_size, config.hidden_dim, bias=False)
        self.w3 = nn.Linear(config.hidden_dim, config.intermediate_size, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Ileri gecis.

        Args:
            x: (batch, seq_len, hidden_dim)

        Returns:
            (batch, seq_len, hidden_dim)
        """
        gate = F.silu(self.w1(x))
        hidden = self.w3(x)
        return self.dropout(self.w2(gate * hidden))


# ---------------------------------------------------------------------------
# Mixture of Experts (Opsiyonel Hook)
# ---------------------------------------------------------------------------
class MixtureOfExperts(nn.Module):
    """Mixture-of-Experts modulu (opsiyonel).

    config.num_experts > 0 oldugunda aktif olur.
    Top-K routing ile expert secimi yapar.

    Args:
        config: KuroNekoConfig.
    """

    def __init__(self, config: KuroNekoConfig) -> None:
        super().__init__()
        self.num_experts = config.num_experts
        self.top_k = config.top_k_experts
        self.gate = nn.Linear(config.hidden_dim, config.num_experts, bias=False)
        self.experts = nn.ModuleList(
            [SwiGLU(config) for _ in range(config.num_experts)]
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Ileri gecis.

        Args:
            x: (batch, seq_len, hidden_dim)

        Returns:
            (batch, seq_len, hidden_dim)
        """
        batch, seq_len, hidden = x.shape
        gate_logits = self.gate(x)  # (batch, seq_len, num_experts)
        top_k_vals, top_k_idx = torch.topk(gate_logits, self.top_k, dim=-1)
        top_k_weights = F.softmax(top_k_vals, dim=-1)

        out = torch.zeros_like(x)
        for i, expert in enumerate(self.experts):
            # Bu expert'in secildigi pozisyonlar
            mask = (top_k_idx == i).any(dim=-1)  # (batch, seq_len)
            if not mask.any():
                continue
            expert_in = x[mask]
            expert_out = expert(expert_in)
            weight = top_k_weights[mask]
            # Karsilik gelen agirligi bul
            expert_weight = torch.zeros_like(mask, dtype=x.dtype)
            expert_weight[mask] = weight[(top_k_idx[mask] == i)]
            out[mask] += expert_out * expert_weight.unsqueeze(-1)

        return out


# ---------------------------------------------------------------------------
# Tek Transformer Katmani
# ---------------------------------------------------------------------------
class KuroNekoTransformerLayer(nn.Module):
    """Tek Transformer katmani.

    Pre-norm mimari: RMSNorm -> Attention -> Add -> RMSNorm -> FFN -> Add
    MoE hook noktasi ile ileride expert eklenebilir.

    Args:
        config: KuroNekoConfig.
        rope: Paylasimli RoPE modulu.
    """

    def __init__(self, config: KuroNekoConfig, rope: RoPE) -> None:
        super().__init__()
        self.attention_norm = nn.RMSNorm(config.hidden_dim, eps=config.rms_norm_eps)
        self.attention = GroupedQueryAttention(config, rope)
        self.ffn_norm = nn.RMSNorm(config.hidden_dim, eps=config.rms_norm_eps)

        # MoE veya standart FFN
        if config.num_experts > 0:
            self.ffn = MixtureOfExperts(config)
            logger.info(
                "Katman %d: MoE aktif (%d expert, top-%d)",
                config.num_experts,
                config.top_k_experts,
            )
        else:
            self.ffn = SwiGLU(config)

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Ileri gecis.

        Args:
            x: (batch, seq_len, hidden_dim)
            mask: Causal mask (optional).

        Returns:
            (batch, seq_len, hidden_dim)
        """
        # Pre-norm + residual: attention
        h = x + self.attention(self.attention_norm(x), mask)
        # Pre-norm + residual: FFN
        out = h + self.ffn(self.ffn_norm(h))
        return out


# ---------------------------------------------------------------------------
# Ana Model
# ---------------------------------------------------------------------------
class KuroNekoModel(nn.Module):
    """KuroNeko v1 — 2B parametre decoder-only Transformer.

    Moduler tasarim: Katmanlar, attention, FFN, RoPE ayri moduller.
    Ileride yeni katman, expert veya aktivasyon eklemek icin
    ilgili modulu genisletin.

    Args:
        config: KuroNekoConfig (default: v1 hiperparametreleri).

    Example:
        >>> config = KuroNekoConfig()
        >>> model = KuroNekoModel(config)
        >>> ids = torch.randint(0, 64000, (2, 128))
        >>> logits = model(ids)
        >>> print(logits.shape)  # (2, 128, 64000)
    """

    def __init__(self, config: Optional[KuroNekoConfig] = None) -> None:
        super().__init__()
        self.config = config or KuroNekoConfig()
        cfg = self.config

        # Token embedding
        self.token_embedding = nn.Embedding(cfg.vocab_size, cfg.hidden_dim)
        self.dropout = nn.Dropout(cfg.dropout)

        # Paylasimli RoPE (tum katmanlar icin tek instance)
        self.rope = RoPE(
            head_dim=cfg.head_dim,
            max_len=cfg.context_length,
            theta=cfg.rope_theta,
        )

        # Transformer katmanlari
        self.layers = nn.ModuleList(
            [KuroNekoTransformerLayer(cfg, self.rope) for _ in range(cfg.num_layers)]
        )

        # Son RMSNorm
        self.norm = nn.RMSNorm(cfg.hidden_dim, eps=cfg.rms_norm_eps)

        # Output projection
        self.lm_head = nn.Linear(cfg.hidden_dim, cfg.vocab_size, bias=False)

        # Weight tying
        if cfg.tie_weights:
            self.lm_head.weight = self.token_embedding.weight

        # Baslat
        self.apply(self._init_weights)
        logger.info(
            "KuroNeko v1 olusturuldu: %.2fB parametre",
            self.num_params / 1e9,
        )

    def _init_weights(self, module: nn.Module) -> None:
        """Agirlik baslatma.

        Linear: N(0, 0.02)
        Embedding: N(0, 0.02)
        RMSNorm: weight=1.0

        Args:
            module: Baslatilacak modul.
        """
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.RMSNorm):
            nn.init.ones_(module.weight)

    @property
    def num_params(self) -> int:
        """Toplam parametre sayisi.

        Returns:
            int: Ogrenilebilir parametre sayisi.
        """
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(
        self,
        input_ids: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> dict[str, torch.Tensor]:
        """Ileri gecis.

        Args:
            input_ids: (batch, seq_len) token ID'leri.
            labels: (batch, seq_len) hedef token ID'leri (loss hesaplama).

        Returns:
            dict with keys:
                - logits: (batch, seq_len, vocab_size)
                - loss: scalar (labels verilmisse)
        """
        batch, seq_len = input_ids.shape

        # Embedding
        x = self.token_embedding(input_ids)
        x = self.dropout(x)

        # Causal mask (tek seferde olustur)
        mask = torch.triu(
            torch.ones(seq_len, seq_len, device=input_ids.device, dtype=torch.bool),
            diagonal=1,
        )

        # Katmanlari uygula
        for layer in self.layers:
            x = layer(x, mask)

        # Son norm + projection
        x = self.norm(x)
        logits = self.lm_head(x)

        result: dict[str, torch.Tensor] = {"logits": logits}

        # Loss hesapla
        if labels is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.shape[-1]),
                labels.view(-1),
                ignore_index=-100,
            )
            result["loss"] = loss

        return result

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 128,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.9,
    ) -> torch.Tensor:
        """Metin uret (auto-regressive).

        Args:
            input_ids: (batch, seq_len) baslangic token ID'leri.
            max_new_tokens: Maksimum yeni token sayisi.
            temperature: Sicaklik (0.0 = greedy).
            top_k: Top-K filtre (0 = kapali).
            top_p: Nucleus filtre (1.0 = kapali).

        Returns:
            (batch, seq_len + max_new_tokens) uretilen token ID'leri.
        """
        self.eval()
        generated = input_ids.clone()

        for _ in range(max_new_tokens):
            # Context window kontrolu
            ctx = generated[:, -self.config.context_length :]

            out = self.forward(ctx)
            logits = out["logits"][:, -1, :]

            # Temperature
            if temperature > 0:
                logits = logits / temperature
            else:
                # Greedy
                next_token = logits.argmax(dim=-1, keepdim=True)
                generated = torch.cat([generated, next_token], dim=1)
                continue

            # Top-K
            if top_k > 0:
                top_k_vals, _ = torch.topk(logits, min(top_k, logits.shape[-1]))
                min_val = top_k_vals[:, -1].unsqueeze(-1)
                logits = logits.masked_fill(logits < min_val, float("-inf"))

            # Top-P (nucleus)
            if top_p < 1.0:
                sorted_logits, sorted_idx = torch.sort(logits, descending=True)
                cumulative = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                mask = cumulative - F.softmax(sorted_logits, dim=-1) > top_p
                sorted_logits[mask] = float("-inf")
                logits = torch.zeros_like(logits).scatter_(-1, sorted_idx, sorted_logits)

            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            generated = torch.cat([generated, next_token], dim=1)

        return generated


# ---------------------------------------------------------------------------
# Parametre sayisi hesaplama (dogrulama)
# ---------------------------------------------------------------------------
def _count_params(config: KuroNekoConfig) -> dict[str, int]:
    """Teorik parametre sayisi hesapla.

    Args:
        config: Model yapilandirmasi.

    Returns:
        dict: Komponent bazinda parametre sayilari.
    """
    d = config.hidden_dim
    h = config.num_heads
    kv = config.num_kv_heads
    hd = config.head_dim
    v = config.vocab_size
    i = config.intermediate_size
    l = config.num_layers

    embedding = v * d
    attention_per_layer = (
        d * (h * hd)  # WQ
        + d * (kv * hd)  # WK
        + d * (kv * hd)  # WV
        + (h * hd) * d  # WO
    )
    ffn_per_layer = 2 * (d * i) + (d * i)  # W1, W2, W3
    norm_per_layer = 2 * d  # attention_norm + ffn_norm
    per_layer = attention_per_layer + ffn_per_layer + norm_per_layer
    final_norm = d
    lm_head = d * v if not config.tie_weights else 0

    return {
        "embedding": embedding,
        "per_layer": per_layer,
        "all_layers": per_layer * l,
        "final_norm": final_norm,
        "lm_head": lm_head,
        "total": embedding + per_layer * l + final_norm + lm_head,
    }


# ---------------------------------------------------------------------------
# Modul testi
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = KuroNekoConfig()
    params = _count_params(config)

    print("=" * 50)
    print("KuroNeko v1 — Parametre Dagilimi")
    print("=" * 50)
    for k, v in params.items():
        print(f"  {k:>15s}: {v:>15,} ({v / 1e9:.3f}B)")
    print("=" * 50)

    # Model olustur
    model = KuroNekoModel(config)
    print(f"\nToplam parametre: {model.num_params / 1e9:.3f}B")

    # Forward testi
    ids = torch.randint(0, config.vocab_size, (2, 128))
    out = model(ids)
    print(f"Forward cikis: {out['logits'].shape}")

    # Loss testi
    labels = torch.randint(0, config.vocab_size, (2, 128))
    out = model(ids, labels=labels)
    print(f"Loss: {out['loss'].item():.4f}")

    # Generate testi
    prompt = torch.randint(0, config.vocab_size, (1, 16))
    generated = model.generate(prompt, max_new_tokens=8, temperature=0.0)
    print(f"Generate cikis: {generated.shape}")
    print("\nTum testler basarili!")
