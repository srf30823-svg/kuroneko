# KuroNeko Egitim Rehberi
> Adım 85 | Tarih: 2026-05-21

## On Kosullar
- Kaggle hesabi
- W&B hesabi
- Google Drive (yedekleme)
- Veri seti hazir (100K ornek)

## Adim 1: Veri Hazirligi
```bash
# Veri setini indir/hazirla
python scripts/collect_data.py data/kuroneko_train.jsonl --synthetic
python scripts/dataset_stats.py data/kuroneko_train.jsonl
```

## Adim 2: Kaggle Notebook
1. Kaggle'da yeni notebook olustur
2. GPU: T4 sec
3. Veri setini yukle
4. notebook/kuroneko_train.ipynb calistir

## Adim 3: Egitim
```python
# SFT
from trl import SFTTrainer
trainer = SFTTrainer(model=model, train_dataset=dataset, args=args)
trainer.train()

# DPO
from trl import DPOTrainer
dpo_trainer = DPOTrainer(model=model, ref_model=ref, args=dpo_args)
dpo_trainer.train()
```

## Adim 4: Degerlendirme
```bash
python scripts/run_benchmark.py models/kuroneko-v1 data/benchmark.jsonl
python scripts/compare_models.py results/baseline.json results/kuroneko.json
```

## Adim 5: Optimizasyon
```bash
python scripts/convert_to_gguf.py models/kuroneko-v1 models/kuroneko-v1-q4 q4_k_m
```

## Adim 6: Dagitim
- GGUF modelini telefona indir
- llama.cpp ile calistir
- FastAPI server olarak calistir

## Sorun Giderme
- OOM: Batch size dusur
- Loss NaN: LR dusur
- Reset: Checkpoint'ten devam
