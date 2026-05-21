# LLM Benchmark Türleri
> Adım 51 | Tarih: 2026-05-21

## Genel Beceri Benchmark'ları

### MMLU (Massive Multitask Language Understanding)
- 57 konuda çoktan seçmeli soru
- İlkokul'dan profesyonele zorluk
- Kullananlar: Tüm büyük modeller

### HellaSwag
- Cümle tamamlama
- Günlük senaryolar
- Commonsense reasoning

### ARC (AI2 Reasoning Challenge)
- İlkokul-ortaokul bilim soruları
- Kolay ve zor setler

### GSM8K
- Matematik kelime problemleri
- İlkokul seviyesi aritmetik
- Chain-of-thought gerektirir

### TruthfulQA
- Doğruluk ve hallucination ölçer
- 817 soru, 38 kategori

### WinoGrande
- Pronoun resolution
- Commonsense reasoning

## Türkçe Benchmark'lar
- TR-MMLU: Türkçe MMLU adaptasyonu
- TQuAD: Türkçe soru-cevap
- TNEWS: Türkçe haber sınıflandırma

## KuroNeko Hedefleri
| Benchmark | Hedef (1B) | Llama-3.2-1B |
|-----------|------------|--------------|
| MMLU | >55% | 56% |
| HumanEval | >35% | 32% |
| GSM8K | >40% | 42% |
| TR-MMLU | >45% | 38% |
