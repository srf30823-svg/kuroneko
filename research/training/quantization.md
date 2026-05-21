# 4bit Quantization
> Adım 15 | Tarih: 2026-05-21

## Quantization Nedir?
- Model ağırlıklarının düşük precision'a dönüştürülmesi
- FP32 → FP16 → INT8 → INT4

## 4bit Quantization Türleri
- NF4 (Normal Float 4): En iyi kalite, QLoRA'da kullanılır
- INT4: Basit, hızlı
- GPTQ: Post-training quantization
- AWQ: Activation-aware quantization
- GGUF: llama.cpp için quantization formatı

## Kalite Etkisi
| Format | Bellek | Kalite Kaybı |
|--------|--------|--------------|
| FP32 | 100% | 0% |
| FP16 | 50% | ~0% |
| INT8 | 25% | ~1% |
| NF4 (4bit) | 12.5% | ~2-3% |

## KuroNeko: NF4 (bitsandbytes)
- QLoRA ile birlikte kullanılır
- bitsandbytes kütüphanesi
- 1B model: ~2.5GB VRAM (eğitim), ~0.6GB (inference)
