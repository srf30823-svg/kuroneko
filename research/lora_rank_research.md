# LoRA (Low-Rank Adaptation) — Araştırma

## Neden LoRA?
- **Verimli**: Sadece küçük matrisler öğrenilir
- **Hızlı**: Full fine-tuning'den 3x hızlı
- **Bellek**: Daha az GPU belleği

## Hiperparametreler
| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| r | 8-64 | Rank (düşük = daha az parametre) |
| alpha | 16-64 | Scaling factor |
| target_modules | q_proj, v_proj, k_proj, o_proj | Hangi katmanlara uygulanır |
| dropout | 0.05-0.1 | Regularizasyon |

## KuroNeko v1 İçin
```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["wq", "wk", "wv", "wo"],
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(model, config)
```

## Rank Seçimi
- **r=8**: Hızlı, düşük kalite
- **r=16**: Dengeli (önerilen)
- **r=32**: İyi kalite
- **r=64**: Yüksek kalite, yavaş

## Kaynaklar
- Hu et al. (2021) — LoRA: Low-Rank Adaptation of Large Language Models
- HuggingFace PEFT documentation
