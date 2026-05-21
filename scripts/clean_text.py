#!/usr/bin/env python3
"""
Veri Temizleme Pipeline'ı

Kullanım:
    python clean_text.py --input raw_data.txt --output clean_data.txt
    python clean_text.py --input-dir data/raw/ --output-dir data/clean/
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import re
import unicodedata
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("clean_text")

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
# Minimum/maximum satır uzunlukları
MIN_LINE_LEN = 10
MAX_LINE_LEN = 100_000

# Minimum/maximum kelime sayısı
MIN_WORDS = 3
MAX_WORDS = 10_000

# Treshold'lar
MIN_ALPHA_RATIO = 0.5  # Minimum alfa karakter oranı
MAX_DIGIT_RATIO = 0.3  # Maksimum rakam oranı
MAX_URL_RATIO = 0.1    # Maksimum URL oranı
MAX_REPEAT_RATIO = 0.3  # Maksimum tekrar oranı

# Regex pattern'leri
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
EMAIL_PATTERN = re.compile(r"\S+@\S+\.\S+")
HTML_PATTERN = re.compile(r"<[^>]+>")
MULTI_SPACE = re.compile(r" {2,}")
MULTI_NEWLINE = re.compile(r"\n{3,}")


# ---------------------------------------------------------------------------
# Temizleme Fonksiyonları
# ---------------------------------------------------------------------------
def normalize_unicode(text: str) -> str:
    """Unicode normalizasyonu (NFC).

    Args:
        text: Giriş metni.

    Returns:
        Normalize edilmiş metin.
    """
    text = unicodedata.normalize("NFC", text)
    # Problemli karakterleri temizle
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Zero-width karakterleri kaldır
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    return text


def remove_urls(text: str) -> str:
    """URL'leri kaldır.

    Args:
        text: Giriş metni.

    Returns:
        URL'siz metin.
    """
    return URL_PATTERN.sub("", text)


def remove_emails(text: str) -> str:
    """E-posta adreslerini kaldır.

    Args:
        text: Giriş metni.

    Returns:
        E-postasız metin.
    """
    return EMAIL_PATTERN.sub("", text)


def remove_html(text: str) -> str:
    """HTML etiketlerini kaldır.

    Args:
        text: Giriş metni.

    Returns:
        HTML'siz metin.
    """
    return HTML_PATTERN.sub("", text)


def normalize_whitespace(text: str) -> str:
    """Boşlukları normaliz et.

    Args:
        text: Giriş metni.

    Returns:
        Normaliz edilmiş metin.
    """
    text = MULTI_SPACE.sub(" ", text)
    text = MULTI_NEWLINE.sub("\n\n", text)
    return text.strip()


def compute_hash(text: str) -> str:
    """Metin hash'i hesapla (dedup için).

    Args:
        text: Giriş metni.

    Returns:
        SHA-256 hash string.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_quality(text: str) -> tuple[bool, str]:
    """Metin kalite kontrolü.

    Args:
        text: Giriş metni.

    Returns:
        (passed, reason) tuple'ı.
    """
    if len(text) < MIN_LINE_LEN:
        return False, f"cok_kisa ({len(text)}<{MIN_LINE_LEN})"
    if len(text) > MAX_LINE_LEN:
        return False, f"cok_uzun ({len(text)}>{MAX_LINE_LEN})"

    words = text.split()
    if len(words) < MIN_WORDS:
        return False, f"cok_az_kelime ({len(words)}<{MIN_WORDS})"
    if len(words) > MAX_WORDS:
        return False, f"cok_fazla_kelime ({len(words)}>{MAX_WORDS})"

    # Alfa karakter oranı
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count / len(text) < MIN_ALPHA_RATIO:
        return False, f"dusuk_alfa_orani ({alpha_count/len(text):.2f})"

    # Rakam oranı
    digit_count = sum(1 for c in text if c.isdigit())
    if digit_count / len(text) > MAX_DIGIT_RATIO:
        return False, f"yuksek_rakam_orani ({digit_count/len(text):.2f})"

    # Tekrar oranı (n-gram based)
    if len(words) >= 10:
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words) - 1)]
        unique_ratio = len(set(bigrams)) / len(bigrams)
        if unique_ratio < (1 - MAX_REPEAT_RATIO):
            return False, f"yuksek_tekrar_orani ({1-unique_ratio:.2f})"

    return True, "ok"


def clean_text(text: str) -> str:
    """Tam temizleme pipeline'ı.

    Args:
        text: Ham metin.

    Returns:
        Temizlenmiş metin.
    """
    text = normalize_unicode(text)
    text = remove_html(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = normalize_whitespace(text)
    return text


def process_file(
    input_path: Path,
    output_path: Path,
    dedup: bool = True,
) -> dict[str, int]:
    """Dosyayı temizle ve kaydet.

    Args:
        input_path: Giriş dosya yolu.
        output_path: Çıkış dosya yolu.
        dedup: Tekrar kaldırma yapılsın mı.

    Returns:
        İstatistik dict'i.
    """
    stats = {
        "total": 0,
        "passed": 0,
        "failed_quality": 0,
        "dedup_removed": 0,
    }
    seen_hashes: set[str] = set()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8", errors="ignore") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            stats["total"] += 1
            line = line.strip()
            if not line:
                continue

            # Temizle
            cleaned = clean_text(line)
            if not cleaned:
                continue

            # Kalite kontrolü
            passed, reason = check_quality(cleaned)
            if not passed:
                stats["failed_quality"] += 1
                continue

            # Dedup
            if dedup:
                h = compute_hash(cleaned)
                if h in seen_hashes:
                    stats["dedup_removed"] += 1
                    continue
                seen_hashes.add(h)

            fout.write(cleaned + "\n")
            stats["passed"] += 1

    logger.info(
        "Islendi: %d satir → %d gecti, %d kalite, %d dedup",
        stats["total"],
        stats["passed"],
        stats["failed_quality"],
        stats["dedup_removed"],
    )
    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Veri temizleme pipeline")
    parser.add_argument("--input", type=Path, help="Giriş dosyası")
    parser.add_argument("--output", type=Path, help="Çıkış dosyası")
    parser.add_argument("--input-dir", type=Path, help="Giriş dizini")
    parser.add_argument("--output-dir", type=Path, help="Çıkış dizini")
    parser.add_argument("--no-dedup", action="store_true", help="Dedup kapalı")
    args = parser.parse_args()

    if args.input and args.output:
        process_file(args.input, args.output, dedup=not args.no_dedup)
    elif args.input_dir and args.output_dir:
        for f in sorted(args.input_dir.glob("*.txt")):
            out = args.output_dir / f.name
            logger.info("Isleniyor: %s", f)
            process_file(f, out, dedup=not args.no_dedup)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
