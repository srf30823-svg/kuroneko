# Checkpoint Stratejisi
> Adım 64 | Tarih: 2026-05-21

## Nedir?
Egitim sirasinin belirli noktalarinda modeli kaydetme
Kaldigin yerden devam etme imkani

## Strateji

### Kaydetme Sikligi
- Her 100 step'te kaydet
- Son 3 checkpoint'i tut (disk tasarrufu)
- En iyi modeli ayri kaydet

### Checkpoint Icerigi
- Model agirlilari (LoRA adapter)
- Tokenizer
- Optimizer state (devam icin)
- Training args
- Step sayisi

### Google Drive Entegrasyonu
```python
from google.colab import drive
drive.mount('/content/drive')

# Kaydet
!cp -r /content/output /content/drive/MyDrive/kuroneko/checkpoints/
```

### Kaggle Output
- Output klasorunu otomatik kaydet
- Dataset olarak paylas

## Kurtarma
```python
# Checkpoint'ten devam
trainer.train(resume_from_checkpoint="output/checkpoint-500")
```

## KuroNeko Icin
- Save steps: 100
- Keep: 3 checkpoint
- Best model: Ayri kaydet
- Google Drive: Her 500 step'te yedek
