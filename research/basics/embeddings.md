# Embedding ve Positional Encoding
> Adım 5 | Tarih: 2026-05-21

## Token Embedding
- Her token ID, embedding matrisinden d_model boyutlu bir vektör alır
- Embedding matrisi: [vocab_size × d_model]
- Eğitim sırasında öğrenilir
- Weight tying: Embedding ve output projection matrisi paylaşılır (parametre tasarrufu)

## Positional Encoding Türleri

### Sinusoidal (Orijinal Transformer)
- Sabit, öğrenmez
- sin/cos fonksiyonları ile pozisyon bilgisi
- Dezavantaj: Uzun context desteği zayıf

### Learned Positional Embedding
- Her pozisyon için öğrenilen vektör
- GPT-2'de kullanıldı
- Dezavantaj: Eğitim uzunluğundan fazla sequence'e genişleyemez

### RoPE (Rotary Positional Encoding)
- Q ve K vektörlerini rotation ile döndürür
- Relative position bilgisi içerir
- Kullananlar: Llama, Mistral, Phi, Gemma
- Avantaj: Uzun context, extrapolation
- **KuroNeko tercihi: RoPE**

### ALiBi (Attention with Linear Biases)
- Attention skorlarına mesafe bazlı bias ekler
- Kullananlar: BLOOM
- Avantaj: Basit, uzun context

## KuroNeko Kararı: RoPE
- Llama uyumluluğu (weight transfer)
- Uzun context desteği
- Türkçe + kod için yeterli
