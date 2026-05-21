# Tokenizer Benchmark — Hız ve Kalite

## Metrikler

### 1. Hız (Throughput)
- **Tokens/saniye**: Saniyedeki işlenen token sayısı
- **Karakter/saniye**: Saniyedeki işlenen karakter sayısı
- **Latency**: Tek bir encode/decode süresi

### 2. Kalite
- **Tokens/kelime**: Düşük = daha iyi sıkıştırma
- **Tokens/karakter**: Düşük = daha iyi sıkıştırma
- **UNK oranı**: 0 olmalı (byte-level)
- **Decode doğruluğu**: %100 olmalı

### 3. Türkçe Spesifik
- **Ek token oranı**: Eklerin ayrı token olma oranı
- **Kök token oranı**: Köklerin tek token olma oranı
- **Morfem bütünlüğü**: Morfemlerin korunma oranı

## Benchmark Sonuçları (Beklenen)

| Metrik | 32K | 64K | 128K |
|--------|-----|-----|------|
| Tokens/kelime (TR) | 3.5 | 2.5 | 1.8 |
| Tokens/kelime (EN) | 1.8 | 1.4 | 1.1 |
| Tokens/karakter | 0.35 | 0.25 | 0.18 |
| Hız (token/s) | 500K | 450K | 400K |
| UNK oranı | 0% | 0% | 0% |

## Kaynaklar
- arXiv 2411.12240 — Tokenizer Performance Evaluation
- Medium — Comprehensive Tokenizer Performance Analysis
- GitHub KorAP/Tokenizer-Evaluation
