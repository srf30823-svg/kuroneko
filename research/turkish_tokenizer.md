# Türkçe İçin Tokenizer Stratejisi

## Türkçe Morfoloji Sorunu

Türkçe aglutinatif bir dildir. Bir kelime tek başına bir cümle anlamı taşıyabilir:
- "Çekoslovakyalılaştıramadıklarımızdan" = "Onların arasından Slovakya yapamadıklarımız"
- Bu tek kelime BPE ile 8-12 token'a ayrılır

## Sorunlar
1. **Ek patlaması**: Her ek ayrı token → context window israfı
2. **Nokalandırma**: Kelimeler tutarsız bölünür
3. **Vocab israfı**: Benzer ekler farklı token'larda
4. **Kod-switching**: Türkçe-İngilizce karışık metinlerde verimsizlik

## Çözüm Stratejileri

### 1. Morphology-First Hybrid Tokenizer (Önerilen)
- Önce morfolojik analiz (Zemberek, TRmorph)
- Kök + ek ayrıştırması yap
- BPE'yi morfolojik parçalar üzerinde çalıştır
- **Kaynak**: arXiv 2508.14292 — "Tokens with Meaning: A Hybrid Tokenization Approach for Turkish"

### 2. Byte-Level BPE + Büyük Vocab
- 64K-128K vocab size
- Byte-level base → UNK yok
- Yeterli veri ile Türkçe kalıplar öğrenilir
- **Tradeoff**: Daha büyük embedding tablosu

### 3. Pre-tokenization Optimizasyonu
- Türkçe'ye özel pre-tokenizer
- Ek sınırlarını belli et
- N-gram tabanlı pre-segmentasyon

## Mevcut Türkçe Tokenizer'lar
- **BERT-multilingual**: WordPiece, 110K vocab — Türkçe için optimize değil
- **Turkish-BERT**: WordPiece, 32K vocab — daha iyi ama hâlâ sorunlu
- **SentencePiece Türkçe**: 32K vocab — raw text avantajı
- **Custom BPE (malibayram/tokenizer)**: Morphology-aware hybrid

## KuroNeko İçin Öneri
1. **Byte-Level BPE, 64K vocab** — başlangıç için en pratik
2. **Pre-tokenizer**: whitespace + punctuation + Türkçe özel kurallar
3. **Özel tokenlar**: Morfolojik sınırları işaretleyen tokenlar
4. **İterasyon**: v2'de morphology-first hybrid'a geçiş planla

## Kaynaklar
- arXiv 2508.14292 — Hybrid Tokenization for Turkish
- ResearchGate — Impact of Tokenization on Turkish LLM
- Reddit r/LocalLLaMA — BPE for agglutinative languages
- GitHub malibayram/tokenizer — Turkish tokenizer research
