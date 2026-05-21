# Fine-tuning vs Instruction Tuning
> Adım 12 | Tarih: 2026-05-21

## Fine-tuning (İnce Ayar)
- Pre-trained modeli alır, belirli bir görev/alan için eğitir
- Veri: Alana özel labeled data
- Örnek: Tıbbi metinler üzerine fine-tuning
- Amaç: Modelin belirli alanda daha iyi performans göstermesi

## Instruction Tuning (Talimat Eğitimi)
- Modeli instruction-response çiftleri ile eğitir
- Veri: {"instruction": "...", "input": "...", "output": "..."}
- Amaç: Modelin talimatları anlaması ve uygun yanıt vermesi
- Örnek: Alpaca, FLAN, InstructGPT

## Supervised Fine-Tuning (SFT)
- Instruction tuning'in bir alt kümesi
- Labeled data ile eğitim
- İlk adım: Base model → SFT model

## Farklar
| Özellik | Fine-tuning | Instruction Tuning |
|---------|-------------|-------------------|
| Veri | Alana özel | Instruction-response |
| Amaç | Uzmanlaşma | Talimat takibi |
| Çıkış | Domain model | Chat/instruction model |
| Örnek | Tıbbi model | ChatGPT |

## KuroNeko Stratejisi
1. Base: Llama-3.2-1B (pre-trained)
2. SFT: Kod + Türkçe instruction verisi
3. DPO: Tercih hizalama (opsiyonel)
