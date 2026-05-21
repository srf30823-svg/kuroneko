# Kaggle Altyapısı — GPU ve Bellek

## Kaggle GPU Seçenekleri
| GPU | VRAM | Hız | Kullanım |
|-----|------|-----|----------|
| P100 | 16GB | Orta | Ücretsiz, sınırlı saat |
| T4 x2 | 16GB | Orta | Ücretsiz, sınırlı saat |
| 2x T4 | 32GB | Orta | Notebook yarışmaları |

## P100 Özellikleri
- VRAM: 16GB
- FP32: 10.6 TFLOPS
- FP16: Destek yok (bf16 yok)
- NVLink: Yok

## Bellek Optimizasyonu (P100 16GB)
| Teknik | Bellek Tasarrufu |
|--------|-----------------|
| Gradient checkpointing | ~40% |
| Mixed precision (FP16) | ~30% |
| Gradient accumulation | Effective batch size |
| Smaller batch size | Doğrudan |

## Batch Size Hesaplama
- Model: 2B parametre × 2 byte (FP16) = 4GB
- Gradients: 4GB
- Optimizer states: 8GB (AdamW)
- Activations: ~2GB
- **Toplam**: ~18GB → 16GB'dan fazla!

## Çözüm
- Gradient checkpointing: 18GB → 12GB
- Sequence length: 2048 yerine 1024
- Batch size: 1-2 per GPU
- Gradient accumulation: 8-16 steps

## Kaynaklar
- Kaggle documentation
- PyTorch memory management
