# Güvenlik ve Zararlı Çıktı Önleme
> Adım 49 | Tarih: 2026-05-21

## Risk Kategorileri
1. **Zararlı kod:** Exploit, malware, hack aracı
2. **Kişisel veri:** TC kimlik, kredi kartı, adres
3. **Yanlış bilgi:** Tıbbi, hukuki, finansal tavsiye
4. **Nefret sövcüsü:** Irk, din, cinsiyet ayrımcılığı
1. **Zararlı kod:** Exploit, malware, hack aracı
2. **Kişisel veri:** TC kimlik, kredi kartı, adres
3. **Yanlış bilgi:** Tıbbi, hukuki, finansal tavsiye
4. **Nefret sövcüsü:** Irk, din, cinsiyet ayrımcılığı
5. **Œrtülü zararlı:** Dolaylı olarak zararlı talimat

## Önleme Stratejileri

### 1. System Prompt
```
Sen yardımcı bir kod asistanısın.
- Zararlı kod yazma
- Kişisel veri isteme
- Yasaklı konularda yanıt verme
- Bilmediğini söyle
```

### 2. Input Filtreleme
- Keyword blacklist
- Regex pattern matching
- ML-based classifier

### 3. Output Filtreleme
- Kod güvenlik taraması (bandit)
- Kişisel veri tespiti (regex)
- Zararlı içerik tespiti

### 4. Eğitim
- Red-teaming verisi
- Refusal training
- Constitutional AI ilkeleri

## Uygulama
```python
def safe_generate(prompt):
    if is_harmful(prompt):
        return "Bu talebi karşılayamam."
    
    response = model.generate(prompt)
    
    if contains_pii(response):
        response = redact_pii(response)
    
    return response
```
