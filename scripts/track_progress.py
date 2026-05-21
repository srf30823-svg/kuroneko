#!/usr/bin/env python3
"""Egitim ilerleme takibi."""
import json
import time
import os
import sys
from pathlib import Path


def track_progress(log_file):
    """W&B log dosyasindan ilerleme takip et."""
    if not os.path.exists(log_file):
        print(f"Dosya bulunamadi: {log_file}")
        return
    
    with open(log_file) as f:
        lines = f.readlines()
    
    # Son durum
    last_loss = None
    last_step = 0
    last_eval = None
    
    for line in lines:
        try:
            data = json.loads(line)
            if "train/loss" in data:
                last_loss = data["train/loss"]
                last_step = data.get("step", 0)
            if "eval/loss" in data:
                last_eval = data["eval/loss"]
        except (json.JSONDecodeError, ValueError):
            continue
    
    print("=" * 40)
    print("KuroNeko Egitim Ilerleme")
    print("=" * 40)
    print(f"Son adim: {last_step}")
    print(f"Son train loss: {last_loss}")
    print(f"Son eval loss: {last_eval}")
    
    if last_loss and last_eval:
        gap = last_eval - last_loss
        print(f"Train-Eval gap: {gap:.4f}")
        if gap > 0.2:
            print("UYARI: Overfitting olabilir!")


def monitor_live(log_file, interval=60):
    """Canli izleme."""
    print(f"Izleniyor: {log_file} (her {interval}s)")
    while True:
        track_progress(log_file)
        time.sleep(interval)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanim: track_progress.py <log_file> [--live]")
        sys.exit(1)
    
    if "--live" in sys.argv:
        monitor_live(sys.argv[1])
    else:
        track_progress(sys.argv[1])
