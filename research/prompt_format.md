# Prompt Format — System, User, Assistant

## Rol Tanımları

### System
- Modelin genel davranışını belirler
- Kısa ve öz olmalı (50-200 token)
- Örnek: "Sen yardımcı bir AI asistanısın. Türkçe yanıt verirsin."

### User
- Kullanıcının mesajı
- Soru, talimat veya bağlam içerir
- Çok turlu konuşmada önceki mesajlar da eklenir

### Assistant
- Modelin yanıtı
- System talimatlarına uygun olmalı
- Tool çağrıları veya düşünce zinciri içerebilir

## Format Kuralları

1. Her mesaj `<|start_header_id|>` ile başlar
2. Rol adı yazılır
3. `<|end_header_id|>` ile rol biter
4. İki yeni satır (`\n\n`) ile mesaj içeriği başlar
5. Mesaj `<|eot_id|>` ile biter
6. Tüm konuşma `<|begin_of_text|>` ile başlar

## Örnek Çok Turlu

```
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
Sen bir programlama asistanısın.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Python'da liste nasıl oluşturulur?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
liste = [1, 2, 3]<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Liste elemanları nasıl yazdırılır?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
for eleman in liste:
    print(eleman)<|eot_id|>
```
