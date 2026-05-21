#!/usr/bin/env python3
"""
KuroNeko SFT (Supervised Fine-Tuning) Training Loop

Kullanım:
    python sft.py --config configs/sft_v1.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import time
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("kuroneko.sft")


class SFTConfig:
    """SFT konfigürasyonu."""

    def __init__(self, **kwargs) -> None:
        self.data_path: str = kwargs.get("data_path", "data/instruction/all_instruct.jsonl")
        self.model_path: str = kwargs.get("model_path", "models/kuroneko-v1/step-final")
        self.output_dir: str = kwargs.get("output_dir", "models/kuroneko-v1-sft")
        self.batch_size: int = kwargs.get("batch_size", 8)
        self.gradient_accumulation_steps: int = kwargs.get("gradient_accumulation_steps", 4)
        self.epochs: int = kwargs.get("epochs", 3)
        self.learning_rate: float = kwargs.get("learning_rate", 2e-5)
        self.weight_decay: float = kwargs.get("weight_decay", 0.01)
        self.grad_clip: float = kwargs.get("grad_clip", 1.0)
        self.max_length: int = kwargs.get("max_length", 2048)
        self.warmup_ratio: float = kwargs.get("warmup_ratio", 0.03)
        self.checkpoint_every: int = kwargs.get("checkpoint_every", 500)
        self.seed: int = kwargs.get("seed", 42)
        self.use_lora: bool = kwargs.get("use_lora", False)
        self.lora_r: int = kwargs.get("lora_r", 16)


def train_sft(config: SFTConfig) -> None:
    """SFT eğitim döngüsü.

    Args:
        config: SFT konfigürasyonu.
    """
    torch.manual_seed(config.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Model yükle
    from kuroneko.model.kuroneko_v1 import KuroNekoConfig, KuroNekoModel

    model_config = KuroNekoConfig(context_length=config.max_length)
    model = KuroNekoModel(model_config).to(device)

    # LoRA (opsiyonel)
    if config.use_lora:
        try:
            from peft import LoraConfig, get_peft_model
            lora_config = LoraConfig(
                r=config.lora_r,
                lora_alpha=config.lora_r * 2,
                target_modules=["wq", "wk", "wv", "wo"],
                lora_dropout=0.05,
                bias="none",
            )
            model = get_peft_model(model, lora_config)
            logger.info("LoRA aktif: r=%d", config.lora_r)
        except ImportError:
            logger.warning("PEFT kurulu değil, LoRA atlanıyor")

    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        betas=(0.9, 0.95),
        eps=1e-8,
        weight_decay=config.weight_decay,
    )

    # Dataset
    from kuroneko.model.dataset import InstructionDataset

    dataset = InstructionDataset(
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

    total_steps = len(dataloader) * config.epochs // config.gradient_accumulation_steps
    warmup_steps = int(total_steps * config.warmup_ratio)

    # Scheduler
    def lr_lambda(step: int) -> float:
        if step < warmup_steps:
            return float(step) / float(max(1, warmup_steps))
        progress = float(step - warmup_steps) / float(max(1, total_steps - warmup_steps))
        return max(0.0, 0.5 * (1.0 + math.cos(math.pi * progress)))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    # AMP
    scaler = torch.cuda.amp.GradScaler(enabled=True)

    # Eğitim
    model.train()
    global_step = 0
    optimizer.zero_grad()

    for epoch in range(config.epochs):
        epoch_loss = 0.0
        start_time = time.time()

        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            labels = batch["labels"].to(device)

            with torch.cuda.amp.autocast():
                outputs = model(input_ids, labels=labels)
                loss = outputs["loss"] / config.gradient_accumulation_steps

            scaler.scale(loss).backward()
            epoch_loss += loss.item()

            if (global_step + 1) % config.gradient_accumulation_steps == 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
                scaler.step(optimizer)
                scaler.update()
                scheduler.step()
                optimizer.zero_grad()

            global_step += 1

            if global_step % 100 == 0:
                logger.info(
                    "Epoch %d | Step %d | Loss: %.4f | LR: %.2e",
                    epoch + 1, global_step, loss.item(), scheduler.get_last_lr()[0],
                )

        avg_loss = epoch_loss / len(dataloader)
        elapsed = time.time() - start_time
        logger.info(
            "Epoch %d tamamlandı | Avg Loss: %.4f | Süre: %.1fs",
            epoch + 1, avg_loss, elapsed,
        )

        # Epoch checkpoint
        save_sft_checkpoint(model, optimizer, epoch + 1, config)

    logger.info("SFT eğitimi tamamlandı!")


def save_sft_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    config: SFTConfig,
) -> None:
    """SFT checkpoint kaydet."""
    output_dir = Path(config.output_dir) / f"epoch-{epoch}"
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    }, output_dir / "checkpoint.pt")
    logger.info("Checkpoint: %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="KuroNeko SFT")
    parser.add_argument("--config", type=Path, help="Konfigürasyon")
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = SFTConfig(**json.load(f))
    else:
        config = SFTConfig()

    train_sft(config)


if __name__ == "__main__":
    main()
