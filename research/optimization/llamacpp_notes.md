# llama.cpp Analizi
> Adım 34 | Tarih: 2026-05-21

## Nedir?
LLM'leri CPU üzerinde çalıştırmak için optimize edilmiş C/C++ kütüphanesi

## Özellikler
- CPU inference (GPU olmadan çalışır)
- Quantization desteği (Q2-Q8)
- Metal (macOS), CUDA, Vulkan backend
- Server modu (OpenAI API uyumlu)
- Embedding üretimi

## Termux'ta Kurulum
```bash
pkg install cmake git
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build -j4

# Model çalıştırma
./build/bin/llama-cli -m model-q4_k_m.gguf -p "Merhaba" -n 200
```

## Performans (Android/Termux)
- 1B model Q4_K_M: ~15-20 token/s (Snapdragon 888)
- 1B model Q4_K_M: ~8-12 token/s (Snapdragon 665)
- RAM: ~1GB (1B Q4_K_M)

## Server Modu
```bash
./build/bin/llama-server -m model.gguf --host 0.0.0.0 --port 8080
# OpenAI API uyumlu endpoint: http://localhost:8080/v1/chat/completions
```

## KuroNeko İçin
- llama.cpp Termux'ta kurulacak
- Q4_K_M formatı kullanılacak
- Server modu ile API sağlanacak
