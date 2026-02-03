# QALB Testing Roadmap 🗺️

> **Comprehensive Testing Plan for Qalb Urdu LLM using Ollama (No GPU Required)**

---

## 📋 Executive Summary

This roadmap outlines a systematic approach to test and evaluate the Qalb Urdu LLM using:
- **Ollama** for local inference (CPU-based, no GPU required)
- **UrduBench (معیار)** - The world's first standardized Urdu reasoning benchmark
- **Dual Script Testing** - Both Urdu Script (اردو) AND Roman Urdu (Urdu Roman)
- **Custom test suites** for real-world application scenarios

---

## 🎯 Testing Objectives

1. **Validate Qalb's Performance** against published benchmarks (90.34 overall score)
2. **Evaluate Reasoning Capabilities** using UrduBench standardized tests
3. **Test Dual Script Support** - Urdu Nastaliq AND Roman Urdu
4. **Assess Real-World Usability** for practical Urdu NLP applications
5. **Document Strengths & Limitations** for future development
6. **Generate Professional PDF Report** with fawadhs.dev branding

---

## 📊 Data Collection Strategy

> **CRITICAL**: All data must be collected and logged throughout every phase for final PDF report generation.

### Data Collection Points

| Phase | Data to Collect | Storage Format |
|-------|-----------------|----------------|
| **Phase 0** | System specs, model info, setup time | `data/setup_log.json` |
| **Phase 1** | All test inputs, outputs, scores, timestamps | `data/baseline/*.json` |
| **Phase 2** | UrduBench results, per-question metrics | `data/urdubench/*.json` |
| **Phase 3** | Prompting comparisons, purity scores | `data/evaluation/*.json` |
| **Phase 4** | Stress test results, performance metrics | `data/stress/*.json` |
| **Phase 5** | Aggregated stats for PDF report | `data/final_report.json` |

### Data Schema for Each Test

```json
{
  "test_id": "QA-001",
  "category": "question_answering",
  "script_type": "urdu_nastaliq | roman_urdu | mixed",
  "input": "پاکستان کا دارالحکومت کیا ہے؟",
  "expected_output": "اسلام آباد",
  "actual_output": "...",
  "is_correct": true,
  "confidence_score": 0.95,
  "response_time_seconds": 12.5,
  "tokens_generated": 45,
  "urdu_purity_score": 0.98,
  "timestamp": "2026-02-02T10:30:00Z",
  "model_version": "qalb:8b-instruct-fp16",
  "prompting_strategy": "zero-shot"
}
```

### Metrics to Track

| Metric | Description | Formula |
|--------|-------------|---------|
| **Accuracy** | % correct answers | `correct / total × 100` |
| **Urdu Purity** | % pure Urdu chars | `urdu_chars / total_chars × 100` |
| **Avg Response Time** | Mean seconds/response | `sum(times) / count` |
| **Token Efficiency** | Tokens per correct answer | `total_tokens / correct_answers` |
| **Script Preference** | Urdu vs Roman performance | `urdu_score - roman_score` |
| **Consistency** | Same output across runs | `matching_runs / total_runs × 100` |

### Data Directory Structure

```
data/
├── setup_log.json              # System & model info
├── baseline/
│   ├── urdu_script/
│   │   ├── qa_results.json
│   │   ├── sentiment_results.json
│   │   ├── translation_results.json
│   │   ├── reasoning_results.json
│   │   ├── classification_results.json
│   │   ├── generation_results.json
│   │   └── ethics_results.json
│   └── roman_urdu/
│       └── ... (same structure)
├── urdubench/
│   ├── mgsm_results.json
│   ├── math500_results.json
│   ├── commonsenseqa_results.json
│   └── openbookqa_results.json
├── evaluation/
│   ├── prompting_comparison.json
│   ├── script_comparison.json
│   └── purity_analysis.json
├── stress/
│   ├── edge_cases.json
│   ├── performance_metrics.json
│   └── variation_tests.json
└── final_report.json           # Aggregated for PDF
```

---

## 🔤 Script Testing Strategy

### Two Scripts to Test

| Script Type | Example | Use Case |
|-------------|---------|----------|
| **Urdu Nastaliq** (اردو) | کیا حال ہے؟ | Formal, literary, official |
| **Roman Urdu** (Romanized) | Kya haal hai? | Social media, texting, casual |

### Why Test Both?

- **230M+ speakers** use both scripts daily
- **Social media** predominantly uses Roman Urdu
- **Formal documents** use Nastaliq script
- **Code-switching** is extremely common
- Real-world apps must handle both

### Script Test Matrix

| Test Category | Urdu Script | Roman Urdu | Mixed |
|---------------|-------------|------------|-------|
| QA | ✅ | ✅ | ✅ |
| Translation | ✅ | ✅ | ✅ |
| Sentiment | ✅ | ✅ | ✅ |
| Reasoning | ✅ | ✅ | ✅ |
| Generation | ✅ | ✅ | ✅ |
| Classification | ✅ | ✅ | ✅ |
| Ethics | ✅ | ✅ | ✅ |

---

## 🔧 Phase 0: Environment Setup (Day 1)

### Prerequisites Checklist

| Requirement | Minimum | Recommended | Status |
|-------------|---------|-------------|--------|
| **RAM** | 16 GB | 32 GB | ⬜ |
| **Storage** | 20 GB free | 50 GB free | ⬜ |
| **OS** | Windows 10+ | Windows 11 | ⬜ |
| **Python** | 3.9+ | 3.11 | ⬜ |
| **Ollama** | Latest | Latest | ⬜ |

### Setup Steps

```powershell
# Step 1: Install Ollama
# Download from: https://ollama.com/download
# Run installer and restart terminal

# Step 2: Verify Ollama installation
ollama --version

# Step 3: Pull Qalb model (16GB download)
ollama pull enstazao/qalb:8b-instruct-fp16

# Step 4: Quick test - Urdu Script
ollama run enstazao/qalb:8b-instruct-fp16 "پاکستان کا دارالحکومت کیا ہے؟"

# Step 5: Quick test - Roman Urdu
ollama run enstazao/qalb:8b-instruct-fp16 "Pakistan ka darul hakoomat kya hai?"

# Step 6: Setup Python environment
cd C:\Users\Hussain\Fawad-Software-Projects\Qalb
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Alternative: Quantized Model (Lower RAM)

```powershell
# Use 4-bit quantized version (~4-5GB) if RAM is limited
ollama pull enstazao/qalb:8b-instruct-q4_0
```

---

## 📊 Phase 1: Baseline Testing (Days 2-4)

### 1.1 Qalb's Original 7 Benchmarks

| Task | Qalb Score | Priority | Urdu | Roman |
|------|------------|----------|------|-------|
| Classification | 96.38 | 🔴 High | 20 tests | 20 tests |
| Sentiment Analysis | 95.79 | 🔴 High | 20 tests | 20 tests |
| Translation | 94.41 | 🔴 High | 20 tests | 20 tests |
| Ethics | 90.83 | 🟡 Medium | 20 tests | 20 tests |
| Reasoning | 88.59 | 🔴 High | 20 tests | 20 tests |
| Generation | 85.97 | 🟡 Medium | 20 tests | 20 tests |
| QA | 80.40 | 🔴 High | 20 tests | 20 tests |

**Total: 280 tests (140 Urdu Script + 140 Roman Urdu)**

### 1.2 Sample Test Cases - Dual Script

#### Question Answering (QA)

| ID | Urdu Script | Roman Urdu |
|----|-------------|------------|
| QA-001 | پاکستان کا قومی کھیل کیا ہے؟ | Pakistan ka qaumi khel kya hai? |
| QA-002 | قائد اعظم کب پیدا ہوئے؟ | Quaid-e-Azam kab paida huay? |
| QA-003 | اردو کتنے لوگ بولتے ہیں؟ | Urdu kitne log bolte hain? |

#### Sentiment Analysis

| ID | Urdu Script | Roman Urdu | Expected |
|----|-------------|------------|----------|
| SENT-001 | آج کا دن بہت اچھا گزرا | Aaj ka din bohat acha guzra | Positive |
| SENT-002 | یہ فلم بہت بری تھی | Ye film bohat buri thi | Negative |
| SENT-003 | کھانا ٹھیک ٹھاک تھا | Khana theek thaak tha | Neutral |

#### Translation

| ID | Input (Urdu) | Input (Roman) | Expected Output |
|----|--------------|---------------|-----------------|
| TRANS-001 | محنت کامیابی کی کنجی ہے | Mehnat kamyabi ki kunji hai | Hard work is the key to success |
| TRANS-002 | علم نور ہے | Ilm noor hai | Knowledge is light |

#### Reasoning

| ID | Urdu Script | Roman Urdu |
|----|-------------|------------|
| REASON-001 | اگر علی کے پاس 10 سیب ہیں اور وہ 3 دے دیتا ہے، کتنے بچے؟ | Agar Ali ke paas 10 seb hain aur wo 3 de deta hai, kitne bache? |
| REASON-002 | ایک درجن میں کتنے انڈے ہوتے ہیں؟ | Ek darjan mein kitne anday hote hain? |

#### Generation

| ID | Urdu Script Prompt | Roman Urdu Prompt |
|----|-------------------|-------------------|
| GEN-001 | پاکستان پر ایک پیراگراف لکھیں | Pakistan par ek paragraph likhein |
| GEN-002 | موسم بہار پر چار سطریں لکھیں | Mausam bahar par 4 satrain likhein |

---

## 🏆 Phase 2: UrduBench Integration (Days 5-8)

### About UrduBench (معیار)

| Attribute | Details |
|-----------|---------|
| **Paper** | [arXiv:2601.21000](https://arxiv.org/abs/2601.21000) |
| **Authors** | Muhammad Ali Shafique, Areej Mehboob, Layba Fiaz, et al. |
| **Purpose** | World's first standardized Urdu reasoning benchmark |
| **Methodology** | Contextually ensembled translations with human-in-the-loop |

### UrduBench Datasets

| Dataset | Type | Tests | Difficulty |
|---------|------|-------|------------|
| **MGSM-Urdu** | Math Reasoning | 250 | Medium-Hard |
| **MATH-500-Urdu** | Advanced Math | 500 | Hard |
| **CommonSenseQA-Urdu** | Common Sense | 1,221 | Easy-Medium |
| **OpenBookQA-Urdu** | Open Knowledge | 500 | Medium |

### UrduBench + Roman Urdu Extension

We'll create Roman Urdu versions of key UrduBench tests:

| Original | Roman Urdu Conversion |
|----------|----------------------|
| MGSM-Urdu (50 samples) | MGSM-Roman (50 samples) |
| CommonSenseQA (50 samples) | CSQA-Roman (50 samples) |

### Why UrduBench Matters

✅ **Context Preserved** - Not naive machine translation  
✅ **Logic Intact** - Mathematical & symbolic structure maintained  
✅ **Culturally Validated** - Native speaker verification  
✅ **No MT Artifacts** - Clean, natural Urdu  

---

## 🔬 Phase 3: Deep Evaluation (Days 9-13)

### 3.1 Evaluation Dimensions

| Dimension | Description | Tests |
|-----------|-------------|-------|
| **Script Performance** | Urdu vs Roman Urdu accuracy | Compare scores |
| **Difficulty Levels** | Easy → Medium → Hard → Expert | Stratified analysis |
| **Prompting Strategies** | Zero-shot, few-shot, CoT | 3 strategies × all tests |
| **Language Consistency** | Urdu purity in responses | Measure mixing |
| **Code-Switching** | Mixed Urdu-Roman-English | Special test set |

### 3.2 Prompting Strategies

| Strategy | Urdu Example | Roman Example |
|----------|--------------|---------------|
| **Zero-shot** | سوال کا جواب دیں | Sawal ka jawab dein |
| **Few-shot** | مثالیں دیکھیں اور جواب دیں | Misalein dekhein aur jawab dein |
| **Chain-of-Thought** | قدم بہ قدم سوچیں | Qadam ba qadam sochein |

### 3.3 Code-Switching Test Cases

Real-world Urdu often mixes scripts and languages:

| ID | Mixed Input | Type |
|----|-------------|------|
| MIX-001 | Mujhe یہ book chahiye | Roman + Urdu + English |
| MIX-002 | کل meeting ہے office میں | Urdu + English |
| MIX-003 | Yaar, یہ کام bohat mushkil hai | Roman + Urdu + Roman |

### 3.4 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Accuracy** | Correct answers | >85% |
| **Urdu Purity** | Pure Urdu output (no foreign chars) | >90% |
| **Roman Understanding** | Correctly interprets Roman Urdu | >80% |
| **Response Consistency** | Same answer across runs | >95% |
| **Response Time (CPU)** | Seconds per response | <60s |

---

## 🧪 Phase 4: Stress Testing (Days 14-16)

### 4.1 Edge Cases by Script

| Test Type | Urdu Script | Roman Urdu |
|-----------|-------------|------------|
| **Long Context** | 1000+ word prompts | 1000+ word prompts |
| **Ambiguous** | ہم نے ان کو دیکھا | Hum ne un ko dekha |
| **Informal** | کیا حال چال؟ | Kya haal chaal? |
| **Slang** | یار بہت مزے کی بات ہے | Yaar bohat maze ki baat hai |
| **Technical** | مشین لرننگ | Machine learning |

### 4.2 Roman Urdu Variations

Test different Romanization styles:

| Standard | Variation 1 | Variation 2 | Variation 3 |
|----------|-------------|-------------|-------------|
| kya | kia | kiya | kyaa |
| hai | he | hey | hay |
| mein | main | mien | me |
| acha | achchha | achha | accha |
| bohat | bohut | bahut | buhat |

### 4.3 Performance Benchmarks (CPU)

| Metric | FP16 Model | Q4 Model |
|--------|------------|----------|
| Tokens/second | ~2-5 | ~5-10 |
| Response time | ~30-60s | ~15-30s |
| RAM usage | ~20GB | ~8GB |
| Quality | Best | Good |

---

## 📈 Phase 5: Results & Reporting (Days 17-20)

### 5.1 PDF Report Generation

**Professional PDF Report with fawadhs.dev branding**

| Element | Specification |
|---------|---------------|
| **Branding** | "fawadhs.dev" in cyan blue (#00BCD4), bottom-right corner |
| **Style** | Minimalist, professional, clean typography |
| **Format** | A4, single-column layout |
| **Font** | Helvetica / Arial for English, Noto Nastaliq for Urdu |

### PDF Report Sections

1. **Cover Page** - Title, date, fawadhs.dev branding
2. **Executive Summary** - Key findings in 1 page
3. **Methodology** - Testing approach, tools used
4. **Results Dashboard** - Visual metrics summary
5. **Detailed Results** - Per-category breakdown
6. **Script Comparison** - Urdu vs Roman Urdu analysis
7. **Use Case Recommendations** - How to use Qalb effectively
8. **Limitations & Caveats** - What Qalb struggles with
9. **Appendix** - Raw data tables, test cases

### 5.2 Results Structure

```
results/
├── baseline/
│   ├── urdu_script/
│   │   ├── classification_results.json
│   │   ├── sentiment_results.json
│   │   └── ...
│   └── roman_urdu/
│       ├── classification_results.json
│       ├── sentiment_results.json
│       └── ...
├── urdubench/
│   ├── mgsm_results.json
│   ├── math500_results.json
│   └── ...
├── code_switching/
│   └── mixed_script_results.json
├── analysis/
│   ├── script_comparison.md
│   ├── performance_summary.md
│   └── recommendations.md
└── final_report.md
```

### 5.3 Key Comparisons

| Comparison | Purpose |
|------------|---------|
| Urdu vs Roman Urdu | Script preference analysis |
| Zero-shot vs Few-shot | Prompting effectiveness |
| Easy vs Hard | Difficulty scaling |
| Pure vs Mixed | Code-switching capability |

### 5.4 Report Deliverables

1. **PDF Report** (`reports/qalb_evaluation_report.pdf`) - Professional fawadhs.dev branded
2. **Executive Summary** - 1-page key findings
3. **Raw Data** (`data/final_report.json`) - Complete test data
4. **Visualizations** - Charts and graphs
5. **Recommendations** - Usage guidelines

---

## 📅 Timeline Overview

| Phase | Duration | Focus | Tests |
|-------|----------|-------|-------|
| **Phase 0** | Day 1 | Setup | Environment ready |
| **Phase 1** | Days 2-4 | Baseline | 280 tests (Urdu + Roman) |
| **Phase 2** | Days 5-8 | UrduBench | 100+ standardized tests |
| **Phase 3** | Days 9-13 | Deep Eval | Multi-dimension analysis |
| **Phase 4** | Days 14-16 | Stress Test | Edge cases & variations |
| **Phase 5** | Days 17-20 | Reporting | Final report |

**Total: ~20 days (4 weeks)**

---

## 🛠️ Project Structure

```
Qalb/
├── .venv/                      # Virtual environment
├── docs/
│   ├── ROADMAP.md              ← This file
│   ├── OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── TRAINING.md
│   ├── BENCHMARKS.md
│   ├── USAGE.md
│   ├── RESEARCH.md
│   └── GLOSSARY.md
├── data/                       # 📊 ALL TEST DATA COLLECTED HERE
│   ├── setup_log.json
│   ├── baseline/
│   │   ├── urdu_script/
│   │   └── roman_urdu/
│   ├── urdubench/
│   ├── evaluation/
│   ├── stress/
│   └── final_report.json
├── reports/                    # 📄 GENERATED REPORTS
│   └── qalb_evaluation_report.pdf
├── tests/
│   ├── baseline/
│   │   ├── urdu_script/        # Urdu Nastaliq tests
│   │   └── roman_urdu/         # Roman Urdu tests
│   ├── urdubench/              # UrduBench integration
│   ├── code_switching/         # Mixed script tests
│   ├── stress/                 # Edge cases
│   └── test_runner.py          # Main test runner
├── scripts/
│   ├── data_collector.py       # Collects & logs all test data
│   ├── evaluate.py             # Calculate metrics
│   ├── roman_converter.py      # Urdu ↔ Roman conversion
│   └── generate_pdf_report.py  # PDF report with fawadhs.dev branding
├── examples/
│   ├── ollama_example.py
│   └── transformers_example.py
├── requirements.txt
└── pyproject.toml
```

---

## 🔗 Key Resources

### Qalb Model
| Resource | Link |
|----------|------|
| GitHub | https://github.com/fawad-Laal/Qalb-Urdu |
| Ollama | `ollama run enstazao/qalb:8b-instruct-fp16` |
| HuggingFace | https://huggingface.co/enstazao/Qalb-1.0-8B-Instruct |
| Paper | https://arxiv.org/abs/2601.08141 |

### UrduBench (معیار)
| Resource | Link |
|----------|------|
| Paper | https://arxiv.org/abs/2601.21000 |
| Datasets | MGSM, MATH-500, CommonSenseQA, OpenBookQA (Urdu) |

---

## ✅ Checklist

### Phase 0: Setup ✅ COMPLETE
- [x] Install Ollama
- [x] Pull Qalb model
- [x] Test Urdu script query
- [x] Test Roman Urdu query
- [x] Setup Python environment (.venv)
- [x] Install dependencies (reportlab, ollama, pandas, etc.)
- [x] Create data collection scripts
- [x] Create PDF report generator

### Phase 1: Baseline
- [x] Create 140 Urdu script test cases ✅
- [x] Create 140 Roman Urdu test cases ✅
- [x] Build test runner script ✅
- [ ] Run baseline tests
- [ ] Log all results to `data/baseline/`

### Phase 2: UrduBench
- [ ] Download UrduBench datasets
- [ ] Create Roman Urdu conversions
- [ ] Run UrduBench tests
- [ ] Log all results to `data/urdubench/`

### Phase 3: Deep Evaluation
- [ ] Test prompting strategies
- [ ] Test code-switching
- [ ] Measure Urdu purity
- [ ] Log all results to `data/evaluation/`

### Phase 4: Stress Testing
- [ ] Test Roman Urdu variations
- [ ] Test edge cases
- [ ] Measure CPU performance
- [ ] Log all results to `data/stress/`

### Phase 5: Reporting
- [ ] Generate `data/final_report.json`
- [ ] Run `python scripts/generate_pdf_report.py`
- [ ] Review `reports/qalb_evaluation_report.pdf`
- [ ] Publish findings

---

## 📝 Notes

### Roman Urdu Challenges
- No standardized spelling (kya vs kia vs kiya)
- Regional variations
- Heavy English mixing in casual use
- Ambiguous transliterations

### Expected Findings
- Qalb likely performs better on Urdu script (trained on Nastaliq)
- Roman Urdu may require additional prompting
- Code-switching may degrade performance

---

## 📚 Citations

```bibtex
@article{qalb2025,
  title={Qalb: Largest State-of-the-Art Urdu Large Language Model},
  author={Hassan, Muhammad Taimoor and Ahmed, Jawad and Awais, Muhammad},
  journal={arXiv preprint arXiv:2601.08141},
  year={2026}
}

@article{urdubench2026,
  title={UrduBench: An Urdu Reasoning Benchmark},
  author={Shafique, Muhammad Ali and Mehboob, Areej and Fiaz, Layba and others},
  journal={arXiv preprint arXiv:2601.21000},
  year={2026}
}
```

---

*Last Updated: February 2, 2026*  
*Project Owner: Fawad Hussain (syedfawadhussain@gmail.com)*  
*Repository: https://github.com/fawad-Laal/Qalb-Urdu*
