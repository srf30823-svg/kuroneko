# Veri Seti README

## İçerik
Bu dizin KuroNeko v1 modeli için kullanılan veri setlerini içerir.

## Dizin Yapısı
```
data/
├── raw/           # Ham veri (indirildikten sonra)
├── clean/         # Temizlenmiş veri
├── instruction/   # Instruction tuning verisi
├── dpo/           # DPO preference verisi
├── test/          # Test seti
├── tokenizer_train.txt  # Tokenizer eğitim verisi
├── README.md      # Bu dosya
└── dataset_card.md  # Veri kartı
```

## İndirme
Veri setleri büyük olduğu için HuggingFace üzerinden indirilir:
```bash
from datasets import load_dataset
ds = load_dataset("kuroneko/pretrain-data")
```

## Lisans
Apache 2.0
