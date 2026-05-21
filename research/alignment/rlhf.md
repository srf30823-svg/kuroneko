# RLHF — Reinforcement Learning from Human Feedback
> Adım 41 | Tarih: 2026-05-21

## Nedir?
İnsan geri bildirimi ile modeli hizalama
ChatGPT'nin temel tekniği

## Süreç
1. **SFT (Supervised Fine-Tuning):** Base model + instruction verisi
2. **Reward Model Eğitimi:** İnsan tercihleri ile reward model eğit
3. **RL Fine-Tuning (PPO):** Reward model ile policy optimization

## Reward Model
- İki yanıt alır (chosen, rejected)
- Hangisinin daha iyi olduğunu tahmin eder
- Bradley-Terry model: P(A>B) = σ(r(A) - r(B))

## PPO (Proximal Policy Optimization)
- Policy gradient method
- KL divergence ile orijinal modele yakınlık
- Clipping ile stabil eğitim

## Avantajları
- İnsan tercihlerine uygun çıktı
- Zararlı içerik azalır
- Yardımcı ve dürüst yanıtlar

## Dezavantajları
- Karmaşık pipeline
- Yüksek hesaplama maliyeti
- Reward hacking riski

## KuroNeko İçin
- v1'de RLHF yok (maliyet çok yüksek)
- v1'de SFT + DPO yeterli
- v2'de RLHF değerlendirilebilir
