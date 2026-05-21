# Gradient Accumulation ve Mixed Precision
> Adım 17 | Tarih: 2026-05-21

## Gradient Accumulation
- Küçük batch'lerde gradient biriktirilir
- N adım sonra bir update yapılır
- Efektif batch = batch_size * accumulation_steps
- Örnek: batch=4, accumulation=4 → efektif=16
- Bellek tasarrufu: Daha küçük batch = daha az VRAM

## Mixed Precision
- FP16/BF16 kullanarak hız ve bellek tasarrufu
- FP32 master weights + FP16 compute
- BF16: A100, H100'te daha iyi (T4'te FP16)
- Loss scaling: Gradient underflow önleme
- KuroNeko: BF16 (desteklenmiyorsa FP16)

## KuroNeko Eğitim Konfig
```python
training_args = {
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "warmup_steps": 50,
    "num_train_epochs": 2,
    "learning_rate": 2e-4,
    "fp16": False,
    "bf16": True,
    "optim": "adamw_8bit",
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,
    "logging_steps": 10,
    "save_steps": 100,
}
```
