# Türkçe Instruction Dataset'leri

## Mevcut Dataset'ler
| Dataset | Boyut | Açıklama |
|---------|-------|----------|
| merve/turkish_instructions | 50K | Çeşitli görevler |
| TFLai/Turkish-Alpaca | 52K | Alpaca format |
| bezir/turkish_exam_instructions | 10K | Sınav soruları |
| bezir/gsm8k-tr | 8K | Matematik |
| yusufbaykaloglu/Turkish-STEM-DPO | 5K | STEM DPO |

## Sentetik Üretim Stratejisi
1. İngilizce instruction'ları Türkçe'ye çevir
2. Türkçe soru-cevap çiftleri oluştur
3. Kod yazma görevleri ekle
4. Mantık yürütme görevleri ekle
5. Çok turlu konuşma senaryoları

## Kaynaklar
- HuggingFace turkish datasets
- Bridging the Bosphorus paper
