# Kod Veri Seti Kaynakları
> Adım 24 | Tarih: 2026-05-21

## HuggingFace Veri Setleri
- **codeparrot/github-code** — GitHub'dan 115M kod dosyası
- **bigcode/starcoderdata** — StarCoder için 250GB kod
- **codeparrot/apps** — Programlama yarışması problemleri
- **mbpp** — Mostly Basic Python Problems (1K problem)
- **humaneval** — OpenAI HumanEval (164 problem)
- **code_search_net** — 6 dilde kod arama
- **the-stack** — 6TB GitHub kodu (BigCode)

## GitHub Kaynakları
- GitHub API ile repo tarama
- Python, JavaScript, Bash dosyaları
- README, dokümantasyon
- Issue ve PR'lar (hata ayıklama için)

## Sentetik Veri Üretimi
- Mevcut modelden kod üretme
- Instruction çiftleri üretme
- Hata enjeksiyonu (debug verisi için)
- Çeviri ile Türkçe veri üretme

## KuroNeko Kod Veri Planı
1. **GitHub Python:** 10K örnek (kaliteli repo'lardan)
2. **GitHub JS:** 5K örnek
3. **GitHub Bash:** 3K örnek
4. **MBPP + HumanEval:** 1K örnek
5. **Sentetik:** 10K örnek (model üretsin)
6. **Debug verisi:** 5K örnek (hata enjeksiyonu)
7. **Toplam:** ~34K kod örneği
