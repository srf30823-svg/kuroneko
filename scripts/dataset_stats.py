#!/usr/bin/env python3
"""Veri seti istatistikleri."""
import json
import sys
from collections import Counter
from pathlib import Path


def analyze_dataset(dataset_path):
    """Veri seti analizi yap."""
    stats = {
        "total": 0,
        "types": Counter(),
        "languages": Counter(),
        "difficulties": Counter(),
        "avg_instruction_len": 0,
        "avg_output_len": 0,
        "empty_inputs": 0,
    }
    
    instr_lens = []
    output_lens = []
    
    with open(dataset_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            stats["total"] += 1
            stats["types"][item.get("type", "unknown")] += 1
            stats["languages"][item.get("language", "unknown")] += 1
            stats["difficulties"][item.get("difficulty", "unknown")] += 1
            
            instr_len = len(item.get("instruction", ""))
            output_len = len(item.get("output", ""))
            instr_lens.append(instr_len)
            output_lens.append(output_len)
            
            if not item.get("input", ""):
                stats["empty_inputs"] += 1
    
    if instr_lens:
        stats["avg_instruction_len"] = sum(instr_lens) / len(instr_lens)
        stats["avg_output_len"] = sum(output_lens) / len(output_lens)
        stats["max_instruction_len"] = max(instr_lens)
        stats["max_output_len"] = max(output_lens)
    
    return stats


def print_stats(stats):
    """Istatistikleri yazdir."""
    print("=" * 50)
    print("KuroNeko Veri Seti Istatistikleri")
    print("=" * 50)
    print(f"Toplam ornek: {stats['total']}")
    print(f"Ortalama instruction uzunlugu: {stats['avg_instruction_len']:.0f} karakter")
    print(f"Ortalama output uzunlugu: {stats['avg_output_len']:.0f} karakter")
    print(f"Bos input sayisi: {stats['empty_inputs']}")
    
    print("\nTur dagilimi:")
    for t, c in stats["types"].most_common():
        print(f"  {t}: {c} ({c/stats['total']*100:.1f}%)")
    
    print("\nDil dagilimi:")
    for l, c in stats["languages"].most_common():
        print(f"  {l}: {c}")
    
    print("\nZorluk dagilimi:")
    for d, c in stats["difficulties"].most_common():
        print(f"  {d}: {c}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanim: dataset_stats.py <dataset.jsonl>")
        sys.exit(1)
    
    stats = analyze_dataset(sys.argv[1])
    print_stats(stats)
