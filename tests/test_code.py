#!/usr/bin/env python3
"""
KuroNeko Tokenizer Test — Kod

Kullanım:
    python test_code.py --tokenizer tokenizer/tokenizer.json
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("test_code")

# Test kodları
CODE_TESTS = [
    # Python
    "def hello(name: str) -> str:\n    return f'Hello, {name}!'",
    "class MyClass:\n    def __init__(self):\n        self.value = 42",
    "import numpy as np\narr = np.array([1, 2, 3])",
    "async def fetch(url: str) -> dict:\n    async with aiohttp.ClientSession() as session:\n        return await session.get(url)",
    # JavaScript
    "const add = (a, b) => a + b;",
    "async function fetchData(url) {\n    const res = await fetch(url);\n    return res.json();\n}",
    # Bash
    "echo 'Hello World'\nfor i in $(seq 1 10); do\n    echo $i\ndone",
    "if [ -f /etc/passwd ]; then\n    cat /etc/passwd\nfi",
]


def test_code_tokenizer(tokenizer_path: str | Path) -> dict:
    """Tokenizer'ı kod örnekleriyle test et.

    Args:
        tokenizer_path: Tokenizer JSON dosyası.

    Returns:
        Test sonuçları dict'i.
    """
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    results = []

    for code in CODE_TESTS:
        encoded = tokenizer.encode(code)
        decoded = tokenizer.decode(encoded.ids)

        tokens = len(encoded.tokens)
        chars = len(code)
        ratio = tokens / max(chars, 1)

        results.append({
            "code": code[:80],
            "tokens": tokens,
            "chars": chars,
            "ratio": round(ratio, 3),
            "decoded_ok": decoded == code,
        })

        logger.info(
            "%d token / %d char (%.3f) — %s",
            tokens, chars, ratio, code[:60].replace("\n", "\\n"),
        )

    all_ok = all(r["decoded_ok"] for r in results)
    logger.info("=== Sonuç ===")
    logger.info("Tüm decode OK: %s", all_ok)

    return {"total_tests": len(results), "all_decoded_ok": all_ok, "details": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Kod tokenizer testi")
    parser.add_argument("--tokenizer", type=Path, required=True, help="Tokenizer JSON")
    parser.add_argument("--output", type=Path, help="Çıkış JSON")
    args = parser.parse_args()

    results = test_code_tokenizer(args.tokenizer)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
