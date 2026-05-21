# Egitim Izleme Dashboard
> Adım 65 | Tarih: 2026-05-21

## W&B Dashboard Metrikleri

### Egitim Metrikleri
- train/loss: Egitim kaybi
- train/learning_rate: Ogrenme orani
- train/grad_norm: Gradient normu
- train/step: Adim sayisi

### Degerlendirme Metrikleri
- eval/loss: Dogrulama kaybi
- eval/perplexity: Perplexity

### Sistem Metrikleri
- system/gpu_memory: GPU bellek kullanimi
- system/gpu_utilization: GPU kullanim orani
- system/throughput: Saniyedeki token sayisi

### Benchmark Metrikleri
- benchmark/mmlu: MMLU skoru
- benchmark/humaneval: HumanEval skoru
- benchmark/tr_mmlu: Turkce MMLU

## Dashboard Olusturma
```python
import wandb

wandb.init(project="kuroneko", name="v1-run1", config={
    "model": "Llama-3.2-1B",
    "lora_r": 16,
    "batch_size": 4,
    "learning_rate": 2e-4,
})

# Loglama
wandb.log({
    "train/loss": loss,
    "eval/loss": eval_loss,
    "system/gpu_memory": gpu_mem,
})
```

## Panel Yapisi
1. Loss grafigi (train + eval)
2. Learning rate grafigi
3. GPU kullanimi
4. Benchmark skorlari tablosu
5. Model karsilastirma
