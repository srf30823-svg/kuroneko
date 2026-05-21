#!/usr/bin/env python3
"""
KuroNeko Tokenizer Eğitim Scripti

HuggingFace tokenizers kütüphanesi ile Byte-Level BPE tokenizer eğitir.

Kullanım:
    python train_tokenizer.py --data data/tokenizer_train.txt --output tokenizer/
    python train_tokenizer.py --data-dir data/clean/ --output tokenizer/ --vocab-size 64000
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers, processors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("train_tokenizer")

# Özel tokenlar
SPECIAL_TOKENS = [
    "<|begin_of_text|>",
    "<|end_of_text|>",
    "<|pad|>",
    "<|start_header_id|>",
    "<|end_header_id|>",
    "<|eot_id|>",
    "<|fim_prefix|>",
    "<|fim_suffix|>",
    "<|fim_middle|>",
    "<indent>",
    "<dedent>",
    "<newline>",
    "<tab>",
    "<comment>",
    "<string>",
    "<|tool_call|>",
    "<|tool_response|>",
    "<|think|>",
    "<|observation|>",
]


def train_tokenizer(
    data_path: str | Path,
    output_dir: str | Path,
    vocab_size: int = 64_000,
) -> None:
    """Byte-Level BPE tokenizer eğit.

    Args:
        data_path: Eğitim verisi dosya yolu.
        output_dir: Çıkış dizini.
        vocab_size: Vocab boyutu (özel tokenlar hariç).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Tokenizer oluştur
    tokenizer = Tokenizer(models.BPE())

    # Pre-tokenizer: ByteLevel
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

    # Decoder: ByteLevel
    tokenizer.decoder = decoders.ByteLevel()

    # Post-processor: ByteLevel (trim_offsets)
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)

    # Trainer
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=SPECIAL_TOKENS,
        min_frequency=2,
        show_progress=True,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    )

    # Eğit
    logger.info("Tokenizer eğitimi başlıyor: %s", data_path)
    tokenizer.train([str(data_path)], trainer=trainer)

    # Kaydet
    tokenizer.save(str(output_dir / "tokenizer.json"))
    logger.info("Tokenizer kaydedildi: %s", output_dir)

    # Test
    test_text = "Merhaba dünya! Bu bir test mesajıdır. print('hello')"
    encoded = tokenizer.encode(test_text)
    logger.info("Test: '%s'", test_text)
    logger.info("Token sayısı: %d", len(encoded.tokens))
    logger.info("Tokenlar: %s", encoded.tokens[:20])
    logger.info("Decode: '%s'", tokenizer.decode(encoded.ids))


def train_from_dir(
    data_dir: str | Path,
    output_dir: str | Path,
    vocab_size: int = 64_000,
    pattern: str = "*.txt",
) -> None:
    """Dizinden tokenizer eğit.

    Args:
        data_dir: Veri dizini.
        output_dir: Çıkış dizini.
        vocab_size: Vocab boyutu.
        pattern: Dosya deseni.
    """
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Dosya bulunamadı: {data_dir}/{pattern}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=SPECIAL_TOKENS,
        min_frequency=2,
        show_progress=True,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    )

    logger.info("Tokenizer eğitimi başlıyor: %d dosya", len(files))
    tokenizer.train([str(f) for f in files], trainer=trainer)

    tokenizer.save(str(output_dir / "tokenizer.json"))
    logger.info("Tokenizer kaydedildi: %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="KuroNeko Tokenizer Eğitimi")
    parser.add_argument("--data", type=Path, help="Eğitim verisi dosyası")
    parser.add_argument("--data-dir", type=Path, help="Eğitim verisi dizini")
    parser.add_argument("--output", type=Path, default=Path("tokenizer"), help="Çıkış dizini")
    parser.add_argument("--vocab-size", type=int, default=64_000, help="Vocab boyutu")
    args = parser.parse_args()

    if args.data:
        train_tokenizer(args.data, args.output, args.vocab_size)
    elif args.data_dir:
        train_from_dir(args.data_dir, args.output, args.vocab_size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
