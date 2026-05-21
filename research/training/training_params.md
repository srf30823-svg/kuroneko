# Eğitim Parametreleri
> Adım 16 | Tarih: 2026-05-21

## Learning Rate
- LoRA fine-tuning: 1e-4 ile 5e-4 arası
- KuroNeko: 2e-4 (standart)
- Çok yüksek: Overfitting, çok düşük: Yavaş öğrenme

## Batch Size
- Küçük GPU: 1-4
- Orta GPU: 4-16
- Büyük GPU: 16-64
- Gradient accumulation ile efektif batch büyütülür
- KuroNeko: batch=4, accumulation=4 (efektif=16)

## Warmup Steps
- İlk birkaç adımda LR yükselir
- Toplam step'in %5-10'u
- KuroNeko: 50 steps warmup

## Epochs
- Instruction tuning: 1-3 epoch
- Çok fazla: Overfitting
- KuroNeko: 2 epoch

## Optimizer
- AdamW: Standart (weight decay ile)
- LR Scheduler: Cosine with warmup
- Weight decay: 0.01
- Beta1: 0.9, Beta2: 0.95
- Grad clip: 1.0
