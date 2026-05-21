# Instruction Tuning Veri Formatları
> Adım 43 | Tarih: 2026-05-21

## Alpaca Format
```json
{
  "instruction": "İngilizce'ye çevir",
  "input": "Merhaba dünya",
  "output": "Hello world"
}
```

## ShareGPT Format
```json
{
  "conversations": [
    {"from": "human", "value": "Merhaba"},
    {"from": "gpt", "value": "Merhaba! Nasıl yardımcı olabilirim?"}
  ]
}
```

## ChatML Format (OpenAI)
```json
{
  "messages": [
    {"role": "system", "content": "Sen bir kod asistanısın."},
    {"role": "user", "content": "Python'da fibonacci yaz"},
    {"role": "assistant", "content": "def fib(n): ..."}
  ]
}
```

## KuroNeko Format
```json
{
  "type": "code_generation",
  "instruction": "Python'da HTTP istemcisi yaz",
  "input": "requests kütüphanesini kullan",
  "output": "import requests\n...",
  "language": "python",
  "difficulty": "medium",
  "tags": ["networking", "http"]
}
```

## Format Karşılaştırması
| Format | Esneklik | Kolaylık | Tool Desteği |
|--------|----------|----------|--------------|
| Alpaca | Orta | Yüksek | Yüksek |
| ShareGPT | Yüksek | Orta | Yüksek |
| ChatML | Yüksek | Yüksek | Çok yüksek |
| KuroNeko | Çok yüksek | Orta | Özel |

## Karar
- Eğitim: ChatML (TRL ile uyumlu)
- Özel veri: KuroNeko formatı
- Dönüşüm: Script ile format dönüşümü
