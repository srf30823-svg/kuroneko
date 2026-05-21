#!/usr/bin/env python3
"""
KuroNeko DPO (Direct Preference Optimization) Training Loop

Kullanım:
    python dpo.py --config configs/dpo_v1.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("kuroneko.dpo")


class DPOConfig:
    """DPO konfigürasyonu."""

    def __init__(self, **kwargs) -> None:
        self.data_path: str = kwargs.get("data_path", "data/dpo/all_dpo.jsonl")
        self.model_path: str = kwargs.get("model_path", "models/kuroneko-v1-sft/epoch-3")
        self.output_dir: str = kwargs.get("output_dir", "models/kuroneko-v1-dpo")
        self.batch_size: int = kwargs.get("batch_size", 4)
        self.epochs: int = kwargs.get("epochs", 1)
        self.learning_rate: float = kwargs.get("learning_rate", 5e-7)
        self.beta: float = kwargs.get("beta", 0.1)
        self.max_length: int = kwargs.get("max_length", 2048)
        self.gradient_accumulation_steps: int = kwargs.get("gradient_accumulation_steps", 4)
        self.checkpoint_every: int = kwargs.get("checkpoint_every", 200)
        self.seed: int = kwargs.get("seed", 42)


def dpo_loss(
    policy_chosen_logps: torch.Tensor,
    policy_rejected_logps: torch.Tensor,
    reference_chosen_logps: torch.Tensor,
    reference_rejected_logps: torch.Tensor,
    beta: float = 0.1,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """DPO loss hesapla.

    Args:
        policy_chosen_logps: Policy model chosen log probs.
        policy_rejected_logps: Policy model rejected log probs.
        reference_chosen_logps: Reference model chosen log probs.
        reference_rejected_logps: Reference model rejected log probs.
        beta: DPO beta parametresi.

    Returns:
        (loss, chosen_rewards, rejected_rewards)
    """
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    ref_logratios = reference_chosen_logps - reference_rejected_logps
    logits = pi_logratios - ref_logratios

    losses = -F.logsigmoid(beta * logits)

    chosen_rewards = beta * (policy_chosen_logps - reference_chosen_logps)
    rejected_rewards = beta * (policy_rejected_logps - reference_rejected_logps)

    return losses.mean(), chosen_rewards.mean(), rejected_rewards.mean()


def train_dpo(config: DPOConfig) -> None:
    """DPO eğitim döngüsü.

    Args:
        config: DPO konfigürasyonu.
    """
    torch.manual_seed(config.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    from kuroneko.model.kuroneko_v1 import KuroNekoConfig, KuroNekoModel

    model_config = KuroNekoConfig(context_length=config.max_length)

    # Policy model (eğitilecek)
    policy_model = KuroNekoModel(model_config).to(device)

    # Reference model (dondurulmuş)
    reference_model = KuroNekoModel(model_config).to(device)
    reference_model.eval()
    for p in reference_model.parameters():
        p.requires_grad = False

    # Optimizer
    optimizer = torch.optim.AdamW(
        policy_model.parameters(),
        lr=config.learning_rate,
        betas=(0.9, 0.95),
        eps=1e-8,
    )

    # Dataset
    from kuroneko.model.dataset import DPODataset

    dataset = DPODataset(
        data_path=config.data_path,
        tokenizer=None,  # TODO
        max_length=config.max_length,
    )

    dataloader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True,
    )

    # Eğitim
    policy_model.train()
    global_step = 0
    optimizer.zero_grad()

    for epoch in range(config.epochs):
        epoch_loss = 0.0
        start_time = time.time()

        for batch in dataloader:
            chosen_ids = batch["chosen_input_ids"].to(device)
            chosen_labels = batch["chosen_labels"].to(device)
            rejected_ids = batch["rejected_input_ids"].to(device)
            rejected_labels = batch["rejected_labels"].to(device)

            # Policy forward
            policy_chosen = policy_model(chosen_ids, labels=chosen_labels)
            policy_rejected = policy_model(rejected_ids, labels=rejected_labels)

            # Reference forward (no grad)
            with torch.no_grad():
                ref_chosen = reference_model(chosen_ids, labels=chosen_labels)
                ref_rejected = reference_model(rejected_ids, labels=rejected_labels)

            # DPO loss
            loss, chosen_r, rejected_r = dpo_loss(
                policy_chosen["loss"].unsqueeze(0),
                policy_rejected["loss"].unsqueeze(0),
                ref_chosen["loss"].unsqueeze(0),
                ref_rejected["loss"].unsqueeze(0),
                beta=config.beta,
            )

            loss = loss / config.gradient_accumulation_steps
            loss.backward()
            epoch_loss += loss.item()

            if (global_step + 1) % config.gradient_accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(policy_model.parameters(), 1.0)
                optimizer.step()
                optimizer.zero_grad()

            global_step += 1

            if global_step % 50 == 0:
                logger.info(
                    "Step %d | Loss: %.4f | Chosen R: %.4f | Rejected R: %.4f",
                    global_step, loss.item(), chosen_r.item(), rejected_r.item(),
                )

        avg_loss = epoch_loss / len(dataloader)
        logger.info("Epoch %d | Avg Loss: %.4f", epoch + 1, avg_loss)

    logger.info("DPO eğitimi tamamlandı!")


def main() -> None:
    parser = argparse.ArgumentParser(description="KuroNeko DPO")
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = DPOConfig(**json.load(f))
    else:
        config = DPOConfig()

    train_dpo(config)


if __name__ == "__main__":
    main()
