# LoRA ve QLoRA — Derinlemesine
> Adım 13 | Tarih: 2026-05-21

## LoRA (Low-Rank Adaptation)
- Tam fine-tuning yerine, ağırlık matrislerine düşük rank'lı matrisler ekler
- W = W0 + A * B (A: d×r, B: r×d, r << d)
- r (rank): 4, 8, 16, 32, 64 (küçük = az parametre)
- Sadece A ve B matrisleri eğitilir, W0 sabit kalır
- Bellek tasarrufu: ~10x daha az parametre
- Hız: Tam fine-tuning'e yakın

## QLoRA (Quantized LoRA)
- Model ağırlıkları 4-bit'e kuantize edilir (NF4 format)
- LoRA adapter'ları üzerinde eğitim yapılır
- Bellek tasarrufu: ~3x daha az VRAM
- 7B model: ~14GB → ~6GB VRAM
- Kalite kaybı: Minimal (doğru kullanıldığında)

## LoRA Parametreleri
- r (rank): 16 (KuroNeko için önerilen)
- alpha: 32 (r * 2, scaling factor)
- target_modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- dropout: 0.05

## KuroNeko LoRA Konfigürasyonu
```python
lora_config = {
    "r": 16,
    "lora_alpha": 32,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
    "lora_dropout": 0.05,
    "bias": "none",
    "task_type": "CAUSAL_LM"
}
```

## Bellek Karşılaştırması (1B model)
| Yöntem | VRAM | Eğitilebilir Parametre |
|--------|------|------------------------|
| Full fine-tuning | ~24GB | 1.1B |
| LoRA (r=16) | ~12GB | ~8M |
| QLoRA (4bit) | ~6GB | ~8M |
