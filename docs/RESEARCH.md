# Qalb Research Paper Summary

## 📄 Paper Information

| Field | Value |
|-------|-------|
| **Title** | Qalb: Largest State-of-the-Art Urdu Large Language Model for 230M Speakers with Systematic Continued Pre-training |
| **Authors** | Muhammad Taimoor Hassan, Jawad Ahmed, Muhammad Awais |
| **Affiliations** | Auburn University (USA), BHT Berlin (Germany), BTU Cottbus (Germany) |
| **arXiv ID** | 2601.08141 |
| **Published** | January 13, 2026 |
| **Categories** | cs.CL (Computation and Language), cs.AI, cs.LG |
| **DOI** | 10.48550/arXiv.2601.08141 |

## 📖 Abstract

Despite remarkable progress in large language models, Urdu—a language spoken by over **230 million people**—remains critically underrepresented in modern NLP systems. Existing multilingual models demonstrate poor performance on Urdu-specific tasks, struggling with:

- Complex morphology
- Right-to-left Nastaliq script
- Rich literary traditions

The paper introduces **Qalb**, an Urdu language model developed through a two-stage approach:

1. **Continued pre-training** on 1.97 billion tokens (1.84B Urdu + 140M English)
2. **Supervised fine-tuning** on the Alif Urdu-instruct dataset

### Key Results

- **90.34** weighted average score
- **+3.24 points** over previous SOTA (Alif-1.0-Instruct: 87.1)
- **+44.64 points** over base model (LLaMA-3.1 8B-Instruct: 45.7)
- State-of-the-art on 6/7 evaluation tasks

## 🔬 Research Contributions

### 1. Problem Identification

The paper identifies critical challenges in Urdu NLP:

| Challenge | Description |
|-----------|-------------|
| **Insufficient Pre-training** | Base models lack quality Urdu exposure |
| **Inconsistent Responses** | Hallucinations and foreign character insertion |
| **Dataset Scarcity** | Small, noisy, non-diverse Urdu datasets |
| **Translation Limitations** | Loss of fluency and cultural misalignment |
| **Script Conflicts** | RTL Nastaliq vs LTR reasoning tasks |
| **Cultural Misalignment** | Safety frameworks ignore regional needs |

### 2. Novel Methodology

**Two-Stage Approach:**

```
Stage 1: Continued Pre-training
├── 1.84B Urdu tokens (diverse sources)
├── 140M English tokens (replay buffer)
└── LoRA-based efficient training

Stage 2: Instruction Fine-tuning
├── Alif Urdu-instruct dataset
├── Llama-3 chat template
└── Urdu assistant persona
```

### 3. Dataset Contribution

**Comprehensive Data Curation:**

| Source | Content |
|--------|---------|
| News & Media | BBC Urdu, Jang, Dunya News, UrduPoint |
| Literature | Rekhta, Makhzan corpus, Islamic books |
| Government | Official documents, publications |
| Social Media | Contemporary language usage |
| English | Wikipedia (catastrophic forgetting prevention) |

**Data Pipeline:**
- Navigation removal
- Quality filtering (>10 words, >50 chars)
- Hash-based deduplication
- Junk/artifact removal
- **67.8% retention rate**

### 4. Efficient Training

**Cost-Effective Approach:**

| Aspect | Details |
|--------|---------|
| Hardware | Single NVIDIA A100 80GB |
| Method | LoRA (rank=128, alpha=32) |
| Parameters | ~1.18B trainable (14.72% of base) |
| Framework | Unsloth (memory-efficient) |

### 5. Comprehensive Evaluation

**7 Diverse Tasks:**

1. Generation
2. Ethics
3. Question Answering
4. Reasoning
5. Translation
6. Classification
7. Sentiment Analysis

## 📊 Experimental Results

### Performance Comparison

| Model | Gen | Trans | Ethics | Reason | QA | Class | Sent | **Overall** |
|-------|-----|-------|--------|--------|-----|-------|------|-------------|
| LLaMA-3.1-8B | 42.8 | 58.9 | 27.3 | 45.6 | 30.5 | 61.4 | 54.3 | 45.7 |
| Alif-1.0-8B | 90.2 | 89.3 | 85.7 | 83.5 | 73.8 | 93.9 | 94.3 | 87.1 |
| **Qalb** | 85.97 | **94.41** | **90.83** | **88.59** | **80.40** | **96.38** | **95.79** | **90.34** |

### Key Findings

1. **Massive improvement over base**: +44.64 points demonstrates critical importance of continued pre-training

2. **Outperforms Alif on 6/7 tasks**:
   - Largest gains: QA (+6.6), Translation (+5.11), Reasoning (+5.09)
   - Substantial improvements: Classification (+2.48), Sentiment (+1.49)

3. **State-of-the-art establishment**: New benchmarks across multiple Urdu NLP tasks

## 💡 Key Insights

### Why Continued Pre-training Works

> "Continued pre-training on diverse, high-quality language data, combined with targeted instruction fine-tuning, effectively adapts foundation models to low-resource languages."

### English Data as Replay Buffer

The 140M English tokens from Wikipedia:
- Prevents catastrophic forgetting
- Maintains general reasoning capabilities
- Preserves original English performance

### LoRA Efficiency

Low-Rank Adaptation enables:
- Training on single GPU
- Reduced memory requirements
- Maintained model quality
- Cost-effective approach

## 🌍 Impact & Significance

### For Urdu Speakers (230M+)

- Natural language interfaces in Urdu
- Educational technology accessibility
- Literature preservation and digitization
- Cross-lingual applications

### For Low-Resource Languages

The methodology is **reproducible** and provides:
- Framework for adapting foundation models
- Data curation best practices
- Efficient training approaches
- Comprehensive evaluation protocols

### For AI Research

- Demonstrates importance of language-specific pre-training
- Shows effectiveness of LoRA for language adaptation
- Provides benchmark for Urdu NLP
- Contributes to multilingual AI accessibility

## 🔮 Future Directions

The paper outlines future work:

1. **Data Expansion**: Gather more diverse Urdu data
2. **Technique Enhancement**: Apply model merging and RL techniques
3. **Evaluation Extension**: Additional Urdu-specific task benchmarks
4. **Open Source**: Release weights and datasets to community

## 📚 Citation

```bibtex
@article{qalb2025,
  title={Qalb: Largest State-of-the-Art Urdu Large Language Model for 230M Speakers with Systematic Continued Pre-training},
  author={Hassan, Muhammad Taimoor and Ahmed, Jawad and Awais, Muhammad},
  journal={arXiv preprint arXiv:2601.08141},
  year={2026},
  eprint={2601.08141},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2601.08141},
  doi={10.48550/arXiv.2601.08141}
}
```

## 🔗 Resources

| Resource | Link |
|----------|------|
| arXiv Paper | https://arxiv.org/abs/2601.08141 |
| PDF | https://arxiv.org/pdf/2601.08141 |
| HTML | https://arxiv.org/html/2601.08141v1 |
| Hugging Face | https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct |
| Ollama | https://ollama.com/enstazao/qalb:8b-instruct-fp16 |

## 🏆 Acknowledgments

The research acknowledges:
- Open-source community
- Unsloth library
- Meta's LLaMA models
- Alif team (Urdu instruction dataset)
- Urdu-speaking community
