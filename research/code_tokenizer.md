# Kod Tokenizasyonu — Özel Stratejiler

## Sorunlar
Kod tokenizasyonu doğal metinden farklıdır:
1. **Girinti (Indentation)**: Python'da anlam taşır → token olarak korunmalı
2. **Özel karakterler**: `{`, `}`, `;`, `->`, `=>` gibi tokenlar
3. **Identifier yapısı**: `snake_case`, `camelCase` bütünlüğü
4. **String literal**: İçerik değişse de yapı aynı kalmalı
5. **Yorumlar**: Gereksiz token israfı yapabilir
6. **Unicode identifier'lar**: `π`, `α` gibi matematiksel semboller

## Stratejiler

### 1. Özel Token'lar
- `<indent>`, `<dedent>` — girinti seviyeleri
- `<newline>`, `<tab>` — boşluk semantiği
- `<comment>`, `<string>` — blok işaretçileri
- `<fstring>`, `<decorator>` — Python özel

### 2. Pre-tokenization Kuralları
- Boşlukları koru (önemli indent için)
- String literal'leri tek token olarak işaretle
- Yorumları ayrı pre-token olarak işaretle
- Operatörleri birleştir (`==`, `!=`, `->`)

### 3. Fill-in-the-Middle (FIM) Desteği
- `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>` tokenları
- Kod tamamlama görevleri için kritik
- StarCoder, CodeLlama kullanır

### 4. Repo-Level Tokenization
- Dosya yapısını anlamak için özel tokenlar
- `<filename>`, `<imports>` gibi metadata tokenları

## Mevcut Kod Tokenizer'lar
- **GPT-2 BPE**: Kod için optimize değil
- **StarCoder Tokenizer**: 49K vocab, FIM destekli
- **CodeLlama Tokenizer**: 32K vocab, Python özel
- **Qwen2.5-Coder Tokenizer**: 151K vocab, çok dilli kod

## KuroNeko İçin Öneri
1. Byte-Level BPE, 64K vocab
2. Pre-tokenizer: whitespace + punctuation + kod özel kurallar
3. Özel tokenlar: `<indent>`, `<dedent>`, `<newline>`, `<tab>`, `<comment>`
4. FIM tokenları ekle: `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>`
5. Python, JavaScript, Bash için özel pre-token kuralları

## Kaynaklar
- mbrenndoerfer.com — Code LLM Training: Tokenization, FIM
- HuggingFace — StarCoder Tokenizer
- arXiv — Code Llama: Open Foundation Models for Code
