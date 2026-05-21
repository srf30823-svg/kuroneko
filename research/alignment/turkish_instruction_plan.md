# Türkçe Instruction Dataset Oluşturma
> Adım 48 | Tarih: 2026-05-21

## Kaynaklar
1. İngilizce setlerin çevirisi (Alpaca, FLAN)
2. Türkçe Wikipedia'dan QA üretimi
3. Türkçe haber metinlerinden özetleme
4. Sentetik veri (model üretsin)
5. Manuel yazım (kaliteli örnekler)

## Sentetik Üretim Pipeline
```
İngilizce instruction → Türkçe çeviri → Kalite kontrol → JSONL
```

## Kategoriler
- Kod yazma (Türkçe açıklamalı)
- Sohbet (Türkçe)
- QA (Türkçe Wikipedia)
- Özetleme (Türkçe haber)
- Çeviri (TR↔EN)
- Genel bilgi (Türkçe)

## Kalite Kontrol
- Dil kontrolü (Türkçe mi?)
- Uzunluk kontrolü
- Format kontrolü
- Manuel review (örneklem)

## Hedef
- 20K Türkçe instruction
- 5K Türkçe tercih pair (DPO için)
