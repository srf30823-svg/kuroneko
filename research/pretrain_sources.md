# Pre-training Veri Kaynakları

## Türkçe + Kod Veri Kaynakları

### Açık Kaynak Dataset'ler
| Dataset | Boyut | Lisans | Açıklama |
|---------|-------|--------|----------|
| FineWeb-2 (tr) | ~20GB | ODC-BY | Yüksek kalite web crawl |
| OSCAR-2301 (tr) | ~27GB | CC0 | Common Crawl Türkçe |
| CC-100 (tr) | ~15GB | CC0 | Common Crawl 100 dil |
| Wikipedia (tr) | ~500MB | CC BY-SA | Wikipedia dump |
| OPUS | ~5GB | Çeşitli | Paralel corpus |
| The Stack v2 | ~468GB | Permissive | Kod verisi |
| CodeSearchNet | ~2GB | Çeşitli | Fonksiyon seviye kod |

### Türkçe Spesifik
| Kaynak | Boyut | Açıklama |
|--------|-------|----------|
| TS Corpus | ~5GB | Türkçe metin corpus |
| BounTr | ~1GB | Boğaziçi Türkçe |
| Turkish Wikipedia | ~500MB | Wikipedia |
| Turkish News | ~2GB | Haber metinleri |

## Önerilen Dağılık (Toplam ~100GB)
| Kategori | Boyut | Yüzde |
|----------|-------|-------|
| Türkçe web (FineWeb + OSCAR) | 40GB | 40% |
| Kod (The Stack v2) | 30GB | 30% |
| Wikipedia + akademik | 10GB | 10% |
| Türkçe özel (haber, kitap) | 10GB | 10% |
| Diğer (QA, instruction seed) | 10GB | 10% |

## Kaynaklar
- HuggingFace Datasets
- Common Pile — Best Practices for Open Datasets
- Bridging the Bosphorus — Turkish LLM paper
