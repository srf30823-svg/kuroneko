# Veri Pipeline Dokümantasyonu

## Pipeline Aşamaları

### 1. Toplama
```bash
# Türkçe Wikipedia
python scripts/collect_data.py --source wikipedia --lang tr

# Common Crawl
python scripts/collect_data.py --source commoncrawl --lang tr

# Kod
python scripts/collect_data.py --source the-stack --lang python
```

### 2. Temizleme
```bash
python scripts/clean_text.py --input raw.txt --output clean.txt
```

### 3. Dedup
```bash
python scripts/dedup.py --input clean.txt --output deduped.txt --threshold 0.8
```

### 4. Kalite Kontrolü
```bash
python scripts/quality_check.py --input deduped.txt --output stats.json
```

### 5. Split
```bash
python scripts/split_data.py --input data.jsonl --train 0.98 --val 0.01 --test 0.01
```

## Veri Formatı
- JSONL (JSON Lines)
- Her satır bir örnek
- UTF-8 encoding
- SHA-256 hash ile dedup
