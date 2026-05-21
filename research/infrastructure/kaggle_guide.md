# Kaggle GPU Kotaları ve Verimli Kullanım
> Adım 61 | Tarih: 2026-05-21

## Kaggle GPU Kotalari
- **Ucretsiz:** 30 saat/hafta GPU (T4 veya P100)
- **Pro:** 30 saat/hafta GPU + ekstra
- **GPU Turleri:** T4 (16GB), P100 (16GB), V100 (16GB - sinirli)

## Verimli Kullanim Ipuclari

### 1. Offline Egitim
- Internet'i kapatin (hiz artar)
- Gerekirse indir, sonra offline yap

### 2. Checkpoint Stratejisi
- Her 100 step'te kaydet
- Son 3 checkpoint'i tut
- Google Drive'a yedekle

### 3. Veri On Isleme
- Veriyi once indir, isle
- Notebook'ta sadece egitim

### 4. Batch Size Optimizasyonu
- T4 icin batch=4-8
- Gradient accumulation ile buyut

### 5. Mixed Precision
- BF16 veya FP16 kullan
- Hiz: 2x, Bellek: %50 tasarruf

## Kaggle Notebook Ayarlari
- GPU: T4 x2 (multi-GPU)
- Internet: Kapali (onisleme sonrasi)
- Persistence: None (hizli ac)
- Language: Python

## Sure Hesaplama
- 1B model, 50K sample, 2 epoch: ~12-18 saat (T4)
- 30 saat kotasi yeterli (1 epoch = 6-9 saat)
- 2 epoch icin 2 hafta gerekir
