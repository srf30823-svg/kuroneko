#!/usr/bin/env python3
"""
PyTorch Dataset sınıfı — KuroNeko veri yükleme

Kullanım:
    from dataset import KuroNekoDataset
    ds = KuroNekoDataset("data.jsonl", tokenizer, max_length=4096)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

import torch
from torch.utils.data import Dataset

logger = logging.getLogger("kuroneko.dataset")


class KuroNekoDataset(Dataset):
    """KuroNeko pre-training dataset.

    JSONL formatında veri okur, tokenize eder.
    Her satır bir örnek.

    Args:
        data_path: JSONL dosya yolu.
        tokenizer: HuggingFace tokenizer.
        max_length: Maksimum sequence uzunluğu.
    """

    def __init__(
        self,
        data_path: str | Path,
        tokenizer: Any,
        max_length: int = 4096,
    ) -> None:
        self.data_path = Path(data_path)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples: list[dict] = []

        self._load_data()

    def _load_data(self) -> None:
        """Veriyi yükle."""
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.examples.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        logger.info("Yuklenen ornek: %d", len(self.examples))

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        """Örnek döndür.

        Args:
            idx: Örnek indeksi.

        Returns:
            dict: {"input_ids": tensor, "labels": tensor}
        """
        example = self.examples[idx]
        text = example.get("text", example.get("content", ""))

        # Tokenize
        encoded = self.tokenizer.encode(text)

        # Truncate + pad
        ids = encoded.ids[: self.max_length]
        ids = ids + [0] * (self.max_length - len(ids))

        input_ids = torch.tensor(ids[:-1], dtype=torch.long)
        labels = torch.tensor(ids[1:], dtype=torch.long)

        return {"input_ids": input_ids, "labels": labels}


class InstructionDataset(Dataset):
    """Instruction tuning dataset.

    Args:
        data_path: JSONL dosya yolu.
        tokenizer: HuggingFace tokenizer.
        max_length: Maksimum sequence uzunluğu.
    """

    def __init__(
        self,
        data_path: str | Path,
        tokenizer: Any,
        max_length: int = 4096,
    ) -> None:
        self.data_path = Path(data_path)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples: list[dict] = []

        self._load_data()

    def _load_data(self) -> None:
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.examples.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        ex = self.examples[idx]
        instruction = ex.get("instruction", "")
        input_text = ex.get("input", "")
        output = ex.get("output", ex.get("response", ""))

        # Format: instruction + input + output
        if input_text:
            text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
        else:
            text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"

        encoded = self.tokenizer.encode(text)
        ids = encoded.ids[: self.max_length]
        ids = ids + [0] * (self.max_length - len(ids))

        input_ids = torch.tensor(ids[:-1], dtype=torch.long)
        labels = torch.tensor(ids[1:], dtype=torch.long)

        return {"input_ids": input_ids, "labels": labels}


class DPODataset(Dataset):
    """DPO preference dataset.

    Format: {"prompt": str, "chosen": str, "rejected": str}

    Args:
        data_path: JSONL dosya yolu.
        tokenizer: HuggingFace tokenizer.
        max_length: Maksimum sequence uzunluğu.
    """

    def __init__(
        self,
        data_path: str | Path,
        tokenizer: Any,
        max_length: int = 4096,
    ) -> None:
        self.data_path = Path(data_path)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples: list[dict] = []

        self._load_data()

    def _load_data(self) -> None:
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ex = json.loads(line)
                    if "prompt" in ex and "chosen" in ex and "rejected" in ex:
                        self.examples.append(ex)
                except json.JSONDecodeError:
                    continue

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        ex = self.examples[idx]

        # Encode prompt + chosen
        chosen_text = ex["prompt"] + ex["chosen"]
        chosen_enc = self.tokenizer.encode(chosen_text)
        chosen_ids = chosen_enc.ids[: self.max_length]
        chosen_ids = chosen_ids + [0] * (self.max_length - len(chosen_ids))

        # Encode prompt + rejected
        rejected_text = ex["prompt"] + ex["rejected"]
        rejected_enc = self.tokenizer.encode(rejected_text)
        rejected_ids = rejected_enc.ids[: self.max_length]
        rejected_ids = rejected_ids + [0] * (self.max_length - len(rejected_ids))

        return {
            "chosen_input_ids": torch.tensor(chosen_ids[:-1], dtype=torch.long),
            "chosen_labels": torch.tensor(chosen_ids[1:], dtype=torch.long),
            "rejected_input_ids": torch.tensor(rejected_ids[:-1], dtype=torch.long),
            "rejected_labels": torch.tensor(rejected_ids[1:], dtype=torch.long),
        }
