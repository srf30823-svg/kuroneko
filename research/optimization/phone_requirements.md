# Telefon Minimum Gereksinimler
> Adım 39 | Tarih: 2026-05-21

## KuroNeko-1B Gereksinimler

### Minimum
- RAM: 2GB (model) + 1GB (sistem) = 3GB toplam
- Storage: 1GB (Q4_K_M model)
- CPU: ARM64, 4 core
- Android: 8.0+

### Önerilen
- RAM: 4GB+ (rahat çalışma)
- Storage: 2GB (model + cache)
- CPU: Snapdragon 665 veya üstü
- Android: 10.0+

### Performans Beklentisi
| Cihaz | RAM | Token/s |
|-------|-----|---------|
| Snapdragon 888 | 8GB | ~20 |
| Snapdragon 778G | 6GB | ~15 |
| Snapdragon 665 | 4GB | ~10 |
| Snapdragon 660 | 4GB | ~8 |

## Model Boyutları
| Format | Boyut | Minimum RAM |
|--------|-------|-------------|
| F16 | 2.0GB | 3GB |
| Q8_0 | 1.1GB | 2GB |
| Q5_K_M | 0.7GB | 1.5GB |
| Q4_K_M | 0.6GB | 1.2GB |
| Q3_K_M | 0.5GB | 1.0GB |

## Termux Kurulum
```bash
pkg update && pkg upgrade
pkg install git cmake python
pip install llama-cpp-python
# Veya kaynaktan derle
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build -j4
```
