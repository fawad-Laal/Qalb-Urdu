# QALB Urdu AI - Independent Evaluation Framework

> **Open-Source Testing and Evaluation Framework for Qalb - The State-of-the-Art Urdu Large Language Model**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/downloads/)

## 📖 Overview

This repository contains an **independent applied evaluation** of the [Qalb Urdu AI model](https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct), conducted to assess practical capabilities for everyday usage scenarios. The evaluation covers **320 test cases** across **8 bilingual categories** over **4 iterative assessment rounds**.

### Key Results

| Metric | Score |
|--------|-------|
| **Peak Score (Round 3)** | 79.2/100 |
| **Final Score (Round 4)** | 77.7/100 |
| **Test Cases** | 320 |
| **Categories** | 8 Bilingual |
| **Evaluation Rounds** | 4 |

## 📋 Quick Links

| Resource | Link |
|----------|------|
| 📊 **Evaluation Report (PDF)** | [QALB-Final-Evaluation-04022026.pdf](reports/QALB-Final-Evaluation-04022026.pdf) |
| 📝 **Evaluation Report (Markdown)** | [FINAL_EVALUATION_REPORT.md](reports/FINAL_EVALUATION_REPORT_20260204_081818.md) |
| 🐙 **GitHub Repository** | [fawad-Laal/qalb-urdu](https://github.com/fawad-Laal/qalb-urdu) |
| 🤗 **Qalb on Hugging Face** | [enstazao/Qalb-1.0-8B-Instruct](https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct) |
| 🦙 **Qalb on Ollama** | [enstazao/qalb:8b-instruct-fp16](https://ollama.com/enstazao/qalb:8b-instruct-fp16) |
| 📄 **arXiv Paper** | [2601.08141](https://arxiv.org/abs/2601.08141) |

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+**
- **Ollama** (for running Qalb model locally)
- **~16GB RAM** recommended for 8B parameter model
- **GPU (Optional)**: CUDA-compatible GPU for faster inference

### Step 1: Clone the Repository

```bash
git clone https://github.com/fawad-Laal/qalb-urdu.git
cd qalb-urdu
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama & Pull Qalb Model

```bash
# Install Ollama from https://ollama.com/download
# Then pull the Qalb model:
ollama pull enstazao/qalb:8b-instruct-fp16
```

### Step 5: Set Up Environment Variables (For Report Generation)

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here  # Optional: Only for markdown report generation with GPT
```

---

## 🧪 Running the Evaluation Tests

### Quick Start - Run All Tests

```bash
# Make sure Ollama is running with Qalb model
ollama serve  # In a separate terminal

# Run the complete test suite
python scripts/test_runner.py
```

### Test Categories

The evaluation covers 8 categories in both **Urdu Script** and **Roman Urdu**:

| Category | Description | Test Count |
|----------|-------------|------------|
| Question Answering | Factual knowledge and comprehension | 40 |
| Mathematics | Arithmetic and mathematical reasoning | 40 |
| Reasoning | Logical and commonsense reasoning | 40 |
| Translation | English↔Urdu translation | 40 |
| Summarization | Text summarization tasks | 40 |
| Creative Writing | Poetry, stories, essays | 40 |
| Conversation | Dialogue and chat | 40 |
| Instruction Following | Following complex instructions | 40 |

### Test Output

Results are saved to:
- `data/baseline/combined_results.json` - Full test results
- `data/checkpoints/` - Checkpoint files for resuming interrupted runs

---

## 📊 Generating Reports

### Generate PDF Academic Report

```bash
python scripts/generate_academic_pdf.py
```

This generates a professional PDF report with:
- Executive summary and key findings
- Charts and visualizations (score evolution, category performance)
- Category-by-category analysis
- Urdu text examples rendered with Amiri font
- 160 annotated examples in appendices

### Generate Markdown Report (Requires OpenAI API)

```bash
python scripts/generate_final_report.py
```

This uses GPT-5-mini to analyze test results and generate a comprehensive markdown report.

---

## 📁 Project Structure

```
qalb-urdu/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Project configuration
├── .env                                # Environment variables (create this)
│
├── data/
│   ├── baseline/
│   │   ├── urdu_script_tests.json     # Urdu script test cases
│   │   ├── roman_urdu_tests.json      # Roman Urdu test cases
│   │   └── combined_results.json      # Test results
│   ├── checkpoints/                    # Test run checkpoints
│   └── evaluation/                     # Evaluation data
│
├── docs/
│   ├── OVERVIEW.md                     # Qalb model overview
│   ├── ARCHITECTURE.md                 # Technical architecture
│   ├── BENCHMARKS.md                   # Performance benchmarks
│   ├── ROUND_2_ANALYSIS.md            # Round 2 analysis
│   ├── ROUND_3_ANALYSIS.md            # Round 3 analysis
│   └── ROUND_4_ANALYSIS.md            # Round 4 analysis
│
├── fonts/
│   └── Amiri/                          # Urdu font for PDF generation
│
├── reports/
│   ├── QALB-Final-Evaluation-04022026.pdf  # Final PDF report
│   ├── FINAL_EVALUATION_REPORT_*.md        # Final markdown report
│   └── archive/                             # Archived old reports
│
├── scripts/
│   ├── test_runner.py                  # Main test execution script
│   ├── generate_final_report.py        # Markdown report generator (GPT)
│   ├── generate_academic_pdf.py        # PDF report generator
│   └── analyze_*.py                    # Analysis scripts
│
├── tests/
│   ├── test_cases.py                   # Test case definitions
│   └── baseline/                       # Baseline test data
│
└── examples/
    ├── ollama_example.py               # Ollama usage example
    └── transformers_example.py         # Transformers usage example
```

---

## 🔧 Customizing Tests

### Adding New Test Cases

Edit `data/baseline/urdu_script_tests.json` or `roman_urdu_tests.json`:

```json
{
  "id": "qa_new_001",
  "category": "question_answering",
  "prompt": "پاکستان کا قومی پھول کون سا ہے؟",
  "expected_keywords": ["چنبیلی", "jasmine"],
  "difficulty": "easy"
}
```

### Test Runner Configuration

Key settings in `scripts/test_runner.py`:

```python
MODEL_NAME = "enstazao/qalb:8b-instruct-fp16"  # Model to test
MAX_RETRIES = 3                                  # Retry failed tests
TIMEOUT_SECONDS = 120                            # Per-test timeout
```

---

## 📈 Evaluation Results Summary

### Performance by Round

| Round | Score | Key Changes |
|-------|-------|-------------|
| **Round 1** | 74.4/100 | Baseline with standard keyword matching |
| **Round 2** | 78.3/100 | +3.9 - Improved Urdu-Roman keyword coverage |
| **Round 3** | 79.2/100 | +0.9 - Peak with refined math evaluation |
| **Round 4** | 77.7/100 | -1.5 - Regression from keyword dilution |

### Strengths Identified
- ✅ Translation tasks: ~86% adequacy/fluency
- ✅ Summarization: ~82% on ROUGE-informed evaluations
- ✅ Consistent bilingual performance (Urdu + Roman)

### Areas for Improvement
- ⚠️ Mathematical reasoning: ~64%
- ⚠️ Multi-step logical inference
- ⚠️ Numeric formatting consistency

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-tests`)
3. Commit your changes (`git commit -m 'Add new test cases'`)
4. Push to the branch (`git push origin feature/new-tests`)
5. Open a Pull Request

---

## 👤 Author

**Fawad Hussain Syed**
- 🌐 Website: [fawadhs.dev](https://fawadhs.dev)
- 📧 Email: [fawad@fawadhs.dev](mailto:fawad@fawadhs.dev)
- 🐙 GitHub: [@fawad-Laal](https://github.com/fawad-Laal)

---

## 📜 License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Qalb Development Team**: Muhammad Taimoor Hassan, Jawad Ahmed, Muhammad Awais
- **Model**: [enstazao/Qalb-1.0-8B-Instruct](https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct)
- **Base Model**: Meta LLaMA 3.1 8B

---

## 📚 Citation

If you use this evaluation framework, please cite:

```bibtex
@misc{qalb-evaluation-2026,
  author = {Syed, Fawad Hussain},
  title = {QALB Urdu AI Independent Evaluation Framework},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/fawad-Laal/qalb-urdu}
}
```

For the Qalb model itself:

```bibtex
@article{qalb2026,
  title={Qalb: Largest State-of-the-Art Urdu Large Language Model for 230M Speakers},
  author={Hassan, Muhammad Taimoor and Ahmed, Jawad and Awais, Muhammad},
  journal={arXiv preprint arXiv:2601.08141},
  year={2026}
}
```
