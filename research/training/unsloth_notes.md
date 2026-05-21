# Unsloth Analizi
> Adım 14 | Tarih: 2026-05-21

## Unsloth Nedir?
- LLM fine-tuning kütüphanesi
- Hız: 2-5x daha hızlı
- Bellek: %60 daha az VRAM
- Kalite: Aynı (loss değerleri aynı)

## Optimizasyonlar
1. Flash Attention 2 entegrasyonu
2. Manuel CUDA kernel optimizasyonları
3. Kuantizasyon optimizasyonu (NF4)
4. LoRA kernel optimizasyonu
5. Gradient checkpointing optimizasyonu
6. RoPE (QK rotary embedding) füzyonu

## Desteklenen Modeller
- Llama (1, 2, 3, 3.1, 3.2)
- Mistral, Mixtral
- Gemma (1, 2)
- Phi (2, 3, 4)
- Qwen (1, 2, 2.5, 3)
- DeepSeek (V2, V3, R1)
- TinyLlama

## Kullanım
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

## KuroNeko İçin Avantajlar
- Kaggle T4 (15GB) ile 1B model eğitilebilir
- Eğitim süresi: 2-3x kısalır
- Maliyet: Daha az GPU saati
- Kolay kurulum: pip install unsloth
