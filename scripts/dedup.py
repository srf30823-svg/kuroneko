#!/usr/bin/env python3
"""
MinHash Dedup Script

Kullanım:
    python dedup.py --input data.txt --output deduped.txt
"""

from __future__ import annotations

import argparse
import hashlib
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("dedup")


def shingle(text: str, k: int = 5) -> set[str]:
    """K-gram shingle oluştur.

    Args:
        text: Giriş metni.
        k: Shingle boyutu.

    Returns:
        Shingle set'i.
    """
    words = text.split()
    if len(words) < k:
        return {" ".join(words)}
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}


def minhash(shingles: set[str], num_hashes: int = 50) -> list[int]:
    """MinHash signature hesapla.

    Args:
        shingles: Shingle set'i.
        num_hashes: Hash fonksiyonu sayısı.

    Returns:
        MinHash signature listesi.
    """
    signature = []
    for i in range(num_hashes):
        min_hash = float("inf")
        for s in shingles:
            h = int(hashlib.md5(f"{i}_{s}".encode()).hexdigest(), 16)
            min_hash = min(min_hash, h)
        signature.append(int(min_hash))
    return signature


def jaccard_similarity(sig_a: list[int], sig_b: list[int]) -> float:
    """Jaccard benzerliği (MinHash tahmini).

    Args:
        sig_a: İmza A.
        sig_b: İmza B.

    Returns:
        Tahmini Jaccard benzerliği.
    """
    matches = sum(1 for a, b in zip(sig_a, sig_b) if a == b)
    return matches / len(sig_a)


def dedup_file(
    input_path: str,
    output_path: str,
    threshold: float = 0.8,
    num_hashes: int = 50,
) -> dict[str, int]:
    """Dosyadan tekrar eden satırları kaldır.

    Args:
        input_path: Giriş dosyası.
        output_path: Çıkış dosyası.
        threshold: Benzerlik eşiği.
        num_hashes: MinHash sayısı.

    Returns:
        İstatistik dict'i.
    """
    stats = {"total": 0, "unique": 0, "duplicates": 0}
    signatures: list[tuple[str, list[int]]] = []

    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    stats["total"] = len(lines)

    with open(output_path, "w", encoding="utf-8") as out:
        for line in lines:
            s = shingle(line)
            sig = minhash(s, num_hashes)

            is_dup = False
            for _, existing_sig in signatures:
                if jaccard_similarity(sig, existing_sig) >= threshold:
                    is_dup = True
                    break

            if is_dup:
                stats["duplicates"] += 1
            else:
                signatures.append((line, sig))
                out.write(line + "\n")
                stats["unique"] += 1

    logger.info(
        "Dedup: %d → %d unique (%d kaldirildi)",
        stats["total"],
        stats["unique"],
        stats["duplicates"],
    )
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="MinHash Dedup")
    parser.add_argument("--input", required=True, help="Giriş dosyası")
    parser.add_argument("--output", required=True, help="Çıkış dosyası")
    parser.add_argument("--threshold", type=float, default=0.8, help="Benzerlik eşiği")
    args = parser.parse_args()
    dedup_file(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
