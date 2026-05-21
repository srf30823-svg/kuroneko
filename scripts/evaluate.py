#!/usr/bin/env python3
"""KuroNeko otomatik benchmark degerlendirme."""
import json
import subprocess
import tempfile
import os
import sys


def evaluate_code_generation(model_output, test_cases):
    """Kod uretimini degerlendir."""
    results = {"passed": 0, "failed": 0, "errors": [], "total": len(test_cases)}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(model_output)
        temp_path = f.name

    try:
        for test in test_cases:
            try:
                result = subprocess.run(
                    ['python3', temp_path],
                    input=test.get('input', ''),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.stdout.strip() == test['expected'].strip():
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "test": test.get('name', 'unknown'),
                        "expected": test['expected'],
                        "got": result.stdout.strip()
                    })
            except subprocess.TimeoutExpired:
                results["failed"] += 1
                results["errors"].append({"test": test.get('name'), "error": "timeout"})
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"test": test.get('name'), "error": str(e)})
    finally:
        os.unlink(temp_path)

    results["pass_rate"] = results["passed"] / max(results["total"], 1)
    return results


def run_benchmark(model_path, benchmark_path):
    """Tam benchmark calistir."""
    with open(benchmark_path) as f:
        benchmark = [json.loads(line) for line in f]

    results = {
        "model": model_path,
        "total": len(benchmark),
        "code_gen": [],
        "debug": [],
        "chat": []
    }

    for item in benchmark:
        if item["type"] == "code_generation":
            pass
        elif item["type"] == "code_debug":
            pass
        elif item["type"] == "chat":
            pass

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanim: evaluate.py <model_path> <benchmark.jsonl>")
        sys.exit(1)

    results = run_benchmark(sys.argv[1], sys.argv[2])
    print(json.dumps(results, indent=2))
