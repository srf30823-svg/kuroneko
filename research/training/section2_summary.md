# Bölüm 2 Özeti — Eğitim Teknikleri
> Adım 20 | Tarih: 2026-05-21

## Tamamlanan Adımlar
11. ✅ Pre-training araştır → pretraining.md
12. ✅ Fine-tuning vs instruction tuning → finetuning_vs_instruction.md
13. ✅ LoRA ve QLoRA derinlemesine → lora_guide.md
14. ✅ Unsloth reposunu incele → unsloth_notes.md
15. ✅ 4bit quantization → quantization.md
16. ✅ Eğitim parametreleri → training_params.md
17. ✅ Gradient accumulation ve mixed precision → gradient_mixed.md
18. ✅ Overfitting önleme → overfitting.md
19. ✅ KuroNeko eğitim parametreleri → kuroneko_train_params.md

## Önemli Kararlar
- **Yöntem:** QLoRA (4bit + LoRA) — Kaggle T4 ile çalışır
- **Base Model:** Llama-3.2-1B (Unsloth versiyonu)
- **LoRA Rank:** 16, Alpha: 32
- **Batch:** 4 (efektif 16, accumulation=4)
- **LR:** 2e-4, cosine schedule, 50 warmup
- **Epoch:** 2
- **Precision:** BF16 (yoksa FP16)
- **Optimizer:** AdamW 8bit

## Oluşturulan Dosyalar (10)
pretraining.md, finetuning_vs_instruction.md, lora_guide.md, unsloth_notes.md,
quantization.md, training_params.md, gradient_mixed.md, overfitting.md,
kuroneko_train_params.md, section2_summary.md
