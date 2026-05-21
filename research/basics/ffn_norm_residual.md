# Feed-Forward, Layer Norm, Residual Connection
> Adım 7 | Tarih: 2026-05-21

## Feed-Forward Network (FFN)
- İki lineer katman + aktivasyon
- Boyut: d_model -> d_ff -> d_model
- d_ff genelde d_model * 4 (örn: 768 -> 3072 -> 768)
- Aktivasyon türleri:
  - ReLU: Basit, hızlı
  - GELU: GPT-2, BERT'te kullanılır
  - SwiGLU: Llama, Mistral'te kullanılır (daha iyi)
- **KuroNeko: SwiGLU** (modern standart)

## Layer Normalization
- Feature boyutuna göre normalizasyon
- Batch norm'dan farklı: Batch boyutu değil, feature boyutu
- Pre-norm (modern): Norm -> Sublayer (daha stabil)
- Post-norm (klasik): Sublayer -> Norm
- **KuroNeko: Pre-norm** (daha stabil eğitim)

## Residual (Skip) Connection
- Her sublayer'ın girişi çıkışa eklenir: LayerNorm(x + Sublayer(x))
- Gradient akışını iyileştirir
- Derin ağlarda vanishing gradient önler
- Bilgi kaybını azaltır

## KuroNeko Transformer Block
```
x = x + Attention(LayerNorm(x))
x = x + FFN(LayerNorm(x))
```
- Pre-norm + residual her iki sublayer'da
- SwiGLU aktivasyon
- GQA attention
- RoPE positional encoding
