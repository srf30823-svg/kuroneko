# Türkçe Metin Kaynakları

## Ana Kaynaklar

### 1. Turkish Wikipedia
- **Boyut**: ~500MB (dump)
- **Kalite**: Yüksek (editör kontrollü)
- **Lisans**: CC BY-SA
- **İndirme**: https://dumps.wikimedia.org/trwiki/
- **İşleme**: WikiExtractor ile markup temizleme

### 2. OSCAR (Open Super-large Crawled Aggregated coRpus)
- **Boyut**: ~27GB (Türkçe kısım)
- **Kalite**: Orta (web crawl, filtreli)
- **Lisans**: CC0 benzeri
- **İndirme**: HuggingFace — `oscar-corpus/OSCAR-2301` (tr)
- **İşleme**: Dil tespiti zaten yapılmış

### 3. Common Crawl — CC-100
- **Boyut**: ~15GB (Türkçe kısım)
- **Kalite**: Orta (otomatik filtreli)
- **Lisans**: CC0
- **İndirme**: HuggingFace — `cc100` (tr)
- **İşleme**: URL filtreleme, dedup

### 4. OPUS (Open Parallel Corpus)
- **Boyut**: ~5GB (Türkçe-İngilizce paralel)
- **Kalite**: Yüksek (çeviri kalitesi)
- **Lisans**: Çeşitli (çoğu açık)
- **İndirme**: https://opus.nlpl.eu/
- **Kaynaklar**: OpenSubtitles, Tatoeba, UN Corpus

### 5. FineWeb-2 (Türkçe)
- **Boyut**: ~20GB
- **Kalite**: Çok yüksek (FineWeb filtreleme)
- **Lisans**: ODC-BY
- **İndirme**: HuggingFace — `HuggingFaceFW/fineweb-2` (tr)

### 6. Türkçe NLP Suite
- **Kaynak**: GitHub agmmnn/turkish-nlp-resources
- **İçerik**: NER, sentiment, medical, legal
- **Lisans**: Çeşitli

## Önerilen Dağılık (Toplam ~50GB)
| Kaynak | Boyut | Yüzde |
|--------|-------|-------|
| FineWeb-2 | 20GB | 40% |
| OSCAR | 10GB | 20% |
| CC-100 | 8GB | 16% |
| Wikipedia | 2GB | 4% |
| OPUS | 3GB | 6% |
| Türkçe NLP | 2GB | 4% |
| Diğer | 5GB | 10% |
| **Toplam** | **50GB** | **100%** |

## Kaynaklar
- HuggingFace Datasets
- OSCAR Corpus
- OPUS
- GitHub agmmnn/turkish-nlp-resources
