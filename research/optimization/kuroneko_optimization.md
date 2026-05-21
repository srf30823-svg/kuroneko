# KuroNeko Optimizasyon Planı
> Adım 38 | Tarih: 2026-05-21

## Optimizasyon Yığını

### Aşama 1 (v1) — Temel
- QLoRA (4bit + LoRA) eğitim
- GGUF Q4_K_M quantization
- llama.cpp ile inference
- Flash Attention 2

### Aşama 2 (v2) — Gelişmiş
- Knowledge Distillation (teacher: CodeLlama-7B)
- Pruning (structured, %20-30)
- GGUF Q5_K_M veya Q4_K_M
- Spekülatif decoding

### Aşama 3 (v3) — Production
- ExecuTorch Android entegrasyonu
- vLLM serving
- INT8/INT4 inference quantization
- Custom CUDA kernel'ler

## Bellek Optimizasyonu
| Teknik | VRAM Tasarrufu | Kalite Kaybı |
|--------|----------------|--------------|
| QLoRA 4bit | ~60% | ~2% |
| GGUF Q4_K_M | ~70% | ~3% |
| Pruning %30 | ~30% | ~1% |
| Distillation | ~50% | ~5% |

## Hız Optimizasyonu
| Teknik | Hız Artışı |
|--------|------------|
| Flash Attention | 2-3x |
| GGUF Q4 | 2x (CPU) |
| Speculative Decoding | 2-3x |
| Batching | 5-10x throughput |
