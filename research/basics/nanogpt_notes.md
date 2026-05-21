# nanoGPT (karpathy) — Mimari Analiz
> Adım 4 | Tarih: 2026-05-21

## Repo Özeti
- Yazar: Andrej Karpathy
- Amaç: Minimalist GPT-2 implementasyonu
- Boyut: ~300 satır model.py + ~300 satır train.py

## Mimari Kararlar

### 1. Basitizm
- Tek dosyada tüm model tanımı
- Gereksiz abstraction yok
- Eğitim ve hacklenme kolaylığı ön planda

### 2. Model Yapıları
- model.py: GPT model tanımı
  - GPTConfig: Hyperparameter dataclass
  - CausalSelfAttention: Multi-head causal attention
  - MLP: Feed-forward (GELU aktivasyon)
  - Block: Transformer block (norm + attention + norm + MLP)
  - GPT: Tam model (embedding + blocks + lm_head)

### 3. Eğitim
- train.py: Basit training loop
- Mixed precision (bfloat16)
- Gradient accumulation
- Cosine LR schedule with warmup
- DistributedDataParallel (DDP) desteği

### 4. Önemli Detaylar
- Pre-norm (LayerNorm her katmandan önce)
- GELU aktivasyon
- Dropout (attention, embedding, residual)
- Weight tying (embedding ve lm_head ağırlıkları paylaşılır)
- Flash Attention (PyTorch 2.0 compile ile)

## KuroNeko İçin Alınacak Dersler
1. Pre-norm tercihi (daha stabil)
2. Weight tying (parametre tasarrufu)
3. Flash Attention kullanımı (hız)
4. Mixed precision eğitim (bellek tasarrufu)
5. Gradient accumulation (efektif batch büyütme)
