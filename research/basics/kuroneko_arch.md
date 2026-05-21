# KuroNeko Model Mimarisi — Tasarım Kararları
> Adım 8 | Tarih: 2026-05-21

## Model Tipi: Decoder-Only Transformer

## Parametre Sayısı Kararı

### Seçenekler
| Model | Parametre | Context | RAM (4bit) | Telefon |
|-------|-----------|---------|-------------|---------|
| Küçük | 360M | 2048 | ~250MB | ✅ Rahat |
| Orta | 1.1B | 4098 | ~600MB | ✅ İyi |
| Büyük | 3B | 4096 | ~1.8GB | ⚠️ Sınır |

### KuroNeko v1 Kararı: 1.1B parametre
- **Gerekçe:**
  - Telefonda rahat çalışır (~600MB RAM, 4bit)
  - Kod yazma için yeterli kapasite
  - Kaggle'da 15GB GPU ile eğitilebilir
  - Llama-3.2-1B ile aynı seviye
  - Fine-tuning için ideal boyut

## Mimari Detaylar

```
KuroNeko-1B Config:
- d_model: 2048
- n_layers: 24
- n_heads: 16 (query heads)
- n_kv_heads: 4 (GQA, 4:1 oran)
- d_ff: 5632 (d_model * 2.75, SwiGLU)
- vocab_size: 32000
- max_seq_length: 4096
- rope_theta: 500000 (Llama 3 uyumlu)
- rms_norm_eps: 1e-5
- dropout: 0.0 (eğitimda 0.1)
- activation: SwiGLU
- positional_encoding: RoPE
- normalization: RMSNorm (pre-norm)
- attention: GQA + Flash Attention
- weight_tying: True (embedding + lm_head)
```

## Toplam Parametre Hesabı
- Embedding: 32000 * 2048 = 65.5M
- Transformer blocks: 24 * (attention + ffn) ≈ 900M
- Output head: 2048 * 32000 = 65.5M (weight tying ile aynı)
- **Toplam: ~1.03B parametre**

## Eğitim Gereksinimleri
- GPU: 15GB+ (Kaggle T4/V100)
- VRAM: ~12GB (4bit QLoRA ile ~8GB)
- RAM: 32GB+
- Disk: 50GB+ (checkpoint'ler için)
- Süre: 3-7 gün (Kaggle, 1 epoch)

## Karşılaştırma
| Özellik | KuroNeko-1B | Llama-3.2-1B | Phi-2 | Gemma-2B |
|---------|-------------|--------------|-------|----------|
| Parametre | 1.1B | 1.1B | 2.7B | 2B |
| Context | 4096 | 128K | 2048 | 8192 |
| Kod | ✅ Uzman | Genel | İyi | İyi |
| Türkçe | ✅ Uzman | Orta | Zayıf | Orta |
| Telefon | ✅ | ✅ | ✅ | ✅ |
