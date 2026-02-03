# Qalb Glossary & Key Terms

## 📚 Model & Architecture Terms

### Qalb (قلب)
**Definition**: The name of the Urdu LLM, meaning "heart" in Urdu. Represents the largest state-of-the-art Urdu Large Language Model designed for 230M+ speakers.

### LLaMA (Large Language Model Meta AI)
**Definition**: Foundation model developed by Meta AI. Qalb is built on LLaMA 3.1 8B as the base model.

### LoRA (Low-Rank Adaptation)
**Definition**: An efficient fine-tuning technique that introduces trainable low-rank decomposition matrices into model layers, significantly reducing memory requirements while maintaining quality.

| LoRA Parameter | Qalb Value |
|----------------|------------|
| Rank (r) | 128 |
| Alpha | 32 |
| Trainable Parameters | ~1.18B (14.72%) |

### Transformer
**Definition**: Neural network architecture that uses self-attention mechanisms. The foundation of modern LLMs including Qalb.

### Autoregressive Language Model
**Definition**: A model that generates text one token at a time, where each new token is predicted based on all previous tokens.

## 🎓 Training Terms

### Continued Pre-training
**Definition**: A training approach that takes an existing pre-trained model and further trains it on new data. More efficient than training from scratch.

**In Qalb**: Used to extend LLaMA 3.1 8B's knowledge to Urdu using 1.97B tokens.

### Supervised Fine-Tuning (SFT)
**Definition**: Training a model on labeled instruction-response pairs to improve its ability to follow instructions.

**In Qalb**: Uses the Alif Urdu-instruct dataset.

### Catastrophic Forgetting
**Definition**: The phenomenon where a neural network forgets previously learned information when trained on new data.

**In Qalb**: Prevented by including 140M English Wikipedia tokens as a replay buffer.

### Replay Buffer
**Definition**: A technique to prevent catastrophic forgetting by including data from the original training distribution during continued training.

### Gradient Checkpointing
**Definition**: Memory optimization technique that trades computation for memory by recomputing activations during backward pass instead of storing them.

### bfloat16 (Brain Float 16)
**Definition**: A 16-bit floating-point format that maintains the range of 32-bit floats while reducing memory usage. Used for efficient training.

## 📊 Evaluation Terms

### SOTA (State-of-the-Art)
**Definition**: The highest level of development/performance achieved at a particular time. Qalb achieves SOTA on Urdu NLP tasks with 90.34 score.

### Benchmark
**Definition**: A standardized test used to compare performance of different models. Qalb was evaluated on 7 diverse Urdu benchmarks.

### Weighted Average Score
**Definition**: An average where different tasks contribute different amounts based on their importance. Qalb's overall score of 90.34 is a weighted average.

## 🔤 Language Terms

### Urdu (اردو)
**Definition**: An Indo-Aryan language spoken by 230M+ people, primarily in Pakistan and India. Written in Nastaliq script (right-to-left).

### Nastaliq Script
**Definition**: The calligraphic style used for writing Urdu, flowing from right to left. Presents unique challenges for NLP systems designed for left-to-right languages.

### Low-Resource Language
**Definition**: A language with limited digital resources (data, tools, models) available for NLP research and development. Urdu is considered low-resource despite having 230M speakers.

### Morphology
**Definition**: The study of word structure and formation. Urdu has complex morphology that poses challenges for language models.

### Code-Switching
**Definition**: Alternating between two or more languages in a single conversation. Common in Urdu-English bilingual contexts.

## 🛠️ Technical Terms

### Tokenization
**Definition**: The process of breaking text into smaller units (tokens) for processing by the model.

### Sequence Length
**Definition**: The maximum number of tokens a model can process at once. Qalb uses 2048 tokens.

### Inference
**Definition**: Using a trained model to generate predictions/outputs. Qalb supports fast inference via Unsloth.

### Quantization
**Definition**: Reducing the precision of model weights to decrease memory usage and increase speed.

| Type | Description |
|------|-------------|
| FP16 | 16-bit floating point (16GB for Qalb) |
| 4-bit | Reduced precision (~4GB for Qalb) |
| GGUF | Quantized format for efficient deployment |

### Batch Size
**Definition**: Number of training examples processed together. Qalb uses effective batch size of 128 for pre-training.

## 📈 Performance Metrics

### Accuracy
**Definition**: Percentage of correct predictions. Used in classification and QA tasks.

### Fluency
**Definition**: How natural and smooth the generated text reads. Important for Urdu generation quality.

### Urdu Purity
**Definition**: Percentage of generated text that is clean Urdu without foreign character insertion. Qalb achieves 95.31%.

## 🔧 Tools & Libraries

### Unsloth
**Definition**: An optimized training framework combining memory-efficient attention mechanisms with fast LoRA implementations. Used for training Qalb.

### crawl4ai
**Definition**: Open-source asynchronous web scraping framework optimized for LLM workflows. Used for Qalb's data collection.

### Ollama
**Definition**: Platform for running large language models locally. Qalb is available as `enstazao/qalb:8b-instruct-fp16`.

### Hugging Face
**Definition**: Platform for sharing and deploying ML models. Qalb is hosted at `enstazao/Qalb-1.0-8B-Instruct`.

### Transformers (Library)
**Definition**: Hugging Face library for working with transformer-based models. Can be used to load and run Qalb.

### BitsAndBytes
**Definition**: Library for 8-bit and 4-bit quantization in PyTorch. Used for memory-efficient Qalb inference.

## 📝 Dataset Terms

### Alif Urdu-instruct
**Definition**: The instruction-tuning dataset used for Qalb's supervised fine-tuning phase.

### Makhzan Corpus
**Definition**: Literary archive of Urdu text included in Qalb's training data.

### Rekhta
**Definition**: Digital platform for Urdu poetry and literature. Source of literary data for Qalb.

## 🎯 Task Types

### Generation
**Definition**: Creating new text based on a prompt. Score: 85.97

### Translation
**Definition**: Converting text between languages (Urdu ↔ English). Score: 94.41

### Classification
**Definition**: Categorizing text into predefined classes. Score: 96.38

### Sentiment Analysis
**Definition**: Detecting emotions/opinions in text. Score: 95.79

### Question Answering (QA)
**Definition**: Providing answers to questions based on knowledge. Score: 80.40

### Reasoning
**Definition**: Logical and commonsense inference tasks. Score: 88.59

### Ethics
**Definition**: Moral reasoning and ethical judgment tasks. Score: 90.83

## 🔢 Key Numbers

| Metric | Value |
|--------|-------|
| Total Training Tokens | 1.97 Billion |
| Urdu Tokens | 1.84 Billion |
| English Tokens | 140 Million |
| Model Parameters | 8 Billion |
| Trainable Parameters | ~1.18 Billion |
| Overall Score | 90.34 |
| Target Speakers | 230 Million |
| Urdu Purity | 95.31% |
| Data Retention Rate | 67.8% |
| Sequence Length | 2048 |
