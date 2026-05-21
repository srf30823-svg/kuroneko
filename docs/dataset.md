# Veri Seti Dokümantasyonu

## Yapı
```
data/
├── raw/           # Ham veri
│   ├── turkish_wiki/
│   ├── opus_turkish/
│   ├── python_code/
│   └── js_code/
├── clean/         # Temizlenmiş veri
│   ├── pretrain_data.jsonl
│   ├── instruction/
│   └── dpo/
├── tokenizer_train.txt  # Tokenizer eğitim verisi
└── README.md
```

## Formatlar

### Pre-training (JSONL)
```json
{"text": "Metin içeriği..."}
```

### Instruction (JSONL)
```json
{"instruction": "Görev", "input": "Bağlam", "output": "Yanıt"}
```

### DPO (JSONL)
```json
{"prompt": "Soru", "chosen": "İyi yanıt", "rejected": "Kötü yanıt"}
```

## İstatistikler
- Pre-training: ~30B token
- Instruction: ~35K örnek
- DPO: ~5K çift
- Train/Val/Test: 98/1/1 split
