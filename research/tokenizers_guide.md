# HuggingFace Tokenizers Kütüphanesi Rehberi

## Kurulum
```bash
pip install tokenizers
```

## Temel Kullanım

### Tokenizer Eğitimi
```python
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()

trainer = trainers.BpeTrainer(
    vocab_size=64000,
    special_tokens=["<|begin_of_text|>", "<|end_of_text|>", ...],
    min_frequency=2,
)
tokenizer.train(["data.txt"], trainer)
tokenizer.save("tokenizer.json")
```

### Tokenizer Yükleme
```python
from tokenizers import Tokenizer
tokenizer = Tokenizer.from_file("tokenizer.json")
encoded = tokenizer.encode("Merhaba dünya!")
decoded = tokenizer.decode(encoded.ids)
```

## Pre-tokenizer Seçenekleri
- **ByteLevel**: Byte-level BPE (önerilen)
- **Whitespace**: Boşluk bazlı
- **WhitespaceSplit**: Sadece whitespace split
- **BertPre-tokenizer**: WordPiece için

## Trainer Seçenekleri
- **BpeTrainer**: BPE eğitimi
- **UnigramTrainer**: Unigram eğitimi
- **WordPieceTrainer**: WordPiece eğitimi

## Post-processor
- **ByteLevel**: Offset trimming
- **RobertaProcessing**: BERT/RoBERTa formatı
- **TemplateProcessing**: Özel template

## Kaynaklar
- HuggingFace Tokenizers Docs
- HuggingFace LLM Course — Chapter 6
