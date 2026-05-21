# Kod Verisi — GitHub Kaynakları

## Ana Kaynaklar

### 1. The Stack v2 (BigCode Project)
- **Boyut**: ~468GB (işlenmiş), ~6TB (ham)
- **Diller**: 600+ dil, Python/JS/Java/C++/Ruby/PHP/Swift/Shell
- **Lisans**: Permissive license filtreli
- **İndirme**: HuggingFace — `bigcode/the-stack-v2`
- **Format**: Parquet
- **Not**: GitHub token gerektirir (contact info paylaşımı)

### 2. GitHub Archive
- **Boyut**: ~20TB (toplam)
- **Kalite**: Ham, işleme gerektirir
- **İndirme**: Google BigQuery, GH Archive

### 3. CodeSearchNet
- **Boyut**: ~2GB
- **Diller**: Python, Java, JS, Go, PHP, Ruby
- **Kalite**: Yüksek (fonksiyon seviyesi)
- **İndirme**: HuggingFace — `code_search_net`

## Önerilen Dağılık
| Kaynak | Dil | Boyut | Yüzde |
|--------|-----|-------|-------|
| The Stack v2 | Python | 15GB | 30% |
| The Stack v2 | JavaScript | 10GB | 20% |
| The Stack v2 | Bash/Shell | 5GB | 10% |
| The Stack v2 | Java | 5GB | 10% |
| The Stack v2 | C++ | 5GB | 10% |
| CodeSearchNet | Multi | 2GB | 4% |
| Diğer | Multi | 8GB | 16% |
| **Toplam** | | **50GB** | **100%** |

## Kaynaklar
- HuggingFace bigcode/the-stack-v2
- GitHub bigcode-project/the-stack-v2
- CodeSearchNet
