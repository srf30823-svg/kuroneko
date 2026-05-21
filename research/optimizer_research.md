# AdamW Optimizer — En İyi Hiperparametreler

## AdamW Hiperparametreleri
| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| lr | 3e-4 | Learning rate (2B model için) |
| beta1 | 0.9 | İlk moment |
| beta2 | 0.95 | İkinci moment (LLM'de 0.95 tercih edilir) |
| eps | 1e-8 | Sayısal kararlılık |
| weight_decay | 0.1 | L2 regularizasyonu |
| grad_clip | 1.0 | Gradient clipping |

## Learning Rate Schedule
1. **Warmup**: 1-2% of total steps (örn. 2000 step)
2. **Stable**: Warmup sonrası sabit LR
3. **Decay**: Cosine decay veya linear decay

## KuroNeko v1 İçin
```python
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=3e-4,
    betas=(0.9, 0.95),
    eps=1e-8,
    weight_decay=0.1,
)
```

## Kaynakar
- LLaMA paper
- GPT-3 paper
- Kempner Institute — Optimizer comparison
