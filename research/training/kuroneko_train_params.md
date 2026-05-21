# KuroNeko Eğitim Parametreleri
> Adım 19 | Tarih: 2026-05-21

## Tam Eğitim Konfigürasyonu

```python
kuroneko_train_config = {
    # Model
    "base_model": "unsloth/Llama-3.2-1B-bnb-4bit",
    "max_seq_length": 4096,

    # LoRA
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],

    # Eğitim
    "num_epochs": 2,
    "batch_size": 4,
    "gradient_accumulation": 4,
    "learning_rate": 2e-4,
    "warmup_steps": 50,
    "weight_decay": 0.01,
    "max_grad_norm": 1.0,

    # Precision
    "bf16": True,
    "fp16": False,

    # Kaydetme
    "save_steps": 100,
    "eval_steps": 50,
    "logging_steps": 10,
    "save_total_limit": 3,

    # Optimizer
    "optim": "adamw_8bit",
    "lr_scheduler": "cosine",

    # Veri
    "dataset_path": "data/kuroneko_train.jsonl",
    "val_split": 0.05,
    "max_samples": None,  # Tüm veri

    # W&B
    "use_wandb": True,
    "wandb_project": "kuroneko",
    "wandb_run_name": "kuroneko-v1-run1",

    # Output
    "output_dir": "models/kuroneko-v1",
    "push_to_hub": False,
}
```

## Tahmini Eğitim Süresi
- Kaggle T4: ~12-18 saat (2 epoch, 50K sample)
- Kaggle V100: ~8-12 saat
- Colab T4: ~15-20 saat

## Tahmini Maliyet
- Kaggle: Ücretsiz (30H/hafta GPU)
- Colab Pro: ~$10/ay
- Bulut GPU: ~$0.5-1/saat
