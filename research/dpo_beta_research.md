# DPO Beta Parametresi Araştırması

## Beta Nedir?
- DPO'daki sıcaklık parametresi
- Reference model ile policy model arasındaki farkı kontrol eder
- **Düşük beta (0.01-0.1)**: Reference'dan uzaklaşabilir, yaratıcı
- **Yüksek beta (0.5-1.0)**: Reference'a yakın kalır, konservatif

## Önerilen Değerler
| Senaryo | Beta | Açıklama |
|---------|------|----------|
| Conservative | 0.5 | Reference'a çok yakın |
| Balanced | 0.1 | Dengeli (önerilen) |
| Creative | 0.05 | Daha yaratıcı |
| Minimal | 0.01 | Reference'dan çok uzak |

## KuroNeko v1 İçin
**Beta = 0.1** — Dengeli, reference model'e yakın ama iyileştirme var

## Kaynaklar
- Rafailov et al. (2023) — Direct Preference Optimization
- HuggingFace TRL DPO documentation
