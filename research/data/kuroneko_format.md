# JSONL Format ve KuroNeko Veri Formatı
> Adım 23 | Tarih: 2026-05-21

## JSONL Nedir?
- Her satır bir JSON objesi
- Büyük veri setleri için ideal (streaming okuma)
- HuggingFace datasets ile uyumlu

## Standart Instruction Format
```json
{
  "instruction": "Python'da bir fonksiyon yaz",
  "input": "Bir sayının faktöriyelini hesaplayan",
  "output": "def faktoriyel(n):\n    if n <= 1:\n        return 1\n    return n * faktoriyel(n-1)"
}
```

## KuroNeko Özel Format
```json
{
  "type": "code_generation",
  "instruction": "Python'da bir HTTP istemcisi yaz",
  "input": "requests kütüphanesini kullan",
  "output": "import requests\n\nresponse = requests.get('https://api.example.com')\nprint(response.json())",
  "language": "python",
  "difficulty": "medium",
  "tags": ["networking", "http", "api"]
}
```

## Format Türleri
1. **code_generation:** Kod yazma
2. **code_debug:** Hata bulma
3. **code_review:** Kod inceleme
4. **chat:** Sohbet
5. **qa:** Soru-cevap
6. **summarization:** Özetleme
7. **translation:** Çeviri

## Dosya Yapısı
```
data/
├── kuroneko_train.jsonl      # Eğitim verisi
├── kuroneko_val.jsonl        # Doğrulama verisi
├── kuroneko_test.jsonl       # Test verisi
└── kuroneko_dpo.jsonl        # DPO verisi (opsiyonel)
```
