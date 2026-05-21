# Türkçe + Kod İçin Optimal Vocab Dağılımı

## Analiz

64K vocab boyutunda optimal dağılım:

| Kategori | Token Sayısı | Yüzde | Açıklama |
|----------|-------------|-------|----------|
| Byte base | 256 | 0.4% | Tüm byte değerleri |
| ASCII kelimeler | 15,000 | 23.4% | İngilizce + Türkçe ortak |
| Türkçe morfemler | 12,000 | 18.8% | Kökler + ekler |
| Kod keyword'leri | 8,000 | 12.5% | Python, JS, Bash |
| Operatörler | 5,000 | 7.8% | Matematik, kod, özel |
| N-gram kalıplar | 10,000 | 15.6% | Sık kullanılan kombinasyonlar |
| Sayılar/tarih | 3,000 | 4.7% | Yıl, saat, para birimi |
| Özel tokenlar | 19 | 0.03% | Sistem tokenları |
| Boşluk/biçim | 5,725 | 8.9% | Boşluk, girinti, newline |
| **Toplam** | **64,000** | **100%** | |

## Türkçe Morfem Dağılımı
En sık kullanılan Türkçe ekler (token olarak öğrenilmeli):
- `-lar/-ler` (çoğul)
- `-da/-de` (bulunma)
- `-dan/-den` (ayrılma)
- `-ın/-in` (iyelik)
- `-mak/-mek` (mastar)
- `-dı/-di` (geçmiş zaman)
- `-acak/-ecek` (gelecek zaman)
- `-yor` (şimdiki zaman)
- `-mış/-miş` (rivayet)

## Kod Keyword Dağılımı
Python: `def`, `class`, `import`, `return`, `if`, `for`, `while`, `try`, `except`
JavaScript: `function`, `const`, `let`, `var`, `async`, `await`, `export`
Bash: `echo`, `if`, `fi`, `done`, `export`, `source`

## Kaynaklar
- Türkçe morfoloji araştırmaları
- GitHub linguist — Dil istatistikleri
- Common Crawl token analizi
