# KuroNeko Özel Benchmark
> Adım 54 | Tarih: 2026-05-21

## Kod Yazma (50 soru)
- Python: 20 soru (easy: 7, medium: 8, hard: 5)
- JavaScript: 15 soru (easy: 5, medium: 6, hard: 4)
- Bash: 10 soru (easy: 4, medium: 4, hard: 2)
- SQL: 5 soru (easy: 2, medium: 2, hard: 1)

## Hata Bulma (30 soru)
- Python: 15 soru (syntax: 5, logic: 5, edge case: 5)
- JavaScript: 10 soru
- Bash: 5 soru

## Sohbet (20 soru)
- Türkçe: 10 soru
- İngilizce: 10 soru
- Kategori: Genel bilgi, kod, günlük

## Değerlendirme Metrikleri
- **Kod:** Pass@1 (doğrudan çalışıyor mu?)
- **Hata bulma:** Accuracy (doğru hatayı buldu mu?)
- **Sohbet:** 1-5 puan (insan değerlendirmesi)

## Otomatik Değerlendirme
```python
# Kod için
def evaluate_code(generated, test_cases):
    for test in test_cases:
        result = execute(generated, test.input)
        if result != test.expected:
            return False
    return True

# Hata bulma için
def evaluate_debug(generated_fix, bug, expected_fix):
    fixed_code = apply_fix(bug.code, generated_fix)
    return test(fixed_code) == test(bug.original)
```

## İnsan Değerlendirmesi
- 3 değerlendirici
- 1-5 Likert skalası
- Kriterler: Doğruluk, yardımcılık, güvenlik, Türkçe kalitesi
