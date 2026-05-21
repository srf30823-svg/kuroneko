#!/usr/bin/env python3
"""
Batch Collator — KuroNeko

Kullanım:
    from collator import BatchCollator
    collator = BatchCollator(pad_token_id=0)
    batch = collator([sample1, sample2, sample3])
"""

from __future__ import annotations

import logging
from typing import Any

import torch

logger = logging.getLogger("kuroneko.collator")


class BatchCollator:
    """Batch collator with padding.

    Args:
        pad_token_id: Padding token ID.
        label_pad_token_id: Label padding token ID (-100).
    """

    def __init__(
        self,
        pad_token_id: int = 0,
        label_pad_token_id: int = -100,
    ) -> None:
        self.pad_token_id = pad_token_id
        self.label_pad_token_id = label_pad_token_id

    def __call__(self, batch: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
        """Batch oluştur.

        Args:
            batch: Örnek listesi.

        Returns:
            dict: Batch tensor'ları.
        """
        # Max length bul
        max_len = max(ex["input_ids"].shape[0] for ex in batch)

        input_ids = []
        labels = []
        attention_mask = []

        for ex in batch:
            ids = ex["input_ids"]
            lbl = ex["labels"]
            seq_len = ids.shape[0]

            # Pad
            pad_len = max_len - seq_len
            if pad_len > 0:
                ids = torch.cat([ids, torch.full((pad_len,), self.pad_token_id)])
                lbl = torch.cat([lbl, torch.full((pad_len,), self.label_pad_token_id)])

            input_ids.append(ids)
            labels.append(lbl)
            attention_mask.append(torch.cat([
                torch.ones(seq_len),
                torch.zeros(pad_len),
            ]))

        return {
            "input_ids": torch.stack(input_ids),
            "labels": torch.stack(labels),
            "attention_mask": torch.stack(attention_mask),
        }
