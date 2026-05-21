#!/usr/bin/env python3
"""
KuroNeko Tokenizer Test — Türkçe Metin

Kullanım:
    python test_turkish.py --tokenizer tokenizer/tokenizer.json
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("test_turkish")

# Test metinleri
TURKISH_TESTS = [
    "Merhaba dünya!",
    "Türkiye'nin başkenti Ankara'dır.",
    "Çekoslovakyalılaştıramadıklarımızdan mısınız?",
    "İstanbul üniversitesinde bilgisayar mühendisliği okuyorum.",
    "Python programlama dili çok popülerdir.",
    "Yapay zeka ve makine öğrenmesi hakkında bilgi ver.",
    "Bugün hava çok güneşli, dışarı çıkabilir miyiz?",
    "Kuantum bilgisayarlar gelecekte devrim yapacak.",
    "Türkçe doğal dil işleme alanında çalışmalar artıyor.",
    "Öğrenciler sınavlara hazırlanıyor.",
]


def test_tokenizer(tokenizer_path: str | Path) -> dict:
    """Tokenizer'ı Türkçe metinlerle test et.

    Args:
        tokenizer_path: Tokenizer JSON dosyası.

    Returns:
        Test sonuçları dict'i.
    """
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    results = []

    total_tokens = 0
    total_chars = 0

    for text in TURKISH_TESTS:
        encoded = tokenizer.encode(text)
        decoded = tokenizer.decode(encoded.ids)

        tokens = len(encoded.tokens)
        chars = len(text)
        ratio = tokens / max(chars, 1)

        total_tokens += tokens
        total_chars += chars

        results.append({
            "text": text,
            "tokens": tokens,
            "chars": chars,
            "ratio": round(ratio, 3),
            "decoded_ok": decoded == text,
        })

        logger.info(
            "%d token / %d char (%.3f) — %s",
            tokens, chars, ratio, text[:50],
        )

    avg_ratio = total_tokens / max(total_chars, 1)
    all_ok = all(r["decoded_ok"] for r in results)

    summary = {
        "total_tests": len(results),
        "all_decoded_ok": all_ok,
        "avg_tokens_per_char": round(avg_ratio, 4),
        "total_tokens": total_tokens,
        "total_chars": total_chars,
        "details": results,
    }

    logger.info("=== Sonuç ===")
    logger.info("Tüm decode OK: %s", all_ok)
    logger.info("Ortalama token/karakter: %.4f", avg_ratio)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Türkçe tokenizer testi")
    parser.add_argument("--tokenizer", type=Path, required=True, help="Tokenizer JSON")
    parser.add_argument("--output", type=Path, help="Çıkış JSON")
    args = parser.parse_args()

    results = test_tokenizer(args.tokenizer)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
