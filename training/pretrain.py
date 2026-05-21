#!/usr/bin/env python3
"""
KuroNeko Pre-training Loop

Kullanım:
    python pretrain.py --config configs/pretrain_v1.yaml
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
logger = logging.getLogger("kuroneko.pretrain")


class TrainingConfig:
    """Eğitim konfigürasyonu."""

    def __init__(self, **kwargs) -> None:
        self.data_path: str = kwargs.get("data_path", "data/clean/pretrain_data.jsonl")
        self.output_dir: str = kwargs.get("output_dir", "models/kuroneko-v1")
        self.batch_size: int = kwargs.get("batch_size", 4)
        self.gradient_accumulation_steps: int = kwargs.get("gradient_accumulation_steps", 8)
        self.max_steps: int = kwargs.get("max_steps", 100_000)
        self.warmup_steps: int = kwargs.get("warmup_steps", 2000)
        self.learning_rate: float = kwargs.get("learning_rate", 3e-4)
        self.weight_decay: float = kwargs.get("weight_decay", 0.1)
        self.grad_clip: float = kwargs.get("grad_clip", 1.0)
        self.max_length: int = kwargs.get("max_length", 2048)
        self.checkpoint_every: int = kwargs.get("checkpoint_every", 1000)
        self.eval_every: int = kwargs.get("eval_every", 500)
        self.log_every: int = kwargs.get("log_every", 100)
        self.seed: int = kwargs.get("seed", 42)
        self.use_amp: bool = kwargs.get("use_amp", True)
        self.gradient_checkpointing: bool = kwargs.get("gradient_checkpointing", True)


def get_cosine_schedule_with_warmup(
    optimizer: torch.optim.Optimizer,
    num_warmup_steps: int,
    num_training_steps: int,
) -> torch.optim.lr_scheduler.LambdaLR:
    """Cosine schedule with warmup.

    Args:
        optimizer: Optimizer.
        num_warmup_steps: Warmup adım sayısı.
        num_training_steps: Toplam eğitim adımı.

    Returns:
        LambdaLR scheduler.
    """
    def lr_lambda(current_step: int) -> float:
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        progress = float(current_step - num_warmup_steps) / float(
            max(1, num_training_steps - num_warmup_steps)
        )
        return max(0.0, 0.5 * (1.0 + math.cos(math.pi * progress)))

    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def train(config: TrainingConfig) -> None:
    """Ana eğitim döngüsü.

    Args:
        config: Eğitim konfigürasyonu.
    """
    # Seed
    torch.manual_seed(config.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(config.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Cihaz: %s", device)

    # Model
    from kuroneko.model.kuroneko_v1 import KuroNekoConfig, KuroNekoModel

    model_config = KuroNekoConfig(
        context_length=config.max_length,
    )
    model = KuroNekoModel(model_config).to(device)

    if config.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    logger.info("Model parametreleri: %.2fB", model.num_params / 1e9)

    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        betas=(0.9, 0.95),
        eps=1e-8,
        weight_decay=config.weight_decay,
    )

    # Scheduler
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=config.warmup_steps,
        num_training_steps=config.max_steps,
    )

    # AMP
    scaler = torch.cuda.amp.GradScaler(enabled=config.use_amp)

    # Dataset
    from kuroneko.model.dataset import KuroNekoDataset

    dataset = KuroNekoDataset(
        data_path=config.data_path,
        tokenizer=None,  # TODO: Tokenizer entegrasyonu
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
    model.train()
    global_step = 0
    total_loss = 0.0
    start_time = time.time()

    optimizer.zero_grad()

    while global_step < config.max_steps:
        for batch in dataloader:
            if global_step >= config.max_steps:
                break

            input_ids = batch["input_ids"].to(device)
            labels = batch["labels"].to(device)

            # Forward (AMP)
            with torch.cuda.amp.autocast(enabled=config.use_amp):
                outputs = model(input_ids, labels=labels)
                loss = outputs["loss"] / config.gradient_accumulation_steps

            # Backward
            scaler.scale(loss).backward()

            total_loss += loss.item()

            # Optimizer step
            if (global_step + 1) % config.gradient_accumulation_steps == 0:
                # Grad clip
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)

                scaler.step(optimizer)
                scaler.update()
                scheduler.step()
                optimizer.zero_grad()

            global_step += 1

            # Log
            if global_step % config.log_every == 0:
                avg_loss = total_loss / config.log_every
                elapsed = time.time() - start_time
                lr = scheduler.get_last_lr()[0]
                logger.info(
                    "Step %d | Loss: %.4f | LR: %.2e | %.1f step/s",
                    global_step, avg_loss, lr, config.log_every / elapsed,
                )
                total_loss = 0.0
                start_time = time.time()

            # Checkpoint
            if global_step % config.checkpoint_every == 0:
                save_checkpoint(model, optimizer, scheduler, global_step, config)

    # Final checkpoint
    save_checkpoint(model, optimizer, scheduler, global_step, config)
    logger.info("Eğitim tamamlandı! Toplam adım: %d", global_step)


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LambdaLR,
    step: int,
    config: TrainingConfig,
) -> None:
    """Checkpoint kaydet.

    Args:
        model: Model.
        optimizer: Optimizer.
        scheduler: Scheduler.
        step: Adım sayısı.
        config: Konfigürasyon.
    """
    output_dir = Path(config.output_dir) / f"step-{step}"
    output_dir.mkdir(parents=True, exist_ok=True)

    torch.save({
        "step": step,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
    }, output_dir / "checkpoint.pt")

    logger.info("Checkpoint kaydedildi: %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="KuroNeko Pre-training")
    parser.add_argument("--config", type=Path, help="Konfigürasyon dosyası")
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            cfg_dict = json.load(f)
        config = TrainingConfig(**cfg_dict)
    else:
        config = TrainingConfig()

    train(config)


if __name__ == "__main__":
    main()
