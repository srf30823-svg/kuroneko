# W&B ile Metrik Takibi
> Adım 58 | Tarih: 2026-05-21

## Nedir?
Weights & Biases — Eğitim metriklerini izleme platformu

## Kurulum
```bash
pip install wandb
wandb login
```

## Kullanım
```python
import wandb

wandb.init(project="kuroneko", name="v1-run1")

# Eğitim sırasında
wandb.log({
    "train/loss": loss,
    "train/lr": lr,
    "eval/loss": eval_loss,
    "eval/perplexity": perplexity,
    "eval/mmlu": mmlu_score,
    "eval/humaneval": humaneval_score,
})

# Eğitim sonunda
wandb.log({
    "benchmark/mmlu": final_mmlu,
    "benchmark/humaneval": final_humaneval,
    "benchmark/tr_mmlu": final_tr_mmlu,
})
```

## Takip Edilen Metrikler
- Train loss
- Eval loss
- Perplexity
- Learning rate
- GPU memory usage
- Throughput (tokens/s)
- Benchmark skorları

## Dashboard
- Real-time grafikler
- Model karşılaştırma
- Hyperparameter sweep
- Artifact storage (model checkpoint)

## KuroNeko İçin
- Proje: "kuroneko"
- Run: "v1-run1", "v1-dpo-run1"
- Metrikler: loss, perplexity, mmlu, humaneval, tr_mmlu
