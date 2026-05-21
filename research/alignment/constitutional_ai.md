# Constitutional AI
> Adım 46 | Tarih: 2026-05-21

## Nedir?
Anthropic'ın geliştirdiği hizalama yöntemi
Modelin kendi çıktılarını bir "anayasa" ile değerlendirmesi

## İki Aşama

### 1. SL-CAI (Supervised Learning)
- Model zararlı sorulara yanıt verir
- Kendi yanıtını Constitutional ilkelerle değerlendirir
- Revize edilmiş yanıt üretir
- Bu veri ile SFT yapılır

### 2. RL-CAI (RL from AI Feedback - RLAIF)
- İnsan yerine AI değerlendirmesi
- Constitutional ilkeler ile reward model
- PPO ile optimizasyon

## Constitutional İlkeler Örnekleri
- "Zararlı olmayan yanıtlar ver"
- "Yaratıcı ve faydalı ol"
- "Dürüst ve şeffaf ol"
- "Başkalarına saygı göster"

## Avantajları
- İnsan etiketi azalır
- Ölçeklenebilir
- Tutarlı

## KuroNeko İçin
- v1'de yok (maliyet)
- v2'de Türkçe constitutional ilkeler değerlendirilebilir
- Basit versiyon: System prompt ile kurallar
