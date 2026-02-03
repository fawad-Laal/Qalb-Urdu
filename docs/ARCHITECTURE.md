# Qalb Technical Architecture

## 🏗️ Model Architecture

### Base Foundation

Qalb is built upon **Meta LLaMA 3.1 8B** as the foundation model, leveraging:

- **Architecture Type**: Transformer-based autoregressive language model
- **Total Parameters**: 8 Billion
- **Trainable Parameters**: ~1.18B (~14.72% of base via LoRA)
- **Precision**: bfloat16

### LoRA Configuration

Qalb uses **Low-Rank Adaptation (LoRA)** for efficient training:

| Parameter | Value |
|-----------|-------|
| LoRA Rank (r) | 128 |
| LoRA Alpha | 32 |
| Trainable Parameters | ~1.18B |
| Percentage of Base | ~14.72% |

### Model Specifications

| Specification | Details |
|--------------|---------|
| **Model Name** | Qalb-1.0-8B-Instruct |
| **Base Model** | unsloth/Meta-Llama-3.1-8B |
| **Model Size** | 8B parameters |
| **Tensor Type** | BF16 |
| **File Format** | Safetensors |
| **Sequence Length** | 2048 tokens |
| **Languages** | Urdu (primary), English (secondary) |

## 🔧 Training Infrastructure

### Hardware

- **GPU**: Single NVIDIA A100 80GB
- **Framework**: Unsloth library
- **Features**: Memory-efficient attention mechanisms + fast LoRA implementations

### Training Configuration

| Parameter | Continued Pre-training | Fine-tuning |
|-----------|----------------------|-------------|
| **Optimizer** | AdamW-8bit | AdamW-8bit |
| **Learning Rate** | Cosine schedule (warmup 0.05) | 5e-5 (linear) |
| **Batch Size** | 128 (effective) | 64 |
| **Epochs** | - | 2 |
| **Precision** | bfloat16 | bfloat16 |
| **Gradient Checkpointing** | Yes | Yes |

## 📊 Two-Stage Training Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                         QALB TRAINING PIPELINE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 1: DATA CURATION                    │    │
│  │                                                               │    │
│  │  ┌──────────────────┐    ┌──────────────────┐               │    │
│  │  │   Urdu Corpus    │    │  English Corpus  │               │    │
│  │  │  1.84B Tokens    │    │   140M Tokens    │               │    │
│  │  │                  │    │                  │               │    │
│  │  │  • News & Media  │    │  • Wikipedia     │               │    │
│  │  │  • Literature    │    │  (Replay Buffer) │               │    │
│  │  │  • Gov Documents │    │                  │               │    │
│  │  │  • Social Media  │    │                  │               │    │
│  │  └──────────────────┘    └──────────────────┘               │    │
│  │                     ↓                                         │    │
│  │              Data Cleaning Pipeline                           │    │
│  │         (67.8% retention rate)                               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              STAGE 2: CONTINUED PRE-TRAINING                 │    │
│  │                                                               │    │
│  │  Base: unsloth/Meta-Llama-3.1-8B                            │    │
│  │  Method: LoRA (rank=128, alpha=32)                          │    │
│  │  Hardware: NVIDIA A100 80GB                                  │    │
│  │  Framework: Unsloth                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │            STAGE 3: INSTRUCTION FINE-TUNING                  │    │
│  │                                                               │    │
│  │  Dataset: Alif Urdu-instruct                                 │    │
│  │  Format: Llama-3 chat template                               │    │
│  │  System Prompt: Urdu-speaking assistant                      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    QALB-1.0-8B-INSTRUCT                      │    │
│  │                                                               │    │
│  │                   Overall Score: 90.34                        │    │
│  │                   Urdu Purity: 95.31%                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Prompt Format

Qalb uses the official **Llama-3 chat template** with distinct control tokens:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

### Default System Prompt (Urdu)

```
آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔
```

**Translation**: "You are a helpful and harmless AI assistant. You provide correct answers to questions in Urdu."

## 🛠️ Model Variants

| Variant | Platform | Size | Quantization |
|---------|----------|------|--------------|
| Qalb-1.0-8B-Instruct | Hugging Face | 8B | BF16 (Full) |
| qalb:8b-instruct-fp16 | Ollama | 16GB | FP16 |
| Quantized versions | Hugging Face | Various | 4-bit, GGUF |

## 🔗 Model Tree

```
unsloth/Meta-Llama-3.1-8B (Base Model)
         │
         ├── Continued Pre-training (1.97B tokens)
         │
         ├── Fine-tuning (Alif Urdu-instruct)
         │
         └── enstazao/Qalb-1.0-8B-Instruct
                    │
                    ├── Finetunes (2 models)
                    │
                    └── Quantizations (3 models)
```

## ⚙️ Inference Parameters

### Recommended Settings

| Parameter | Value |
|-----------|-------|
| **max_new_tokens** | 256 |
| **temperature** | 0.1 |
| **top_p** | 0.9 |
| **repetition_penalty** | 1.1 |
| **do_sample** | True |

### Stop Tokens

```python
eos_token_id = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]
```
