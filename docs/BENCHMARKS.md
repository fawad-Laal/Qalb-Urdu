# Qalb Performance Benchmarks

## 📊 Evaluation Overview

Qalb was evaluated on a comprehensive Urdu evaluation suite covering **seven diverse tasks**:

1. **Generation** - Creative and factual text generation
2. **Ethics** - Moral reasoning and ethical judgment
3. **Question Answering (QA)** - Factual knowledge retrieval
4. **Reasoning** - Logical and commonsense reasoning
5. **Translation** - Urdu-English bidirectional translation
6. **Classification** - Text categorization tasks
7. **Sentiment Analysis** - Emotion and opinion detection

## 🏆 Overall Performance

| Model | Overall Score |
|-------|---------------|
| **Qalb (Ours)** | **90.34** |
| Alif-1.0-8B-Instruct (Previous SOTA) | 87.1 |
| LLaMA-3.1-8B-Instruct (Base) | 45.7 |

### Key Achievement
- **+3.24 points** over previous state-of-the-art (Alif-1.0)
- **+44.64 points** over base model (LLaMA-3.1 8B-Instruct)

## 📈 Detailed Task Performance

### Performance Comparison Table

| Task | Qalb | Alif-1.0 | LLaMA-3.1 Base | Improvement vs Alif |
|------|------|----------|----------------|---------------------|
| **Classification** | **96.38** | 93.9 | 61.4 | +2.48 |
| **Sentiment Analysis** | **95.79** | 94.3 | 54.3 | +1.49 |
| **Translation** | **94.41** | 89.3 | 58.9 | +5.11 |
| **Ethics** | **90.83** | 85.7 | 27.3 | +5.13 |
| **Reasoning** | **88.59** | 83.5 | 45.6 | +5.09 |
| **Generation** | 85.97 | **90.2** | 42.8 | -4.23 |
| **QA** | **80.40** | 73.8 | 30.5 | +6.60 |

> **Note**: Scores are on a 0-100 scale. Qalb outperforms in **6 out of 7** categories.

## 📊 Performance Visualization

### Task-by-Task Comparison

```
Classification     ████████████████████████████████████████████████░░ 96.38
                   ██████████████████████████████████████████████░░░░ 93.90 (Alif)
                   ██████████████████████████████░░░░░░░░░░░░░░░░░░░░ 61.40 (Base)

Sentiment Analysis ███████████████████████████████████████████████░░░ 95.79
                   ██████████████████████████████████████████████░░░░ 94.30 (Alif)
                   ███████████████████████████░░░░░░░░░░░░░░░░░░░░░░░ 54.30 (Base)

Translation        ██████████████████████████████████████████████░░░░ 94.41
                   ████████████████████████████████████████████░░░░░░ 89.30 (Alif)
                   █████████████████████████████░░░░░░░░░░░░░░░░░░░░░ 58.90 (Base)

Ethics             █████████████████████████████████████████████░░░░░ 90.83
                   ██████████████████████████████████████████░░░░░░░░ 85.70 (Alif)
                   █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 27.30 (Base)

Reasoning          ████████████████████████████████████████████░░░░░░ 88.59
                   █████████████████████████████████████████░░░░░░░░░ 83.50 (Alif)
                   ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 45.60 (Base)

Generation         ██████████████████████████████████████████░░░░░░░░ 85.97
                   █████████████████████████████████████████████░░░░░ 90.20 (Alif)
                   █████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 42.80 (Base)

QA                 ████████████████████████████████████████░░░░░░░░░░ 80.40
                   █████████████████████████████████████░░░░░░░░░░░░░ 73.80 (Alif)
                   ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 30.50 (Base)
```

## 🎯 Key Improvements Analysis

### Largest Gains (vs. Alif-1.0)

| Task | Improvement | Analysis |
|------|-------------|----------|
| **QA** | +6.6 points | Better factual knowledge retrieval |
| **Ethics** | +5.13 points | Improved moral reasoning |
| **Translation** | +5.11 points | Enhanced Urdu-English capabilities |
| **Reasoning** | +5.09 points | Stronger logical understanding |
| **Classification** | +2.48 points | Better text categorization |
| **Sentiment** | +1.49 points | Refined emotion detection |

### Area for Improvement

| Task | Difference | Analysis |
|------|------------|----------|
| **Generation** | -4.23 points | Alif slightly better at creative generation |

## 🔬 Massive Improvement Over Base Model

The comparison with base LLaMA-3.1 8B-Instruct demonstrates the **critical importance of continued pre-training on Urdu data**:

| Task | Base Score | Qalb Score | Improvement |
|------|------------|------------|-------------|
| Ethics | 27.3 | 90.83 | **+63.53** |
| QA | 30.5 | 80.40 | **+49.90** |
| Generation | 42.8 | 85.97 | **+43.17** |
| Reasoning | 45.6 | 88.59 | **+42.99** |
| Sentiment | 54.3 | 95.79 | **+41.49** |
| Translation | 58.9 | 94.41 | **+35.51** |
| Classification | 61.4 | 96.38 | **+34.98** |

## 📏 Quality Metrics

### Urdu Purity Score

| Metric | Value |
|--------|-------|
| **Urdu Purity** | 95.31% |

This indicates that Qalb generates clean Urdu text without:
- Foreign character insertion
- Script mixing issues
- Inconsistent text generation

## 🏅 State-of-the-Art Status

Qalb establishes **new benchmarks** across multiple Urdu NLP tasks:

- ✅ **#1** in Classification (96.38)
- ✅ **#1** in Sentiment Analysis (95.79)
- ✅ **#1** in Translation (94.41)
- ✅ **#1** in Ethics (90.83)
- ✅ **#1** in Reasoning (88.59)
- ✅ **#1** in QA (80.40)
- ⭐ **#2** in Generation (85.97)

## 📊 Summary Statistics

| Metric | Value |
|--------|-------|
| **Overall Score** | 90.34 |
| **Tasks Won** | 6/7 |
| **Avg. Improvement vs. Alif** | +3.24 |
| **Avg. Improvement vs. Base** | +44.64 |
| **Best Task** | Classification (96.38) |
| **Most Improved Task** | QA (+6.6 vs. Alif) |

## 📝 Evaluation Methodology

The evaluation was conducted using:
- Standardized Urdu benchmark suite
- Consistent evaluation metrics
- Fair comparison across models
- Weighted average scoring for overall performance
