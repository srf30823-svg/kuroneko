# Bellek Optimizasyonu Teknikleri

## Teknikler

### 1. Gradient Checkpointing
- **Tasarruf**: ~40% activation belleği
- **Maliyet**: ~30% daha yavaş eğitim
- **Kullanım**: `model.gradient_checkpointing_enable()`

### 2. Mixed Precision (FP16/BF16)
- **Tasarruf**: ~50% model + gradient belleği
- **Maliyet**: Minimal
- **Kullanım**: `torch.cuda.amp.autocast()`

### 3. Gradient Accumulation
- **Tasarruf**: Effective batch size artırımı
- **Maliyet**: Daha fazla step
- **Kullanım**: Loss'u accumulation steps'e böl

### 4. CPU Offloading
- **Tasarruf**: GPU belleği boşaltma
- **Maliyet**: CPU-GPU transfer
- **Kullanım**: DeepSpeed ZeRO

### 5. Flash Attention
- **Tasarruf**: O(N) → O(1) attention map
- **Maliyet**: Yok
- **Kullanım**: `flash_attn` kütüphanesi

## KuroNeko v1 Bellek Planı (P100 16GB)
| Teknik | Bellek |
|--------|--------|
| Model (FP16) | 4GB |
| Gradients | 4GB |
| Optimizer (AdamW) | 8GB |
| Activations | 2GB |
| **Toplam (optimize)** | **~12GB** |
| **Toplam (ham)** | **~18GB** |

## Kaynaklar
- PyTorch memory management
- Gradient checkpointing paper
- Flash Attention paper
