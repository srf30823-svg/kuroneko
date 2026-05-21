# Flash Attention 2 — Araştırma

## Neden Flash Attention?
- **Bellek**: O(N) yerine O(1) attention map
- **Hız**: 2-4x hızlanma
- **Uzun context**: 4K+ token için kritik

## Kurulum
```bash
pip install flash-attn --no-build-isolation
```

## Kullanım
```python
from flash_attn import flash_attn_func

# q, k, v: (batch, seq_len, num_heads, head_dim)
out = flash_attn_func(q, k, v, causal=True)
```

## Kurallar
- head_dim: 64 veya 128 olmalı
- dtype: fp16 veya bf16
- seq_len: 2'nin kuvveti olması tercih edilir

## KuroNeko v1 İçin
- head_dim = 128 (2048/16)
- bf16 desteği var
- 4096 context → Flash Attention kritik

## Kaynaklar
- Dao et al. (2022) — FlashAttention: Fast and Memory-Efficient Exact Attention
- GitHub Dao-AILab/flash-attention
