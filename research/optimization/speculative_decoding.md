# Spekülatif Decoding
> Adım 36 | Tarih: 2026-05-21

## Nedir?
Küçük model (draft) büyük modelin (target) çıktılarını tahmin eder
Büyük model sadece doğrular → Hız artışı

## Nasıl Çalışır?
1. Draft model kadar token üretir (hızlı)
2. Target model tüm token'ları paralel doğrular
3. Uyuşanlar kabul, uyuşmayan yerden devam
4. Hız artışı: 2-3x

## Avantajları
- Aynı kalite (lossless)
- Ekstra eğitim gerektirmez
- Mevcut model ile kullanılabilir

## Dezavantajları
- Draft model için ek bellek
- Küçük modellerde kazanç az

## KuroNeko İçin
- 1B model için draft model: 100-300M parametre
- Telefon için bellek kısıtı nedeniyle ilk sürümde yok
- v2'de değerlendirilebilir
