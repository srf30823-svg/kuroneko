# DPO Veri Formatı

## Standart Format
```json
{
    "prompt": "Kullanıcı sorusu",
    "chosen": "İyi yanıt",
    "rejected": "Kötü yanıt"
}
```

## Alpaca Formatı
```json
{
    "instruction": "Görev açıklaması",
    "input": "Ek bağlam (opsiyonel)",
    "chosen": "İyi çıktı",
    "rejected": "Kötü çıktı"
}
```

## Chat Formatı
```json
{
    "messages": [
        {"role": "user", "content": "Soru"}
    ],
    "chosen": {"role": "assistant", "content": "İyi yanıt"},
    "rejected": {"role": "assistant", "content": "Kötü yanıt"}
}
```

## Türkçe DPO Kategorileri
1. **Doğruluk**: Doğru vs yanlış bilgi
2. **Yararlılık**: Yardımsız vs yardımcı
3. **Güvenlik**: Güvenli vs zararlı
4. **Dil kalitesi**: Akıcı vs akıcı olmayan Türkçe
5. **Kod kalitesi**: Çalışan vs çalışmayan kaynak

## Kaynaklar
- HuggingFace DPO documentation
- TRL DPO trainer
- arXiv — DPO paper (Rafailov et al. 2023)
