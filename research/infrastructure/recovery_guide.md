# Hata Kurtarma Stratejisi
> Adım 68 | Tarih: 2026-05-21

## Olasi Hatalar ve Cozumleri

### 1. GPU OOM (Out of Memory)
**Belirti:** RuntimeError: CUDA out of memory
**Cozum:**
- Batch size yuselt (4 -> 2)
- Gradient accumulation artir
- Gradient checkpointing ac
- Daha kucuk model kullan

### 2. Colab/Kaggle Reset
**Belirti:** Baglanti kesildi, notebook reset
**Cozum:**
- Checkpoint'ten devam
- Google Drive'a yedek
- Kaggle: Output dataset olarak kaydet

### 3. Loss NaN
**Belirti:** Loss NaN veya Inf
**Cozum:**
- Learning rate dusur
- Gradient clipping kontrol et
- Veri kontrol et (NaN deger var mi?)

### 4. Veri Hatasi
**Belirti:** Egitim donuyor, hata veriyor
**Cozum:**
- Veri formatini kontrol et
- Tokenizer hatasi
- Bos ornekleri filtrele

### 5. Checkpoint Bozulmasi
**Belirti:** Model yuklenemiyor
**Cozum:**
- Onceki checkpoint'ten devam
- Checkpoint formatini kontrol et

## Otomatik Kurtarma
```python
def train_with_recovery(trainer, max_retries=3):
    for attempt in range(max_retries):
        try:
            trainer.train(resume_from_checkpoint=True)
            return True
        except RuntimeError as e:
            if "out of memory" in str(e):
                torch.cuda.empty_cache()
                print(f"OOM hatasi, retry {attempt+1}")
            else:
                raise
    return False
```

## Yedekleme Plani
- Her 100 step: Checkpoint
- Her 500 step: Google Drive
- Her epoch: HuggingFace Hub (opsiyonel)
