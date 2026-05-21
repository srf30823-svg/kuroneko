# DPO — Direct Preference Optimization
> Adım 42 | Tarih: 2026-05-21

## Nedir?
RLHF'in basitleştirilmiş hali
Reward model ve RL olmadan doğrudan tercih optimizasyonu

## RLHF vs DPO
| Özellik | RLHF | DPO |
|---------|------|-----|
| Reward Model | Gerekli | Gerekli değil |
| RL Algoritması | PPO | Yok |
| Karmaşıklık | Yüksek | Düşük |
| Stabilite | Düşük | Yüksek |
| Maliyet | Yüksek | Düşük |

## Nasıl Çalışır?
- Preference pairs (chosen, rejected) ile doğrudan eğitim
- Implicit reward model içinde tanımlı
- Loss: -log(σ(β * (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x))))

## Avantajları
- Basit implementasyon
- Stabil eğitim
- Daha az hiperparametre
- Daha az hesaplama

## KuroNeko İçin
- **v1'de DPO kullanılacak** (SFT sonrası)
- Tercih verisi: 5-10K chosen/rejected pair
- Türkçe + İngilizce tercih verisi
