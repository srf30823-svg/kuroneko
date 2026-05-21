#!/usr/bin/env python3
"""GGUF donusturme scripti."""
import subprocess
import sys
import os
from pathlib import Path


def convert_to_gguf(model_path, output_path, quantization="q4_k_m"):
    """HuggingFace modelini GGUF'a cevir."""
    
    # llama.cpp convert scripti
    convert_script = Path("llama.cpp/convert.py")
    
    if not convert_script.exists():
        print("llama.cpp bulunamadi. Klonlaniyor...")
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp"])
    
    # Donustur
    print(f"Donusturuluyor: {model_path} -> {output_path}")
    subprocess.run([
        "python3", str(convert_script),
        model_path,
        "--outtype", "f16",
        "--outfile", output_path + ".f16.gguf"
    ])
    
    # Quantize
    quantize_bin = Path("llama.cpp/quantize")
    if quantize_bin.exists():
        print(f"Quantize ediliyor: {quantization}")
        subprocess.run([
            str(quantize_bin),
            output_path + ".f16.gguf",
            output_path + f".{quantization}.gguf",
            quantization
        ])
    
    print(f"Tamamlandi: {output_path}.{quantization}.gguf")


def convert_with_unsloth(model, tokenizer, output_path, quantization="q4_k_m"):
    """Unsloth ile direkt GGUF olustur."""
    model.save_pretrained_gguf(output_path, tokenizer, quantization_method=quantization)
    print(f"GGUF olusturuldu: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanim: convert_to_gguf.py <model_path> <output_path> [quantization]")
        sys.exit(1)
    
    quant = sys.argv[3] if len(sys.argv) > 3 else "q4_k_m"
    convert_to_gguf(sys.argv[1], sys.argv[2], quant)
