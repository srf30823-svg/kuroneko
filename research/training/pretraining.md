# Pre-training Nedir?
> Adım 11 | Tarih: 2026-05-21

## Pre-training (Ön Eğitim)
- Modelin ham metin üzerinde dil öğrenmesi
- Hedef: Sonraki token'i tahmin etme (causal language modeling)
- Veri: Milyarlarca token (The Pile, CommonCrawl, Wikipedia, kod)
- Süre: Haftalar-aylar (büyük modellerde)
- Maliyet: Yüzbinlerce dolar (büyük modellerde)

## Pre-training Süreci
1. Veri toplama ve temizleme
2. Tokenizer eğitimi
3. Model mimarisi tanımlama
4. Eğitim (GPU cluster, haftalar)
5. Değerlendirme (perplexity, benchmark)

## Pre-training vs Fine-tuning vs Instruction Tuning
- Pre-training: Genel dil bilgisi (base model)
- Fine-tuning: Alana özel uyarlama (domain adaptation)
- Instruction Tuning: Talimat takibi (chat/instruction following)

## KuroNeko Stratejisi
- Pre-training yapmayacak (maliyet çok yüksek)
- Mevcut base model (Llama-3.2-1B) kullanılacak
- Instruction tuning + fine-tuning ile uzmanlaştırılacak
- Kod ve Türkçe alanında özel eğitim
