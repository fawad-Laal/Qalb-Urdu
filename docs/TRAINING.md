# Qalb Training Methodology

## 📋 Overview

Qalb was developed through a systematic **two-stage approach**:
1. **Continued Pre-training** on 1.97 billion tokens
2. **Supervised Fine-tuning** on the Alif Urdu-instruct dataset

This approach leverages the general linguistic knowledge already encoded in a pre-trained model and extends it with target language data—particularly effective for low-resource languages like Urdu.

## 📊 Dataset Construction

### Data Collection Tool

The team utilized **crawl4ai**—an open-source, asynchronous web scraping framework optimized for LLM workflows:

- **Technology**: Headless browser architecture via Playwright
- **Capability**: Renders JavaScript-heavy pages for dynamic content
- **Output**: 9.09 GB of text data
- **Final Dataset**: ~1.97 billion tokens across 5.04 million documents

### Urdu Corpus (1.84 Billion Tokens)

| Source Category | Description | Sources |
|-----------------|-------------|---------|
| **News & Media** | 61+ million words | BBC Urdu, Jang, Dunya News, UrduPoint |
| **Literature & Religion** | Extensive volumes | Islamic Urdu Books, Rekhta, Makhzan corpus |
| **Specialized Domains** | Domain-specific content | Sports, Entertainment, Health |
| **Government Documents** | Official publications | Government documents and publications |
| **Social Media** | Contemporary language | Curated social media content |

### English Corpus (140 Million Tokens)

- **Source**: Wikipedia
- **Purpose**: Replay buffer to prevent catastrophic forgetting
- **Goal**: Maintain general reasoning capabilities and original English performance

## 🧹 Data Cleaning Pipeline

A rigorous multi-stage cleaning process ensured data quality:

### Stage 1: Navigation Removal
- Stripped hundreds of identified footer and header patterns
- Removed website navigation elements

### Stage 2: Filtering
- Removed records with fewer than 10 words
- Eliminated content with less than 50 characters
- Filtered noise and low-quality content

### Stage 3: Deduplication
- Applied hash-based detection
- Removed duplicate articles across different news aggregators

### Stage 4: Junk Removal
- Cleaned numeric artifacts
- Removed timestamps
- Eliminated non-Urdu metadata

### Results
- **Retention Rate**: ~67.8%
- **Quality**: Only high-quality semantic content remained

## 🎓 Stage 1: Continued Pre-Training

### Why Continued Pre-Training?

Unlike training from scratch (requiring massive computational resources), continued pre-training:
- Leverages existing linguistic knowledge
- Extends capabilities with target language data
- Requires significantly less compute
- Particularly effective for low-resource languages

### Configuration

| Parameter | Value |
|-----------|-------|
| **Base Model** | unsloth/Meta-Llama-3.1-8B |
| **Method** | Low-Rank Adaptation (LoRA) |
| **Hardware** | Single NVIDIA A100 80GB |
| **Framework** | Unsloth library |
| **Precision** | bfloat16 with gradient checkpointing |
| **Optimizer** | AdamW-8bit |
| **Learning Rate Schedule** | Cosine with warmup ratio 0.05 |
| **LoRA Rank (r)** | 128 |
| **LoRA Alpha** | 32 |
| **Trainable Parameters** | ~1.18B (~14.72% of base) |
| **Effective Batch Size** | 128 |
| **Sequence Length** | 2048 |

### LoRA Benefits

Low-Rank Adaptation introduces trainable low-rank decomposition matrices into the model's layers:
- ✅ Reduces memory requirements
- ✅ Lowers computational costs
- ✅ Maintains model quality
- ✅ Only updates ~14.72% of parameters

## 🎯 Stage 2: Instruction Fine-Tuning

### Dataset
- **Name**: Alif Urdu-instruct dataset
- **Purpose**: Supervised fine-tuning for instruction following
- **Goal**: Make model function as helpful Urdu-speaking assistant

### Configuration

| Parameter | Value |
|-----------|-------|
| **LoRA Setup** | Same as pre-training (rank 128) |
| **Learning Rate** | 5e-5 |
| **Epochs** | 2 |
| **Batch Size** | 64 |
| **Optimizer** | AdamW-8bit |
| **Scheduling** | Linear |
| **Prompt Format** | Official Llama-3 chat template |

### System Prompt

```urdu
آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔
```

**Translation**: "You are a helpful and harmless AI assistant. You provide correct answers to questions in Urdu."

## 💡 Training Optimizations

### Unsloth Library Features

The Unsloth library provided:
- **Memory-efficient attention mechanisms**
- **Fast LoRA implementations**
- **Optimized training throughput**
- **Reduced GPU memory footprint**

### Efficiency Achievements

- ✅ Trained on single A100 GPU
- ✅ Cost-effective approach
- ✅ Maintained high quality
- ✅ Achieved state-of-the-art performance

## 📈 Training Results

### Performance Improvements

| Comparison | Improvement |
|------------|-------------|
| vs. Base LLaMA-3.1 8B-Instruct | **+44.64 points** |
| vs. Previous SOTA (Alif-1.0) | **+3.24 points** |

### Key Outcomes

- **90.34** weighted average score
- **95.31%** Urdu purity
- State-of-the-art on **6 out of 7** benchmarks
- Strong English retention (no catastrophic forgetting)

## 🔄 Training Pipeline Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA CURATION                           │
│  crawl4ai → 9.09 GB raw data → Cleaning → 1.97B tokens     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  CONTINUED PRE-TRAINING                     │
│  Meta-Llama-3.1-8B + LoRA + 1.97B tokens → Enhanced Model  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 INSTRUCTION FINE-TUNING                     │
│  Enhanced Model + Alif Urdu-instruct → Qalb-1.0-8B-Instruct│
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Reproducibility

The methodology is designed to be **reproducible** and can guide similar efforts for other underserved languages:

1. **Collect diverse target language data**
2. **Include English data as replay buffer**
3. **Apply rigorous data cleaning**
4. **Use efficient LoRA-based continued pre-training**
5. **Fine-tune on high-quality instruction dataset**
