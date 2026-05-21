#!/usr/bin/env python3
"""Model karsilastirma."""
import json
import sys


def compare_models(results_paths):
    """Birden fazla modelin sonuclarini karsilastir."""
    comparison = {}
    
    for path in results_paths:
        name = path.split("/")[-1].replace(".json", "")
        with open(path) as f:
            results = json.load(f)
        comparison[name] = results
    
    # Tablo olustur
    print("=" * 60)
    print("Model Karsilastirma")
    print("=" * 60)
    
    headers = ["Model", "MMLU", "HumanEval", "GSM8K", "TR-MMLU", "Kod+TR"]
    print(f"{headers[0]:<20} {headers[1]:>8} {headers[2]:>10} {headers[3]:>8} {headers[4]:>8} {headers[5]:>8}")
    print("-" * 60)
    
    for name, results in comparison.items():
        mmlu = results.get("mmlu", "-")
        humaneval = results.get("humaneval", "-")
        gsm8k = results.get("gsm8k", "-")
        tr_mmlu = results.get("tr_mmlu", "-")
        kod_tr = results.get("kod_tr", "-")
        print(f"{name:<20} {str(mmlu):>8} {str(humaneval):>10} {str(gsm8k):>8} {str(tr_mmlu):>8} {str(kod_tr):>8}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanim: compare_models.py <results1.json> <results2.json> ...")
        sys.exit(1)
    
    compare_models(sys.argv[1:])
