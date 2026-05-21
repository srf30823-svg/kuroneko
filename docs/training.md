# Eğitim Dokümantasyonu

## Pipeline

### 1. Pre-training
```bash
python training/pretrain.py --config configs/pretrain_v1.yaml
```

### 2. SFT
```bash
python training/sft.py --config configs/sft_v1.yaml
```

### 3. DPO
```bash
python training/dpo.py --config configs/dpo_v1.yaml
```

## Konfigürasyonlar
- `configs/pretrain_v1.yaml` — Pre-training ayarları
- `configs/sft_v1.yaml` — SFT ayarları
- `configs/dpo_v1.yaml` — DPO ayarları

## Checkpoint Yönetimi
- Her 1000 adımda checkpoint
- Google Drive'a otomatik yedekleme
- W&B ile metrik takibi

## Kaggle Notları
- P100 16GB → batch_size=1-2, grad_accum=8-16
- FP16 (BF16 yok) → AMP aktif
- Gradient checkpointing zorunlu
- Sequence length: 1024-2048
