# Veri Kalitesi ve Temizleme
> Adım 22 | Tarih: 2026-05-21

## Veri Kalitesi Metrikleri
- **Deduplikasyon:** Tekrar eden örnekleri çıkar
- **Uzunluk filtresi:** Çok koksa/uzunsa at
- **Dil tespiti:** Yanlış dildeki örnekleri çıkar
- **Kalite skoru:** Model kalitesini ölç (perplexity, length ratio)
- **Toxicity filtresi:** Zararlı içeriği çıkar

## Temizleme Adımları
1. HTML/Markdown temizleme
2. URL ve email çıkarma
3. Özel karakter normalizasyonu
4. Deduplikasyon (exact + fuzzy)
5. Uzunluk filtresi (min 50, max 4000 token)
6. Dil tespidi (langdetect)
7. Kalite filtresi (heuristic + model-based)

## Araçlar
- **datasets** (HuggingFace): Yükleme, filtreleme
- **deduplicate** (GitHub): Fuzzy deduplikasyon
- **fasttext**: Dil tespiti
- **clean-text**: Metin temizleme

## KuroNeko Pipeline
```
Ham veri → HTML temizle → Dedup → Dil tespiti → Uzunluk filtresi → Kalite skoru → JSONL
```
