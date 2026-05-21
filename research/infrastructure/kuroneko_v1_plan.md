# KuroNeko v1 Egitim Plani
> Adım 69 | Tarih: 2026-05-21

## On Hazirlik
1. Veri setini hazirla (100K ornek)
2. Kaggle notebook olustur
3. W&B hesabi ac
4. Google Drive bagla

## Egitim Asamalari

### Asama 1: SFT (1-2 hafta)
- Base: Llama-3.2-1B
- Veri: 100K instruction
- Epoch: 2
- Sure: ~12-18 saat (Kaggle T4)
- Cikti: kuroneko-v1-sft

### Asama 2: DPO (3-5 gun)
- Base: kuroneko-v1-sft
- Veri: 5-10K tercih pair
- Epoch: 1
- Sure: ~4-6 saat
- Cikti: kuroneko-v1-dpo

### Asama 3: Degerlendirme (1 gun)
- Benchmark: 100 soru
- Baseline karsilastirma
- Rapor olustur

## Zaman Cizelgesi
| Hafta | Gorev | Sure |
|-------|-------|------|
| 1 | Veri hazirligi | 2-3 gun |
| 1-2 | SFT egitimi | 3-5 gun |
| 2-3 | DPO egitimi | 2-3 gun |
| 3 | Degerlendirme | 1-2 gun |
| 3 | Optimizasyon (GGUF) | 1 gun |
| 4 | Test + duzeltmeler | 2-3 gun |

## Basari Kriterleri
- MMLU > 55%
- HumanEval > 35%
- TR-MMLU > 45%
- Telefonda calisir
- Token/s > 10 (ortalama telefon)
