# Chat Template — Llama-3 Formatı

## Format

Llama-3 chat template:
```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{assistant_message}<|eot_id|>
```

## KuroNeko Chat Template

### System + User + Assistant
```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sen yardımcı bir AI asistanısın.<|eot_id|><|start_header_id|>user<|end_header_id|>

Merhaba!<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Merhaba! Size nasıl yardımcı olabilirim?<|eot_id|>
```

### Kod Modu
```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Sen bir kod yazma asistanısın. Python, JavaScript ve Bash bilirsin.<|eot_id|><|start_header_id|>user<|end_header_id|>

Fibonacci fonksiyonu yaz.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```<|eot_id|>
```

### Tool Kullanımı
```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Kullanabileceğiniz araçlar: search, calculator<|eot_id|><|start_header_id|>user<|end_header_id|>

İstanbul'da hava durumu nedir?<|eot_id|><|start_header_id|>assistant<|end_header_id|>

<|tool_call|>{"name": "search", "arguments": {"query": "İstanbul hava durumu"}}<|tool_response|>{"result": "İstanbul'da güneşli, 25°C"}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

İstanbul'da bugün hava güneşli ve sıcaklık 25°C.<|eot_id|>
```
