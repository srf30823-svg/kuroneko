# Erken Durdurma Kriterleri
> Adım 59 | Tarih: 2026-05-21

## Nedir?
Eğitim kötüleşmeye başladığında otomatik durdurma

## Kriterler

### Validation Loss
- 3 ardışık evaluation'da loss artarsa durdur
- Patience: 3
- Threshold: 0.01

### Overfitting Tespiti
- Train loss düşer, val loss yükselir
- Gap > 0.2 ise uyarı
- Gap > 0.5 ise durdur

### Plateau
- 5 evaluation'da iyileşme < 0.001
- Learning rate çok düşük

### GPU OOM
- Out of memory hatası
- Batch size otomatik düşür

## Implementasyon
```python
class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.01):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
    
    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
            return False
        
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
        
        return self.counter >= self.patience
```

## KuroNeko İçin
- Patience: 3
- Min delta: 0.01
- Check every: 50 steps
- Save best model: Evet
