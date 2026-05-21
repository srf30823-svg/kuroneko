# Kaggle Notebook Sablonu
> Adım 63 | Tarih: 2026-05-21

## Notebook Yapisi

### Hucre 1: Kurulum
```python
# Gerekli kutuphaneler
!pip install unsloth transformers datasets trl wandb -q

# W&B giris
import wandb
wandb.login()
```

### Hucre 2: Veri Yukleme
```python
from datasets import load_dataset

# Veri setini yukle
dataset = load_dataset("json", data_files="kuroneko_train.jsonl")
print(f"Train: {len(dataset['train'])} ornek")
```

### Hucre 3: Model Yukleme
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length=4096,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
```

### Hucre 4: Egitim
```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    args=TrainingArguments(
        output_dir="output",
        num_train_epochs=2,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=10,
        save_steps=100,
        warmup_steps=50,
    ),
)

trainer.train()
```

### Hucre 5: Kaydetme
```python
model.save_pretrained("kuroneko-v1")
tokenizer.save_pretrained("kuroneko-v1")

# GGUF
model.save_pretrained_gguf("kuroneko-v1-gguf", tokenizer, "q4_k_m")
```
