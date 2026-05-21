# KuroNeko Proje Wiki
> Adım 84 | Tarih: 2026-05-21

# KuroNeko Wiki

## Genel Bakis
KuroNeko (KaraKedi), kod yazma ve yazilim gelistirme uzmani bir dil modelidir.
Telefonda calisir, Türkçe ve Ingilizce konusur, bagimsiz bir sistemdir.

## Mimariler
- **Model:** Decoder-only transformer, 1.1B parametre
- **Egitim:** QLoRA (4bit + LoRA)
- **Optimizasyon:** GGUF Q4_K_M, llama.cpp
- **Hizmet:** FastAPI + llama.cpp server

## Performans
| Metrik | Hedef | Durum |
|--------|-------|-------|
| MMLU | >55% | Bekleniyor |
| HumanEval | >35% | Bekleniyor |
| TR-MMLU | >45% | Bekleniyor |
| Token/s | >10 | Bekleniyor |

## Dosya Yapisi
```
kuroneko/
├── research/       # Arastirma notlari
│   ├── basics/     # LLM temelleri
│   ├── training/   # Egitim teknikleri
│   ├── data/       # Veri seti
│   ├── optimization/ # Optimizasyon
│   ├── alignment/  # Hizalama
│   ├── benchmark/  # Degerlendirme
│   └── infrastructure/ # Altyapi
├── scripts/        # Python scriptleri
├── notebooks/      # Kaggle notebook'lari
├── docs/           # Dokumantasyon
├── models/         # Model dosyalari
└── logs/           # Loglar
```

## Baglantilar
- GitHub: [kuroneko-proje]
- W&B: [kuroneko]
- HuggingFace: [kuroneko/kuroneko-v1]
