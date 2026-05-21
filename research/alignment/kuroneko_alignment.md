# KuroNeko Hizalama Stratejisi
> Adım 47 | Tarih: 2026-05-21

## Aşama 1: SFT (v1)
- Base model: Llama-3.2-1B
- Veri: 100K instruction örnek
- Format: ChatML
- Yöntem: QLoRA (4bit + LoRA)

## Aşama 2: DPO (v1.5)
- SFT modeli base olarak al
- Tercih verisi: 5-10K pair
- Beta: 0.1
- Yöntem: QLoRA + DPO

## Aşama 3: RLHF (v2 - opsiyonel)
- Reward model eğitimi
- PPO ile optimizasyon
- Constitutional AI ilkeleri

## Hizalama İlkeleri
1. **Güvenlik:** Zararlı, yasaklı içerik üretmez
2. **Doğruluk:** Bilgi yanlışı minimize edilir
3. **Yardımcılık:** Kullanıcıya faydalı yanıtlar
4. **Dürüstlük:** Bilmediğini söyler
5. **Türkçe:** Türkçe sorulara Türkçe yanıt

## Güvenlik Önlemleri
- System prompt ile sınırlar
- Zararlı talimat filtresi
- Kod execution sandboxing
- Output length limiti
