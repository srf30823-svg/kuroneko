# Mevcut Tokenizer'lar Karşılaştırması

## Qwen 2.5 Tokenizer
- **Tür**: Byte-Level BPE
- **Vocab**: 151,936 token
- **Özellikler**:
  - Çok dilli optimize (Çince + İngilizce + kod)
  - Türkçe için yeterli ama optimize değil
  - Özel tokenlar: `<|im_start|>`, `<|im_end|>`, `<|object_ref_start|>`
  - FIM desteği var
  - Repo-level tokenization desteği
- **Avantaj**: Çok dilli, kod desteği, büyük vocab
- **Dezavantaj**: Türkçe için fazla büyük, Çince bias

## Llama 3 Tokenizer
- **Tür**: Byte-Level BPE (tiktoken)
- **Vocab**: 128,256 token
- **Özellikler**:
  - İngilizce merkezli ama çok dilli
  - Özel tokenlar: `<|begin_of_text|>`, `<|end_of_text|>`, `<|start_header_id|>`
  - Chat template desteği
  - Tiktoken implementasyonu (hızlı)
- **Avantaj**: Hızlı, yaygın, iyi chat desteği
- **Dezavantaj**: Türkçe için optimize değil, İngilizce bias

## Mistral Tokenizer
- **Tür**: Byte-Level BPE (SentencePiece altyapılı)
- **Vocab**: 32,768 token
- **Özellikler**:
  - Kompakt vocab → daha küçük embedding
  - Özel tokenlar: `<s>`, `</s>`, `[INST]`, `[/INST]`
  - Instruction tuning için optimize
- **Avantaj**: Küçük, verimli, instruction-optimize
- **Dezavantaj**: Küçük vocab → Türkçe'de token israfı

## Karşılaştırma Tablosu
| Özellik | Qwen 2.5 | Llama 3 | Mistral | KuroNeko |
|---------|----------|---------|---------|----------|
| Vocab | 152K | 128K | 33K | 64K |
| Türkçe | Orta | Orta | Zayıf | Hedef |
| Kod | İyi | Orta | Zayıf | Hedef |
| Hız | Orta | Hızlı | Hızlı | Hızlı |
| Chat | Evet | Evet | Evet | Evet |
| FIM | Evet | Hayır | Hayır | Evet |

## KuroNeko İçin Öneri
- **Referans**: Llama 3 tokenizer yapısı (chat template)
- **Vocab**: 64K (Türkçe + kod için optimal)
- **Özel tokenlar**: Llama 3 + FIM + Türkçe + kod özel
- **Implementasyon**: HuggingFace tokenizers (ByteLevelBPETokenizer)
