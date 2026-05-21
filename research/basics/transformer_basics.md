# Transformer Mimarisi — KuroNeko Araştırma Notları
> Adım 1 | Tarih: 2026-05-21

## Temel Mimari

Transformer, 2017'de "Attention Is All You Need" makalesiyle Google tarafından tanıtıldı. Tekrarlayan (RNN) veya evrişimsel (CNN) katmanlar yerine tamamen attention mekanizmasına dayanır.

## Üç Ana Model Tipi

### 1. Encoder-Only (BERT tipi)
- Sadece encoder stack'i kullanır
- Bidirectional attention (her token diğer tüm token'lara bakar)
- Kullanım: Classification, embedding üretme, NER
- Örnekler: BERT, RoBERTa, DeBERTa

### 2. Decoder-Only (GPT tipi)
- Sadece decoder stack'i kullanır
- Causal/masked attention (sadece önceki token'lara bakar)
- Kullanım: Metin üretme, sohbet, kod yazma
- Örnekler: GPT-3/4, Llama, Mistral, **KuroNeko**

### 3. Encoder-Decoder (T5 tipi)
- Hem encoder hem decoder stack
- Encoder bidirectional, decoder causal
- Kullanım: Çeviri, özetleme, seq2seq
- Örnekler: T5, BART, FLAN

## KuroNeko İçin Karar: Decoder-Only

**Gerekçe:**
- Kod yazma ve sohbet için decoder-only en iyi performansı gösterir
- Daha az parametre, daha hızlı eğitim
- Llama, Mistral, Phi gibi modeller bu mimariyi kullanır
- Telefonda çalıştırma için daha uygun

## Transformer Bileşenleri

### Self-Attention Mekanizması
```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```
- Query (Q): "Ne arıyorum?"
- Key (K): "Ne sunuyorum?"
- Value (V): "Gerçek bilgi"
- d_k: Boyut (genelde 64 veya 128)

### Multi-Head Attention
- Birden fazla attention head paralel çalışır
- Her head farklı ilişkileri öğrenir
- Örnek: 12 head × 64 boyut = 768 toplam boyut

### Feed-Forward Network (FFN)
- İki lineer katman + aktivasyon (GELU veya SwiGLU)
- Genelde model boyutunun 4 katı (d_model × 4)
- Token bazında bağımsız çalışır

### Positional Encoding
- Transformer sıralama bilgisi içermez
- Sıra bilgisi eklenmeli
- Türler: Sinusoidal (orijinal), RoPE (Llama), ALiBi

### Layer Normalization
- Her katmandan sonra uygulanır
- Pre-norm (modern) veya post-norm (klasik)
- KuroNeko: **Pre-norm** (daha stabil eğitim)

### Residual Connection
- Her katmanın girişi çıkışa eklenir
- Gradient akışını iyileştirir
- Derin ağlarda kritik

## Decoder-Only Spifikasyonları

### Causal Masking
- Token i, sadece 0..i-1 token'larına bakar
- Üretme sırasında geleceği görmez
- Üçgen mask matrisi ile uygulanır

### Autoregressive Generation
- Her adımda bir token üretir
- Üretilen token girdiye eklenir
- Temperature, top-k, top-p ile kontrol
