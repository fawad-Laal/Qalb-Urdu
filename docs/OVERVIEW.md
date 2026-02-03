# Qalb - Comprehensive Overview

## What is Qalb?

**Qalb** (قلب - meaning "heart" in Urdu) is the **largest state-of-the-art Urdu Large Language Model** specifically designed to serve 230+ million Urdu speakers worldwide. Developed through systematic continued pre-training, Qalb addresses critical challenges in Urdu NLP and brings significant advancements in reasoning, fluency, and cultural alignment.

## 🎯 Why Qalb Matters

### The Problem with Urdu in AI

Before Qalb, Urdu speakers faced significant challenges:

1. **Insufficient Pre-training Data**: Base models like LLaMA-3.1 8B-Instruct showed unsatisfactory performance on Urdu tasks, generating text that native speakers found unnatural due to insufficient exposure to quality Urdu data.

2. **Inconsistent Responses**: Multilingual LLMs often produced extremely hallucinated responses and sometimes inserted foreign characters during Urdu text generation.

3. **Lack of High-Quality Datasets**: Urdu lacked reliable, instruction-tuned datasets. Existing datasets were often small, noisy, or lacked diversity.

4. **Translation Limitations**: Direct translation resulted in fluency loss and cultural misalignment, highlighting the need for native Urdu data generation.

5. **Script Challenges**: Urdu's right-to-left Nastaliq script conflicts with left-to-right reasoning tasks.

6. **Cultural Alignment Issues**: Existing safety frameworks failed to align with regional requirements and cultural nuances.

### The Qalb Solution

Qalb addresses these challenges through:

- **Deep Urdu Understanding**: Pre-trained on diverse mix of news, literature, government documents, and social media
- **State-of-the-Art Performance**: Outperforms previous models on 6 out of 7 benchmarks
- **Ethical & Safe**: Fine-tuned to be helpful, harmless, and honest
- **Reasoning Capable**: Excellent performance on logical reasoning and commonsense tasks
- **Bilingual Proficiency**: Retains strong English capabilities while excelling in Urdu

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| **Total Training Tokens** | 1.97 Billion |
| **Urdu Tokens** | 1.84 Billion |
| **English Tokens** | 140 Million |
| **Overall SOTA Score** | 90.34 |
| **Target Speakers** | 230 Million |
| **Urdu Purity** | 95.31% |
| **Model Parameters** | 8 Billion |

## 🏗️ Model Foundation

- **Base Model**: Meta LLaMA 3.1 8B
- **Architecture**: Transformer-based autoregressive language model
- **Training Method**: Continued pre-training + Supervised fine-tuning
- **Fine-tuning Dataset**: Alif Urdu-instruct dataset
- **License**: Apache 2.0

## 🌟 Key Features

### 1. State-of-the-Art Performance
Outperforms previous best models (Alif-1.0 and LLaMA-3.1 Base) on 6 out of 7 benchmarks with an overall score of 90.34.

### 2. Deep Urdu Understanding
Pre-trained on a diverse mix of:
- News archives (BBC Urdu, Jang, Dunya News, UrduPoint)
- Classical and contemporary literature (Rekhta, Makhzan corpus)
- Government documents
- Social media content

### 3. Ethical & Safe Design
Fine-tuned to provide helpful, harmless, and honest responses, refusing to generate toxic or misleading content.

### 4. Strong Reasoning Capabilities
Excellent performance on:
- Logical reasoning
- Mathematical word problems
- Commonsense tasks in Urdu

### 5. Bilingual Proficiency
Retains strong English capabilities while excelling in Urdu, making it ideal for:
- Translation tasks
- Code-switching scenarios
- Cross-lingual applications

## 🎯 Use Cases

1. **Natural Language Interfaces**: Chatbots and virtual assistants in Urdu
2. **Educational Technology**: Learning tools for Urdu-speaking communities
3. **Literature Preservation**: Digitization of Urdu literature
4. **Translation Services**: Urdu-English bidirectional translation
5. **Cultural Research**: Linguistic and cultural studies
6. **Content Generation**: Creative writing and factual content in Urdu
7. **Sentiment Analysis**: Understanding public opinion in Urdu media

## 👥 Development Team

| Author | Affiliation |
|--------|-------------|
| Muhammad Taimoor Hassan | Auburn University, USA |
| Jawad Ahmed | BHT Berlin, Germany |
| Muhammad Awais | BTU Cottbus, Germany |

## 📅 Timeline

- **Research Submission**: January 13, 2026
- **arXiv Publication**: January 2026
- **Model Release**: January 2026

## 🔗 Official Resources

| Resource | Link |
|----------|------|
| Hugging Face | https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct |
| Ollama | https://ollama.com/enstazao/qalb:8b-instruct-fp16 |
| arXiv Paper | https://arxiv.org/abs/2601.08141 |
| Blog Post | https://taimoor.xyz/blog/qalb-release.html |
