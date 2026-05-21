# Veri Seti Kartı — KuroNeko v1

## Genel Bilgiler
- **Proje**: KuroNeko v1 — Türkçe + Kod LLM
- **Versiyon**: 1.0.0
- **Tarih**: 2026-05-21
- **Lisans**: Apache 2.0

## Veri Kaynakları
- FineWeb-2 (Türkçe): ~15GB
- OSCAR (Türkçe): ~20GB
- CC-100 (Türkçe): ~10GB
- Wikipedia (Türkçe): ~0.4GB
- OPUS (Türkçe): ~3GB
- The Stack v2 (kod): ~100GB
- Türkçe özel: ~3GB

## İstatistikler
- Toplam ~150GB temiz veri
- ~30B token (64K vocab)
- Train/Val/Test: 98/1/1

## Kullanım
```python
from datasets import load_dataset
ds = load_dataset("kuroneko/pretrain-data", split="train")
```

## Kaynaklar
- HuggingFace: kuroneko/pretrain-data
- GitHub: srf30823-svg/kuroneko
