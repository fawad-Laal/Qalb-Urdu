# Qalb Usage Guide

## 🚀 Quick Start

### Option 1: Ollama (Easiest - Recommended for Local Testing)

```bash
# Install Ollama if not already installed
# Download from: https://ollama.com/download

# Pull and run the model
ollama run enstazao/qalb:8b-instruct-fp16
```

### Option 2: Python with Ollama

```python
import ollama

response = ollama.chat(model='enstazao/qalb:8b-instruct-fp16', messages=[
  {
    'role': 'user',
    'content': 'پاکستان کا قومی کھیل کیا ہے؟',
  },
])

print(response['message']['content'])
```

### Option 3: cURL (REST API)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "enstazao/qalb:8b-instruct-fp16",
  "prompt": "پاکستان کا قومی کھیل کیا ہے؟",
  "stream": false
}'
```

## 🐍 Python Usage Methods

### Method 1: Using Unsloth (Recommended - Fast & Efficient)

The easiest and fastest way to run Qalb with 2x faster inference:

```python
from unsloth import FastLanguageModel
import torch

# Load model with 4-bit quantization
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="enstazao/Qalb-1.0-8B-Instruct",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,  # Use 4-bit quantization for memory efficiency
)
FastLanguageModel.for_inference(model)

# System prompt in Urdu
urdu_system_prompt = "آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔"

# Example questions
questions = [
    "پاکستان کا قومی کھیل کیا ہے؟",
    "لاہور شہر کیوں مشہور ہے؟ مختصر وضاحت کریں۔",
    "سوال: لیاقت علی خان کون تھے؟",
    "کراچی کو روشنیوں کا شہر کیوں کہا جاتا ہے؟",
    "انگریزی میں ترجمہ کریں: 'محنت کامیابی کی کنجی ہے۔'"
]

print("🚀 Starting Batch Generation...\n")

for user_input in questions:
    print(f"🔹 Question: {user_input}")

    # Format prompt using Llama-3 style
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{urdu_system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.1,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
        eos_token_id=[tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    )

    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
    
    print(f"✅ Answer: {response}")
    print("-" * 50)
```

### Method 2: Using Hugging Face Transformers

Compatible with standard transformers if Unsloth is not available:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

model_name = "enstazao/Qalb-1.0-8B-Instruct"
urdu_system_prompt = "آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔"

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

print("⏳ Loading model in 4-bit...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# Example questions
questions = [
    "پاکستان کا قومی کھیل کیا ہے؟",
    "لاہور شہر کیوں مشہور ہے؟ مختصر وضاحت کریں۔",
    "سوال: لیاقت علی خان کون تھے؟",
    "سوال: اسلام آباد شہر کے بارے میں بتائیں۔",
    "انگریزی میں ترجمہ کریں: 'محنت کامیابی کی کنجی ہے۔'"
]

print("Model Loaded. Starting Generation...\n")

for user_input in questions:
    print(f"🔹 Question: {user_input}")
    
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{urdu_system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

    input_ids = tokenizer([prompt], return_tensors="pt").to("cuda")

    outputs = model.generate(
        **input_ids,
        max_new_tokens=256,
        temperature=0.1,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
        eos_token_id=terminators
    )

    response = tokenizer.decode(outputs[0][input_ids['input_ids'].shape[1]:], skip_special_tokens=True)
    
    print(f"✅ Answer: {response}")
    print("-" * 50)
```

## 🌐 Google Colab

For easy cloud-based testing without local GPU:

[Open In Colab](https://colab.research.google.com/drive/1SQ_OaPhr1Q130FDho89zvughfRxJqdoF?usp=sharing)

## ⚙️ Recommended Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `max_new_tokens` | 256 | Maximum tokens to generate |
| `temperature` | 0.1 | Lower = more deterministic |
| `top_p` | 0.9 | Nucleus sampling threshold |
| `repetition_penalty` | 1.1 | Prevents repetitive outputs |
| `do_sample` | True | Enable sampling |

## 📝 Prompt Template

Use the official Llama-3 chat template:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

### Default System Prompt

**Urdu:**
```
آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔
```

**English Translation:**
```
You are a helpful and harmless AI assistant. You provide correct answers to questions in Urdu.
```

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **GPU VRAM** | 8GB (with 4-bit quantization) |
| **RAM** | 16GB |
| **Storage** | 20GB free space |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| **GPU VRAM** | 16GB+ (for FP16) |
| **RAM** | 32GB |
| **Storage** | 40GB free space |

## 📦 Installation

### For Unsloth

```bash
pip install unsloth
pip install torch
```

### For Transformers

```bash
pip install transformers
pip install torch
pip install bitsandbytes
pip install accelerate
```

### For Ollama

```bash
# Windows: Download from https://ollama.com/download
# Linux/Mac:
curl -fsSL https://ollama.com/install.sh | sh
```

## 🎯 Example Use Cases

### 1. Question Answering

```python
question = "پاکستان کا دارالحکومت کون سا شہر ہے؟"
# Response: اسلام آباد پاکستان کا دارالحکومت ہے۔
```

### 2. Translation (Urdu → English)

```python
question = "انگریزی میں ترجمہ کریں: 'محنت کامیابی کی کنجی ہے۔'"
# Response: Hard work is the key to success.
```

### 3. Creative Writing

```python
question = "ایک مختصر کہانی لکھیں جس میں ایک بچہ اور اس کا دوست ہو۔"
# Response: [Generates creative Urdu story]
```

### 4. Sentiment Analysis

```python
question = "اس جملے کا جذبات بتائیں: 'آج کا دن بہت اچھا گزرا'"
# Response: یہ جملہ مثبت جذبات کا اظہار کرتا ہے...
```

### 5. Text Classification

```python
question = "اس خبر کی درجہ بندی کریں: 'پاکستان نے کرکٹ میچ جیت لیا'"
# Response: کھیل (Sports)
```

## ⚠️ Limitations & Best Practices

### Limitations

- May reflect biases present in training data
- Should not be used as sole source for:
  - Medical advice
  - Legal guidance
  - Religious rulings
- Always fact-check critical information

### Best Practices

1. ✅ Use appropriate system prompts
2. ✅ Set reasonable `max_new_tokens`
3. ✅ Use lower `temperature` for factual tasks
4. ✅ Verify outputs for critical applications
5. ✅ Use 4-bit quantization for memory-constrained systems
