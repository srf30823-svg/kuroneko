# Vocab Size Seçimi — 32K vs 64K vs 128K Tradeoff'ları

## Teori

### Chinchilla Vocabulary Scaling
- arXiv 2407.13623: "Scaling Laws with Vocabulary"
- Optimal vocab size ≈ N^0.45 (N = model parametre sayısı)
- 2B model için: 2000^0.45 ≈ 64K → **64K optimal**

### Tradeoff Analizi

| Vocab Size | Embedding Boyutu | Türkçe Kalite | Kod Kalite | Bellek | Hız |
|-----------|-----------------|---------------|------------|--------|-----|
| 32K | 2048×32K = 67MB | Zayıf (çok token) | Zayıf | Küçük | En hızlı |
| 64K | 2048×64K = 134MB | İyi | İyi | Orta | Hızlı |
| 128K | 2048×128K = 268MB | Çok iyi | Çok iyi | Büyük | Orta |
| 256K | 2048×256K = 536MB | En iyi | En iyi | Çok büyük | Yavaş |

### Türkçe İçin Analiz
- **32K**: Türkçe kelimeler çok parçalanır → ortalama 4-5 token/kelime
- **64K**: Dengeli → ortalama 2-3 token/kelime
- **128K**: İyi → ortalama 1.5-2 token/kelime
- **256K**: Gereksiz → marjinal iyileşme, 2x bellek

### Kod İçin Analiz
- **32K**: Operatörler ve identifier'lar parçalanır
- **64K**: Yeterli → çoğu keyword tek token
- **128K**: İyi → uzun identifier'lar tek token

## Optimal Seçim: 64K

**Gerekçe**:
1. Chinchilla scaling law'e göre 2B model için optimal
2. Türkçe + kod için yeterli coverage
3. Embedding boyutu makul (134MB)
4. Inference hızı yüksek
5. Llama 3 (128K) ile Qwen (152K) arasında dengeli

## İleriye Dönük
- v2 modelde 128K'ya genişletilebilir
- MoE ile vocab paylaşımı düşünülebilir

## Kaynaklar
- arXiv 2407.13623 — Scaling Laws with Vocabulary
- Reddit r/MachineLearning — Vocabulary size discussion
- Salvatore Raieli — Vocabulary Size in LLM Scaling
