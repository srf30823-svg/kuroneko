# LLM Veri Seti Türleri
> Adım 21 | Tarih: 2026-05-21

## Pre-training Veri
- Ham metin: Web sayfaları, kitaplar, makaleler
- Boyut: Milyarlarca token (100GB+)
- Kaynak: CommonCrawl, The Pile, Wikipedia, GitHub
- Format: Düz metin, JSONL

## Instruction Veri
- Talimat-yanıt çiftleri
- Format: {"instruction": "...", "input": "...", "output": "..."}
- Boyut: 10K-1M örnek
- Kaynak: Alpaca, FLAN, OpenAssistant, özel üretim

## Preference (DPO) Veri
- İki yanıt arasında tercih
- Format: {"prompt": "...", "chosen": "...", "rejected": "..."}
- Boyut: 10K-500K örnek
- Kaynak: HH-RLHF, UltraFeedback, özel üretim

## Kod Veri
- Kaynak kod, dokümantasyon, hata ayıklama
- Format: {"instruction": "...", "code": "...", "language": "..."}
- Kaynak: GitHub, StackOverflow, CodeSearchNet

## KuroNeko Veri Stratejisi
1. Instruction: Kod yazma, hata bulma, Türkçe sohbet (50K)
2. Kod: Python, JS, Bash, JSON, YAML (30K)
3. Türkçe: Sohbet, soru-cevap, özetleme (20K)
4. Toplam: ~100K instruction örnek
