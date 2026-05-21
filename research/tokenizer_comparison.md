# Tokenizer Karşılaştırması: WordPiece vs SentencePiece vs BPE

## Genel Bakış

| Özellik | BPE | WordPiece | SentencePiece |
|---------|-----|-----------|---------------|
| Algoritma | Frekans bazlı merge | Likelihood bazlı merge | Unigram veya BPE |
| Kullanılan modeller | GPT-2, Llama, Gemma, Qwen | BERT, DeBERTa, RoBERTa | T5, ALBERT, XLNet, Mistral |
| Pre-tokenization | Gerekli (whitespace) | Gerekli (whitespace) | Gerekli değil (raw text) |
| Dil bağımsızlık | Yüksek | Orta | En yüksek |
| UNK handling | Byte-level'da yok | [UNK] token | Byte-level'da yok |
| Space tokenization | Ayrı token (_) | Ayrı token | Vocab'da space |
| Eğitim hızı | Hızlı | Orta | Yavaş (Unigram) |
| Çıkarım hızı | Hızlı | Hızlı | Orta |

## BPE (Byte-Pair Encoding)
- **Avantaj**: Basit, hızlı, yaygın destek
- **Dezavantaj**: Greedy matching, morfolojik farkındalık yok
- **En iyi kullanım**: Decoder-only LLM'ler, çok dilli modeller

## WordPiece
- **Avantaj**: Likelihood bazlı → daha kaliteli tokenizasyon
- **Dezavantaj**: UNK token sorunu, pre-tokenization bağımlılığı
- **En iyi kullanım**: Encoder modeller (BERT), classification görevleri
- **Fark**: BPE frekans kullanır, WordPiece P(mevcut|önceki) likelihood kullanır

## SentencePiece
- **Avantaj**: Raw text işler, dil bağımsız, Unigram seçeneği
- **Dezavantaj**: Daha yavaş eğitim, daha büyük model dosyası
- **En iyi kullanım**: Multilingual modeller, T5 tarzı encoder-decoder
- **Özellik**: Space'ı token olarak öğrenir → detokenizasyon kolay

## KuroNeko İçin Öneri
**Byte-Level BPE** tercih edilmeli:
1. Türkçe + kod için yeterli
2. UNK sorunu olmaz
3. HuggingFace tokenizers kütüphanesinde tam destek
4. Llama/Qwen tokenizer'ları ile uyumlu
5. 64K vocab size ile Türkçe morfolojiyi yakala
