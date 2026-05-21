# KuroNeko — Tokenizer Dokümantasyonu

## Kurulum
```bash
pip install tokenizers
```

## Eğitim
```bash
python scripts/train_tokenizer.py \
    --data data/tokenizer_train.txt \
    --output tokenizer/ \
    --vocab-size 64000
```

## Kullanım
```python
from tokenizers import Tokenizer
tok = Tokenizer.from_file("tokenizer/tokenizer.json")
encoded = tok.encode("Merhaba dünya!")
decoded = tok.decode(encoded.ids)
```

## Yapı
- **Format**: Byte-Level BPE
- **Vocab**: 64,000 + 19 özel token = 64,019
- **Özel Tokenlar**: 19 adet (chat, FIM, kod, tool, system)

## Dosyalar
- `research/bpe_research.md` — BPE algoritması
- `research/tokenizer_comparison.md` — Karşılaştırma
- `research/turkish_tokenizer.md` — Türkçe stratejisi
- `research/code_tokenizer.md` — Kod stratejisi
- `research/existing_tokenizers.md` — Mevcut tokenizer'lar
- `research/vocab_size_analysis.md` — Vocab analizi
- `research/special_tokens.md` — Özel tokenlar
- `research/bytelevel_bpe.md` — Byte-level BPE
- `research/vocab_distribution.md` — Vocab dağılımı
- `research/tokenizers_guide.md` — HF rehberi
- `research/tokenizer_benchmark.md` — Benchmark
- `research/chat_template.md` — Chat template
- `research/prompt_format.md` — Prompt formatı
