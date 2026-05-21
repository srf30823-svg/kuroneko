# LLMs-from-scratch (rasbt) — Kavram Analizi
> Adım 3 | Tarih: 2026-05-21

## Repo Özeti
- Yazar: Sebastian Raschka
- Amaç: ChatGPT benzeri LLM'yi sıfırdan Python/PyTorch ile inşa etme
- Kitap: "Build a Large Language Model (From Scratch)"

## Ana Kavramlar

### 1. Text Embedding Pipeline
- Raw text → Tokenization → Token IDs → Embedding vectors
- Her token ID, embedding matrisinden bir vektör olarak temsil edilir
- Embedding boyutu (d_model): Modelin temel boyut parametresi

### 2. Attention Mekanizması
- Scaled Dot-Product Attention: Attention(Q,K,V) = softmax(QK^T/sqrt(d_k)) * V
- Multi-Head: Birden fazla attention head paralel çalışır
- Causal Attention: Decoder'da gelecek token'lar maskelenir

### 3. GPT Mimarisi
- Decoder-only transformer
- Token embedding + positional embedding
- N x transformer block (attention + FFN + layer norm + residual)
- Lineer çıkış katmanı (vocab boyutunda)

### 4. Eğitim Süreci
- Language modeling loss: Cross-entropy (sonraki token tahmini)
- Dataset: OpenWebText, The Pile gibi büyük metin koleksiyonları
- Optimizer: AdamW
- Learning rate scheduling: Cosine with warmup

### 5. Metin Üretme
- Greedy decoding: En yüksek olasılıklı token
- Temperature scaling: Rastgelelik kontrolü
- Top-k sampling: En olası k token arasından seçim
- Top-p (nucleus) sampling: Kumulatif olasılık eşiği

## KuroNeko İçin Alınacak Dersler
1. Decoder-only mimari tercihi doğrulandı
2. Embedding + positional encoding pipeline net
3. Eğitim loss ve optimizer seçimi (AdamW + cosine)
4. Üretme stratejileri (top-p + temperature)
