# ByteLevel BPE Avantajları

## Neden Byte-Level?

### 1. UNK Token Yok
- 256 byte base vocab → her Unicode karakter temsil edilebilir
- Türkçe karakterler (ç, ğ, ı, ö, ş, ü) sorunsuz
- Emoji, matematiksel semboller, CJK karakterler → hepsi temsil edilebilir

### 2. Dil Bağımsız
- Ön segmentasyon gerektirmez
- Türkçe, Çince, Arapça → hepsi aynı base'den başlar
- Morfolojik analiz gerekmez

### 3. Kod İçin İdeal
- Her karakter ASCII byte olarak temsil edilir
- Özel karakterler (`{`, `}`, `->`, `=>`) sorunsuz
- Unicode identifier'lar (π, α) çalışır

### 4. Kompakt
- Base vocab = 256 (karakter-level ~100K)
- Merge kuralları ile büyük parçalar öğrenilir
- Bellek verimli

## Byte-Level vs Character-Level
| Özellik | Character-Level | Byte-Level |
|---------|----------------|------------|
| Base vocab | ~100K | 256 |
| UNK | Olabilir | İmkansız |
| Türkçe | İyi | İyi |
| Unicode | Sınırlı | Tam |
| Sequence uzunluğu | Kısa | ~4x uzun |
| Bellek | Büyük | Küçük |

## Tradeoff
- Byte-level daha uzun sequence üretir (ortalama 4x)
- Ama UNK olmaması ve dil bağımsızlığı avantajı çok büyük
- Modern LLM'lerin tamamı byte-level kullanır (Llama, Gemma, Qwen)

## KuroNeko İçin
Byte-Level BPE kesinlikle tercih edilmeli.
