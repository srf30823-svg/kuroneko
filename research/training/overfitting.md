# Overfitting Önleme
> Adım 18 | Tarih: 2026-05-21

## Overfitting Nedir?
- Model eğitim verisini ezberler, genelleme yapamaz
- Training loss düşer, validation loss yükselir

## Önleme Teknikleri

### Dropout
- Rastgele nöronları kapatma
- Attention dropout: 0.0-0.1
- Hidden dropout: 0.0-0.1
- KuroNeko: 0.0 (LoRA ile zaten regularization var)

### Weight Decay
- L2 regularization
- Büyük ağırlıkları cezalandırır
- KuroNeko: 0.01

### Early Stopping
- Validation loss artarsa durdur
- Patience: 3-5 evaluation step
- KuroNeko: 3 patience

### Veri Çeşitliliği
- Farklı kaynaklardan veri
- Deduplikasyon
- Format çeşitliliği

### Epoch Sayısı
- Instruction tuning: 1-3 epoch yeterli
- KuroNeko: 2 epoch

### Learning Rate Scheduling
- Cosine decay: Yavaş yavaş azalt
- Linear decay: Doğrusal azalt
- KuroNeko: Cosine with warmup
