#!/usr/bin/env python3
"""
Veri Kalite Metrikleri

Kullanım:
    python quality_check.py --input data.txt
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections import Counter
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("quality_check")


def compute_stats(texts: list[str]) -> dict:
    """Veri seti istatistiklerini hesapla.

    Args:
        texts: Metin listesi.

    Returns:
        İstatistik dict'i.
    """
    total_chars = sum(len(t) for t in texts)
    total_words = sum(len(t.split()) for t in texts)
    total_lines = len(texts)

    # Kelime frekansları
    word_freq: Counter = Counter()
    for t in texts:
        word_freq.update(t.lower().split())

    # Karakter dağılımı
    char_freq: Counter = Counter()
    for t in texts:
        char_freq.update(t)

    # Dil tespiti (basit: Türkçe karakter oranı)
    turkish_chars = sum(1 for t in texts for c in t if c in "çğıöşüÇĞİÖŞÜ")
    turkish_ratio = turkish_chars / max(total_chars, 1)

    # Boşluk oranı
    space_ratio = sum(1 for t in texts for c in t if c.isspace()) / max(total_chars, 1)

    # Satır uzunluk dağılımı
    lengths = [len(t) for t in texts]

    stats = {
        "total_lines": total_lines,
        "total_chars": total_chars,
        "total_words": total_words,
        "avg_line_length": total_chars / max(total_lines, 1),
        "avg_word_count": total_words / max(total_lines, 1),
        "unique_words": len(word_freq),
        "turkish_char_ratio": round(turkish_ratio, 4),
        "space_ratio": round(space_ratio, 4),
        "min_line_length": min(lengths) if lengths else 0,
        "max_line_length": max(lengths) if lengths else 0,
        "top_20_words": word_freq.most_common(20),
        "top_20_chars": char_freq.most_common(20),
    }
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Veri kalite kontrolü")
    parser.add_argument("--input", type=Path, required=True, help="Giriş dosyası")
    parser.add_argument("--output", type=Path, help="Çıkış JSON dosyası")
    parser.add_argument("--sample", type=int, default=10000, help="Örnek boyutu")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        texts = [line.strip() for line in f if line.strip()][:args.sample]

    stats = compute_stats(texts)

    logger.info("=== Veri Istatistikleri ===")
    for k, v in stats.items():
        if k not in ("top_20_words", "top_20_chars"):
            logger.info("  %s: %s", k, v)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        logger.info("Rapor kaydedildi: %s", args.output)


if __name__ == "__main__":
    main()
