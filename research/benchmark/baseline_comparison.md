# Baseline Model ve Karşılaştırma
> Adım 57 | Tarih: 2026-05-21

## Baseline Modeller

### Llama-3.2-1B (Temel)
- Meta'nın 1B parametre modeli
- Genel amaçlı
- Kod: Orta, Türkçe: Zayıf

### CodeLlama-1B (Kod)
- Meta'nın kod modeli
- Python uzmanı
- Türkçe: Zayıf

### Phi-2 (Küçük)
- Microsoft'un 2.7B modeli
- Kod: İyi
- Türkçe: Zayıf

### Gemma-2B (Genel)
- Google'ın 2B modeli
- Genel amaçlı
- Türkçe: Orta

## Karşılaştırma Planı
| Model | MMLU | HumanEval | GSM8K | TR-MMLU | Kod+TR |
|-------|------|-----------|-------|---------|--------|
| Llama-3.2-1B | 56% | 32% | 42% | 38% | 25% |
| CodeLlama-1B | 45% | 38% | 35% | 30% | 30% |
| Phi-2 | 58% | 35% | 45% | 32% | 28% |
| Gemma-2B | 55% | 30% | 40% | 40% | 22% |
| **KuroNeko-1B** | **>55%** | **>35%** | **>40%** | **>45%** | **>30%** |

## Hedef
- Genel: Llama-3.2-1B ile eşit veya iyi
- Kod: CodeLlama-1B ile eşit veya iyi
- Türkçe: Tüm modelleri geçmek
- Kod+Türkçe: Rekabetsiz
