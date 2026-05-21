# The Stack v2 Araştırması

## Genel Bakış
- **Proje**: BigCode Project
- **Boyut**: ~468GB (işlenmiş), ~6TB (ham)
- **Diller**: 600+ programlama dili
- **Lisans**: Permissive license filtreli
- **Format**: Parquet

## İçerik
- Python, JavaScript, Java, C++, Ruby, PHP, Swift, Shell
- 3B+ dosya
- Repository-level bilgi
- Commit history

## İndirme
```python
from datasets import load_dataset
ds = load_dataset("bigcode/the-stack-v2", split="train", streaming=True)
```

## Filtreleme Stratejisi
1. Lisans filtreleme (MIT, Apache, BSD)
2. Dosya boyutu filtreleme (< 1MB)
3. Dil filtreleme (Python, JS, Bash)
4. Kalite skoru (syntax valid, docstring var)
5. Dedup (exact + near-dedup)

## Kaynaklar
- HuggingFace bigcode/the-stack-v2
- GitHub bigcode-project/the-stack-v2
