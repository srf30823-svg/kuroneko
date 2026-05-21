#!/usr/bin/env python3
"""Otomatik veri toplama."""
import json
import os
import re
import subprocess
from pathlib import Path


def collect_from_github(query, language, max_repos=10):
    """GitHub'dan kod ornekleri topla."""
    # GitHub API veya gh CLI kullan
    result = subprocess.run(
        ["gh", "search", "repos", query, "--language", language, "--limit", str(max_repos)],
        capture_output=True, text=True
    )
    
    repos = result.stdout.strip().split("\n")
    examples = []
    
    for repo in repos:
        if not repo:
            continue
        # Repo'yu clone et ve kod dosyalarini tara
        # Bu kismi implementasyona bagli
        pass
    
    return examples


def collect_from_wikipedia(lang="tr", max_pages=100):
    """Wikipedia'dan metin topla."""
    # Wikipedia API kullan
    import urllib.request
    import json
    
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=random&rnlimit={max_pages}&format=json"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            pages = data["query"]["random"]
            return [{"title": p["title"], "id": p["id"]} for p in pages]
    except Exception as e:
        print(f"Hata: {e}")
        return []


def generate_synthetic_instructions(base_instructions, count=100):
    """Sentetik instruction olustur."""
    synthetic = []
    
    templates = [
        "Python'da {task} kodunu yaz",
        "JavaScript'te {task} ornegi ver",
        "Bash'te {task} scripti yaz",
        "Acikla: {task}",
        "Karsilastir: {task}",
    ]
    
    tasks = [
        "dosya okuma", "HTTP istemcisi", "veritabani baglantisi",
        "sifreleme", "siralama algoritmasi", "arama algoritmasi",
    ]
    
    for i in range(count):
        template = templates[i % len(templates)]
        task = tasks[i % len(tasks)]
        instruction = template.format(task=task)
        
        synthetic.append({
            "type": "code_generation",
            "instruction": instruction,
            "input": "",
            "output": f"# {instruction} ornegi",
            "language": "python",
            "difficulty": "medium",
            "tags": ["synthetic"],
        })
    
    return synthetic


def save_dataset(examples, output_path):
    """Dataset'i kaydet."""
    with open(output_path, "w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    
    print(f"Kaydedildi: {output_path} ({len(examples)} ornek)")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Kullanim: collect_data.py <output.jsonl> [--github|--wikipedia|--synthetic]")
        sys.exit(1)
    
    output = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--synthetic"
    
    if mode == "--synthetic":
        examples = generate_synthetic_instructions([], 100)
    elif mode == "--wikipedia":
        examples = collect_from_wikipedia()
    else:
        examples = []
    
    save_dataset(examples, output)
