# Tokenizer Türleri — KuroNeko Araştırma Notları
> Adım 2 | Tarih: 2026-05-21

## Üç Ana Subword Tokenizer

### BPE (Byte-Pair Encoding)
- Frekans tabanlı, greedy birleştirme
- Kullananlar: GPT-2/3/4, Llama, Mistral
- Avantaj: Basit, hızlı, yaygın

### WordPiece
- Likelihood tabanlı, BERT için geliştirildi
- Kullananlar: BERT, ALBERT, DeBERTa
- Avantaj: Daha istatistiksel subword seçimi

### SentencePiece (Unigram LM)
- Raw text üzerinde çalışır, dil bağımsız
- Kullananlar: T5, PaLM, Llama
- Avantaj: Multilingual, byte fallback, kod için ideal

## KuroNeko Kararı: SentencePiece (Unigram LM)

Gerekçe:
1. Türkçe + İngilizce desteği (dil bağımsız)
2. Raw text — ön işleme gerektirmez, kod verisinde kritik
3. Byte fallback — bilinmeyen karakterler sorun olmaz
4. Llama uyumluluğu — weight transfer kolay

## Vocabulary Boyutu
- KuroNeko v1: 32,000 (Türkçe + kod için yeterli)
- Küçük model: 32K, Orta: 32K-65K, Büyük: 65K-128K

## Özel Tokenler
<bos>, <eos>, <pad>, <unk>, <user>, <assistant>, <system>
