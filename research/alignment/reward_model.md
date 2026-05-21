# Reward Model
> Adım 45 | Tarih: 2026-05-21

## Nedir?
Model çıktılarını değerlendiren ikincil model
RLHF pipeline'ının parçası

## Eğitimi
1. İnsan tercih verisi toplanır (A vs B)
2. Bradley-Terry model ile eğitilir
3. Loss: -log(σ(r(chosen) - r(rejected)))

## Mimari
- Base model + lineer head (skalar output)
- Genelde eğitilen modelin kendisi kullanılır
- Boyut: Eğitilen model ile aynı

## Kullanım
```python
from transformers import AutoModelForSequenceClassification

reward_model = AutoModelForSequenceClassification.from_pretrained(
    "reward_model", num_labels=1
)

score = reward_model(**inputs).logits
```

## KuroNeko İçin
- v1'de reward model yok (DPO kullanılacak)
- v2'de RLHF ile birlikte değerlendirilebilir
