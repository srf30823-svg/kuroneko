# Attention Mekanizması — Derinlemesine
> Adım 6 | Tarih: 2026-05-21

## Scaled Dot-Product Attention
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V

- Q (Query): "Ne arıyorum?" — d_k boyutlu
- K (Key): "Ne sunuyorum?" — d_k boyutlu
- V (Value): "Gerçek bilgi" — d_v boyutlu
- sqrt(d_k): Scaling factor, gradient akışını iyileştirir

## Multi-Head Attention
- h adet attention head paralel çalışır
- Her head: d_k = d_model / h boyutunda
- Farklı head'ler farklı ilişkileri öğrenir:
  - Head 1: Sözdizimsel ilişkiler
  - Head 2: Anlamsal yakınlık
  - Head 3: Uzun mesafe bağımlılıkları
  - Head 4: Pozisyonel desenler
- Çıkış: Concat(head_1, ..., head_h) * W_O

## Causal (Masked) Attention
- Decoder-only modellerde kullanılır
- Token i, sadece 0..i-1 token'larına bakar
- Üçgen mask matrisi:
  [[1, 0, 0, 0],
   [1, 1, 0, 0],
   [1, 1, 1, 0],
   [1, 1, 1, 1]]
- Gelecek token'ların bilgisini engeller

## Flash Attention
- Bellek verimli attention implementasyonu
- O(N) bellek yerine O(sqrt(N))
- Hız artışı: 2-4x
- PyTorch 2.0 compile ile otomatik
- KuroNeko: Kullanılacak (varsa)

## Grouped Query Attention (GQA)
- Multi-Head'den farklı: Key ve Value head'leri paylaşılır
- MHA: h query, h key, h value head
- GQA: h query, g key, value head (g < h)
- KV cache boyutunu küçültür
- Kullananlar: Llama 3, Mistral
- KuroNeko: GQA kullanılacak (bellek tasarrufu)
