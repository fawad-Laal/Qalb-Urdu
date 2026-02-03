# QALB Urdu AI Testing Project

> **Testing and Evaluation Framework for Qalb - The State-of-the-Art Urdu Large Language Model**

## 🎯 Project Overview

This project is dedicated to testing, evaluating, and exploring the capabilities of **Qalb**, the largest state-of-the-art Urdu Large Language Model designed for 230+ million Urdu speakers worldwide.

## 📋 Quick Links

| Resource | Link |
|----------|------|
| 🐙 GitHub | [fawad-Laal/Qalb-Urdu](https://github.com/fawad-Laal/Qalb-Urdu) |
| 🤗 Hugging Face | [enstazao/Qalb-1.0-8B-Instruct](https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct) |
| 🦙 Ollama | [enstazao/qalb:8b-instruct-fp16](https://ollama.com/enstazao/qalb:8b-instruct-fp16) |
| 📄 arXiv Paper | [2601.08141](https://arxiv.org/abs/2601.08141) |
| 📝 Blog Post | [taimoor.xyz/blog/qalb-release](https://taimoor.xyz/blog/qalb-release.html) |

## 🚀 Getting Started

### Using Ollama (Recommended for Local Testing)

```bash
# Pull and run the model
ollama run enstazao/qalb:8b-instruct-fp16
```

### Using Python with Ollama

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

## 📊 Model Performance

| Task | Qalb Score | Previous SOTA (Alif) | LLaMA-3.1 Base |
|------|------------|---------------------|----------------|
| **Overall** | **90.34** | 87.1 | 45.7 |
| Translation | 94.41 | 89.3 | 58.9 |
| Classification | 96.38 | 93.9 | 61.4 |
| Sentiment Analysis | 95.79 | 94.3 | 54.3 |
| Ethics | 90.83 | 85.7 | 27.3 |
| Reasoning | 88.59 | 83.5 | 45.6 |
| QA | 80.40 | 73.8 | 30.5 |
| Generation | 85.97 | 90.2 | 42.8 |

## 📁 Project Structure

```
Qalb/
├── README.md                    # This file
├── docs/
│   ├── OVERVIEW.md             # Comprehensive Qalb overview
│   ├── ARCHITECTURE.md         # Technical architecture details
│   ├── TRAINING.md             # Training methodology
│   ├── BENCHMARKS.md           # Performance benchmarks
│   ├── USAGE.md                # Usage guide and examples
│   └── RESEARCH.md             # Research paper summary
├── tests/                       # Test scripts
├── examples/                    # Example code
└── notebooks/                   # Jupyter notebooks
```

## 👤 Project Owner

- **Name:** Fawad Hussain
- **Email:** syedfawadhussain@gmail.com

## 📜 License

This project follows the Apache 2.0 license as per the original Qalb model.

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
