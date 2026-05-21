# BPE Algoritması — Derinlemesine Araştırma

## Tarihçe
BPE (Byte-Pair Encoding) ilk olarak 1994'te Philip Gage tarafından veri sıkıştırma algoritması olarak önerildi.
2015'te Sennrich vd. makalesi "Neural Machine Translation of Rare Words with Subword Units" ile
NLP alanına adapte edildi. GPT-2 (2019) ile byte-level BPE popüler oldu ve Llama, Gemma, Qwen
gibi modern LLM'lerin standart tokenizasyon yöntemi haline geldi.

## Algoritma Detayı

### Eğitim Aşaması
1. **Pre-tokenization**: Metin kelime/boşluk bazında bölünür
2. **Base vocabulary**: Her karakter (veya byte) ayrı token olarak başlatılır
3. **Frekans sayımı**: Komşu token çiftlerinin frekansı hesaplanır
4. **Merge**: En sık görülen çipte birleştirilir → yeni token olarak eklenir
5. **Tekrar**: Hedefe (vocab_size) ulaşana kadar 3-4 tekrarlanır

### Tokenizasyon (Çıkarım)
1. Metin karaktere/byte'a bölünür
2. Öğrenilen merge kuralları büyükten küçüğe uygulanır
3. Her kelime, öğrenilmiş alt kelime birimlerine ayrılır

## Avantajları
- **UNK yok (Byte-level)**: 256 byte base vocab → her metin tokenizasyonu mümkün
- **Dil bağımsız**: Ön segmentasyon gerektirmez
- **Basit ve hızlı**: O(n) tokenizasyon karmaşıklığı
- **Sıkıştırma verimlisi**: Sık kullanılan kalıplar kısa token'lara dönüşür
- **Vocab size kontrolü**: İstenilen boyuta kadar öğrenilebilir

## Dezavantajları
- **Anlamsal bütünlük yok**: Morfolojik olarak anlamlı parçaları görmez
- **Agglutinatif dillerde sorunlu**: Türkçe gibi dillerde ek patlaması olur
  - Örnek: "çekosyalılaştıramadıklarımızdan" → 8-10 token
- **Kod tokenizasyonu zayıf**: Girinti, özel karakterler için optimize değil
- **Greedy matching**: En uzun eşleşme her zaman optimal değil
- **Cross-lingual verimsizlik**: Farklı diller farklı merge kuralları öğrenir

## Byte-Level BPE vs Character-Level BPE
| Özellik | Character-Level | Byte-Level |
|---------|----------------|------------|
| Base vocab | ~100K karakter | 256 byte |
| UNK token | Olabilir | İmkansız |
| Unicode desteği | Sınırlı | Tam |
| Token/word oranı | Daha yüksek | Daha düşük |
| Kullanılan modeller | GPT-2 (ilk) | Llama, Gemma, Qwen |

## Güncel En İyi Pratikler
1. **Byte-level BPE** tercih edilir (UNK olmaması için)
2. **Pre-tokenization** whitespace + punctuation bazlı olmalı
3. **Normalizasyun** NFC Unicode normalizasyonu önerilir
4. **Vocab size** 32K-128K arası (dil ve kullanım senaryosuna göre)
5. **Özel tokenlar** model görevine göre eklenir

## Kaynaklar
- Sennrich et al. (2016) — Neural Machine Translation of Rare Words
- Radford et al. (2019) — GPT-2 Paper
- HuggingFace Tokenizers Documentation
- Sebastian Raschka — BPE from Scratch (2025)
