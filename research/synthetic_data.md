# Sentetik Veri Üretme Stratejileri

## Stratejiler

### 1. Alpaca-Style Generation
- Seed instruction'lar ile LLM'den yanıt üret
- Self-Instruct yöntemi
- Avantaj: Basit, hızlı
- Dezavantaj: Çeşitlik sınırlı

### 2. Evol-Instruct
- Basit instruction'ları karmaşık hale getir
- Derinlik evrimi: Detay ekle
- Genişlik evrimi: Kısıtlama ekle
- Avantaj: Yüksek kalite, çeşitli
- Dezavantaj: Yavaş, LLM bağımlı

### 3. Magpie
- Modelin kendi ürettiği veri
- Instruction-backtranslation
- Avantaj: Model-specific, yüksek kalite
- Dezavantaj: Büyük model gerektirir

### 4. Bonito
- Conditional task generation
- Veriden task çıkarımı
- Avantaj: Veri-driven
- Dezavantaj: Fine-tuning gerektirir

### 5. CodecLM (Google)
- Encode-decode synthetic data
- Task-specific tailoring
- Avantaj: En yüksek kalite
- Dezavantaj: Karmaşık pipeline

## KuroNeko Stratejisi
1. **Aşama 1**: Alpaca-style (5K örnek)
2. **Aşama 2**: Evol-Instruct (10K örnek)
3. **Aşama 3**: Türkçe çeviri + sentetik (10K örnek)
4. **Aşama 4**: Kod instruction (10K örnek)
5. **Toplam**: ~35K instruction örneği

## Kaynaklar
- arXiv — Seed-Free Synthetic Data Generation
- Google Research — CodecLM
- GitHub wasiahmad/Awesome-LLM-Synthetic-Data
- Scale AI — Synthetic Data Strategies
