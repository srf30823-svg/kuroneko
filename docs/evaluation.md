# Değerlendirme Dokümantasyonu

## Benchmark'lar

### Türkçe
- `turkish_bench.py` — Türkçe dil bilgisi, anlama, üretme
- `turkish_mmlu` — MMLU Türkçe çeviri

### Kod
- `code_bench.py` — HumanEval benzeri
- Python, JavaScript, Bash

### Genel
- `run_benchmarks.py` — Tüm benchmark'ları çalıştır
- `perplexity.py` — Perplexity hesaplama

## Metrikler
| Metrik | Açıklama |
|--------|----------|
| Perplexity | Modelin metin tahmin kalitesi |
| Accuracy | Doğru cevap oranı |
| BLEU | Metin benzerliği |
| ROUGE | Özetleme kalitesi |
| Pass@K | Kod üretme başarısı |

## Kullanım
```bash
python kuroneko/eval/run_benchmarks.py --model models/kuroneko-v1/
python kuroneko/eval/perplexity.py --model models/kuroneko-v1/ --data data/test/
```
