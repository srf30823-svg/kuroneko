# ExecuTorch — Android Entegrasyonu
> Adım 35 | Tarih: 2026-05-21

## Nedir?
PyTorch'un mobile/edge cihazlar için runtime'ı
Android, iOS, embedded sistemlerde PyTorch modeli çalıştırır

## Özellikler
- PyTorch modelini doğrudan mobile'da çalıştırır
- Quantization desteği
- NPU, GPU, CPU delegate'leri
- Düşük gecikme

## Android Kullanımı
```kotlin
// Model yükle
val module = ExecuTorchModule.load(modelPath)

// Inference
val input = Tensor.fromBlob(data, longArrayOf(1, seqLen))
val output = module.forward(input)
```

## KuroNeko İçin
- llama.cpp yeterli olabilir (daha basit)
- ExecuTorch, PyTorch ekosistemi ile entegrasyon gerektiğinde
- İlk sürüm: llama.cpp, v2'de ExecuTorch değerlendirilebilir
