# Özel Tokenlar (Special Tokens) Araştırması

## Kategoriler

### 1. Sistem Tokenlar
- `<|begin_of_text|>` — Metin başlangıcı
- `<|end_of_text|>` — Metin sonu
- `<|pad|>` — Padding
- `<|unk|>` — Bilinmeyen (byte-level'da gerekli değil)

### 2. Chat Tokenlar (Llama 3 formatı)
- `<|start_header_id|>` — Rol başlangıcı
- `<|end_header_id|>` — Rol sonu
- `<|eot_id|>` — End of turn
- Roller: `system`, `user`, `assistant`

### 3. Kod Tokenlar
- `<|fim_prefix|>` — Fill-in-the-middle ön
- `<|fim_suffix|>` — Fill-in-the-middle son
- `<|fim_middle|>` — Fill-in-the-middle orta
- `<indent>`, `<dedent>` — Girinti
- `<newline>`, `<tab>` — Boşluk
- `<comment>`, `<string>` — Yorum/string işaretçi

### 4. Türkçe Özel Tokenlar (v2 için)
- Morfolojik sınırlar: `<|root|>`, `<|suffix|>`
- Ek işaretçiler: `<|case|>`, `<|plural|>`, `<|verb|>`
- Not: v2'de eklenebilir, v1'de gerekli değil

### 5. Tool/Agent Tokenlar
- `<|tool_call|>` — Araç çağrısı başlangıcı
- `<|tool_response|>` — Araç yanıtı
- `<|think|>` — Düşünce zinciri (Qwen3 formatı)
- `<|observation|>` — Gözlem

## KuroNeko v1 Token Listesi
```
<|begin_of_text|>     64000
<|end_of_text|>       64001
<|pad|>               64002
<|start_header_id|>   64003
<|end_header_id|>     64004
<|eot_id|>            64005
<|fim_prefix|>        64006
<|fim_suffix|>        64007
<|fim_middle|>        64008
<indent>              64009
<dedent>              64010
<newline>             64011
<tab>                 64012
<comment>             64013
<string>              64014
<|tool_call|>         64015
<|tool_response|>     64016
<|think|>             64017
<|observation|>       64018
Toplam özel token: 19
Vocab: 64K base + 19 özel = 64019
```

## Kaynaklar
- Llama 3 Tokenizer Spec
- HuggingFace Tokenizers Docs
- StarCoder Tokenizer
