# Veri Seti Envanteri

## Ham Veri Dağılımı

| Kaynak | Ham Boyut | Temizlenmiş | Token (64K) |
|--------|-----------|-------------|-------------|
| FineWeb-2 (tr) | 20GB | 15GB | ~3B |
| OSCAR (tr) | 27GB | 20GB | ~4B |
| CC-100 (tr) | 15GB | 10GB | ~2B |
| Wikipedia (tr) | 0.5GB | 0.4GB | ~80M |
| OPUS (tr) | 5GB | 3GB | ~600M |
| The Stack v2 (kod) | 468GB | 100GB | ~20B |
| Türkçe özel | 5GB | 3GB | ~600M |
| **Toplam** | **~540GB** | **~150GB** | **~30B** |

## Chinchilla Analizi
- Model: 2B parametre
- Chinchilla optimal: 20 × N = 40B token
- **Sonuç**: 30B token yeterli (Chinchilla altında ama kabul edilebilir)

## Token Dağılımı
| Kategori | Token | Yüzde |
|----------|-------|-------|
| Türkçe web | 10B | 33% |
| Kod | 15B | 50% |
| İngilizce | 3B | 10% |
| Diğer | 2B | 7% |
| **Toplam** | **30B** | **100%** |

## Kaynaklar
- HuggingFace datasets
- Common Crawl
- BigCode Project
