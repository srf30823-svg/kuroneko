# Instruction Tuning Dataset'leri

## İngilizce Dataset'ler
| Dataset | Boyut | Açıklama |
|---------|-------|----------|
| Alpaca | 52K | Stanford, instruction format |
| OpenOrca | 4M | Orca paper, FLAN benzeri |
| FLAN | 1.8M | Google, çoklu görev |
| Dolly | 15K | Databricks, insan etiketli |
| Self-Instruct | 82K | Self-supervised generation |
| Evol-Instruct | 52K | ZhipuAI, complexity evolution |
| Magpie | 200K | Llama-3 tabanlı sentetik |

## Türkçe Dataset'ler
| Dataset | Boyut | Açıklama |
|---------|-------|----------|
| Turkish-Alpaca | 52K | Alpaca Türkçe çeviri |
| turkish_instructions | 50K | Merve, çeşitli görevler |
| gsm8k-tr | 8K | Matematik, Türkçe |
| combined-turkish-v5 | 1M | Birleşik Türkçe |

## Sentetik Veri Stratejileri
1. **Alpaca-style**: LLM'den instruction/response üret
2. **Evol-Instruct**: Basit → karmaşık evrim
3. **Magpie**: Modelin kendi ürettiği veri
4. **Bonito**: Conditional task generation
5. **CodecLM**: Google, tailored synthetic data

## Kaynaklar
- HuggingFace datasets
- arXiv — Seed-Free Synthetic Data Generation
- Google Research — CodecLM
- GitHub wasiahmad/Awesome-LLM-Synthetic-Data
