# HuggingFace TRL Kütüphanesi
> Adım 44 | Tarih: 2026-05-21

## Nedir?
Transformer Reinforcement Learning
SFT, DPO, PPO, KTO destekleyen kütüphane

## Ana Modüller

### SFTTrainer
```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="output",
        num_train_epochs=2,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
    ),
)
trainer.train()
```

### DPOTrainer
```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=DPOConfig(
        output_dir="output",
        beta=0.1,
        num_train_epochs=1,
    ),
    train_dataset=preference_dataset,
)
trainer.train()
```

### PPOTrainer
```python
from trl import PPOTrainer

# Reward model + PPO training
# Daha karmaşık, RLHF için
```

## Desteklenen Özellikler
- LoRA/QLoRA entegrasyonu
- Gradient checkpointing
- Mixed precision
- Distributed training
- W&B logging

## KuroNeko İçin
- SFTTrainer: İlk eğitim
- DPOTrainer: Tercih hizalama
- PPOTrainer: v2'de değerlendirilebilir
