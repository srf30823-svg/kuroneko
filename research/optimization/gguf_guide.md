# GGUF Formatı
> Adım 33 | Tarih: 2026-05-21

## Nedir?
llama.cpp için optimize edilmiş model formatı
GPTQ, AWQ, GGML'in halefi

## Quantization Türleri

| Format | Boyut (1B model) | Kalite |
|--------|------------------|--------|
| F16 | ~2GB | En iyi |
| Q8_0 | ~1.1GB | Çok iyi |
| Q5_K_M | ~700MB | İyi |
| Q4_K_M | ~600MB | İyi (önerilen) |
| Q3_K_M | ~500MB | Orta |
| Q2_K | ~400MB | Düşük |

## Oluşturma
```bash
# llama.cpp ile dönüştürme
python convert.py model_path --outtype f16
./quantize model.gguf model-q4_k_m.gguf Q4_K_M

# Unsloth ile doğrudan
model.save_pretrained_gguf("output", tokenizer, quantization_method="q4_k_m")
```

## KuroNeko İçin
- **Q4_K_M**: Telefon için en iyi kalite/boyut dengesi
- **Q5_K_M**: Daha iyi kalite, biraz daha büyük
- İlk sürüm: Q4_K_M
