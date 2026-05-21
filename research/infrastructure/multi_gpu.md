# Coklu GPU Egitimi
> Adım 66 | Tarih: 2026-05-21

## Nedir?
Birden fazla GPU ile es zamanli egitim
Sureyi kisaltir, buyuk batch imkani verir

## Yontemler

### Data Parallelism (DDP)
- Her GPU'da model kopyasi
- Veri GPU'lara bolusur
- Basit, etkili
- Kaggle T4 x2 icin ideal

### Model Parallelism
- Model GPU'lara bolusur
- Buyuk modeller icin
- Daha kompleks

### FSDP (Fully Sharded Data Parallel)
- Model + optimizer + gradient sharding
- En verimli bellek kullanimi
- PyTorch 2.0+

## Kaggle T4 x2 Kullanimi
```python
# Unsloth otomatik DDP destekler
# Tek GPU kodunu calistir, otomatik olusur

# Veya manuel:
torchrun --nproc_per_node=2 train.py
```

## KuroNeko Icin
- 1B model icin tek GPU yeterli
- T4 x2: Daha buyuk batch, hizli egitim
- Ilk egitim: Tek T4
- v2: T4 x2 degerlendirilebilir
