# Preference Dataset'leri — DPO İçin

## Mevcut Dataset'ler
| Dataset | Boyut | Açıklama |
|---------|-------|----------|
| UltraFeedback | 64K | OpenAI, çoklu kriter |
| HH-RLHF | 170K | Anthropic, helpful/harmless |
| StackExchange Preferences | 330K | StackOverflow tercihler |
| SHP | 380K | Reddit tercihler |
| Nectar | 140K | Çoklu LLM karşılaştırma |

## Türkçe Preference
| Dataset | Boyut | Açıklama |
|---------|-------|----------|
| Turkish-STEM-DPO | 5K | STEM alanı |
| Combined Turkish DPO | 10K | Çeşitli |

## Sentetik Üretim
1. Aynı prompt'a farklı yanıtlar üret
2. Kalite sıralaması yap (LLM-as-judge)
3. Chosen/rejected çiftleri oluştur

## Kaynaklar
- HuggingFace preference datasets
- DPO paper (Rafailov et al. 2023)
- TRL DPO documentation
