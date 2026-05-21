# Chinchilla Yasası Analizi

## Chinchilla Scaling Law
- **Formül**: C = N × D (C: compute, N: parametre, D: data token)
- **Optimal**: D = 20 × N (N = model parametre sayısı)

## KuroNeko v1 İçin Hesaplama
- **Model**: 2B parametre
- **Optimal veri**: 20 × 2B = 40B token
- **Mevcut veri**: ~30B token (64K vocab ile)
- **Durum**: Chinchilla altında ama kabul edilebilir

## Tradeoff Analizi
| Token Sayısı | Chinchilla | Kalite | Süre |
|-------------|------------|--------|------|
| 20B | 0.5x | Temel | 1x |
| 40B | 1.0x | Optimal | 2x |
| 60B | 1.5x | İyi | 3x |
| 100B | 2.5x | Çok iyi | 5x |

## Sonuç
30B token ile eğitim yapılacak. Bu:
- Chinchilla'nın %75'i
- A100 1 GPU'da ~2 hafta
- Kaggle P100 ile ~1 ay (kısıtlı GPU saatleri)

## İyileştirme Senaryoları
1. **Veri kalitesini artır**: Daha az ama daha iyisini kullan
2. **Multi-epoch**: 2 epoch ile 60B token'a ulaş
3. **Veri çeşitliliği**: Daha fazla kod + akademik metin

## Kaynaklar
- Hoffmann et al. (2022) — Training Compute-Optimal Large Language Models
- arXiv — Scaling Laws for Neural Language Models
