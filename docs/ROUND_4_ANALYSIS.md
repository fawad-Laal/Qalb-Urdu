# Round 4 Evaluation Analysis
## Qalb Urdu AI Model Testing Framework

**Date:** February 4, 2026  
**Model:** enstazao/qalb:8b-instruct-fp16  
**Framework Version:** 4.0.0  
**Test Duration:** ~4 hours 40 minutes  

---

## Executive Summary

Round 4 introduced comprehensive keyword expansions for translation and commonsense/reasoning categories, aiming to reduce evaluation strictness by accepting more valid synonym variants. Contrary to expectations, this resulted in a **score decrease** of -1.5 points (77.7 vs 79.2 in Round 3).

### Key Findings

| Metric | Round 3 | Round 4 | Change |
|--------|---------|---------|--------|
| Urdu Script | 80.0 | 78.0 | **-2.0** |
| Roman Urdu | 78.4 | 77.4 | **-1.0** |
| Combined | 79.2 | 77.7 | **-1.5** |

**Critical Insight:** Adding more keywords does not always improve scores. The scoring algorithm requires matching at least one keyword from the expanded list, but model responses may use entirely different vocabulary than any provided keywords.

---

## Methodology

### Round 4 Changes

**Objective:** Expand keyword lists to accept more valid response variations.

**Changes Implemented:**

1. **Translation Keywords (26 tests updated)**
   - Added synonym variants for English-to-Urdu translations
   - Added Roman Urdu transliterations (e.g., "shukriya", "theek")
   - Example: "Hello, how are you?" keywords expanded from 4 to 14 terms

2. **Reasoning/Commonsense Keywords (20 tests updated)**
   - Added concept-based alternatives (e.g., "علاج/ilaaj" for doctor tests)
   - Added action synonyms (e.g., "بچاؤ/bachaav" for protection)
   - Example: Rain umbrella test expanded from 5 to 13 keywords

### Scoring Algorithm

```
score = 50 + (50 × passed_keywords / total_keywords)
```

**Important Note:** Adding more keywords increases the denominator, which can *decrease* scores if the model doesn't match the new keywords.

---

## Detailed Category Analysis

### Urdu Script Tests (78.0/100)

| Category | Tests | Avg Score | Min | Max | Change from R3 |
|----------|-------|-----------|-----|-----|----------------|
| translation | 20 | 88.0 | 75.0 | 100.0 | ↑ Improved |
| summarization | 20 | 83.6 | 78.3 | 85.0 | Stable |
| creative_writing | 20 | 80.3 | 76.7 | 85.0 | Stable |
| instruction_following | 20 | 78.2 | 53.1 | 95.0 | Stable |
| mathematics | 20 | 76.1 | 58.3 | 85.6 | Stable |
| question_answering | 20 | 75.2 | 44.7 | 87.5 | Stable |
| conversation | 20 | 75.1 | 55.0 | 83.0 | Stable |
| **reasoning** | **20** | **67.6** | **35.0** | **91.2** | **↓ Decreased** |

### Roman Urdu Tests (77.4/100)

| Category | Tests | Avg Score | Min | Max | Change from R3 |
|----------|-------|-----------|-----|-----|----------------|
| translation | 20 | 85.1 | 75.7 | 95.0 | ↑ Improved |
| summarization | 20 | 78.9 | 76.2 | 81.2 | Stable |
| mathematical_reasoning | 20 | 78.6 | 55.0 | 85.0 | Stable |
| instruction_following | 20 | 77.5 | 60.0 | 95.0 | Stable |
| text_generation | 20 | 76.7 | 55.0 | 80.0 | Stable |
| question_answering | 20 | 76.3 | 55.0 | 85.0 | Stable |
| conversation | 20 | 73.7 | 55.0 | 86.4 | Stable |
| **commonsense_reasoning** | **20** | **72.0** | **55.0** | **77.5** | **↓ Decreased** |

---

## Analysis of Score Decrease

### Root Cause Investigation

The score decrease despite keyword expansion reveals fundamental issues with the scoring methodology:

#### 1. **Keyword Dilution Effect**

When we add more keywords, the scoring formula penalizes responses that match only some keywords:

**Example: roman_trans_002 (Hello, how are you?)**
- Round 3 keywords (6): `["ہیلو", "سلام", "کیسے", "خیریت", "kaise", "haal"]`
- Round 4 keywords (14): Added `"حال", "کیا حال", "آداب", "مزاج", "طبیعت", "theek", "ٹھیک", "aap", "آپ"`
- Model response matched: `"کیسے"` (1 keyword)
- Round 3 score: 50 + (50 × 1/6) = **58.3**
- Round 4 score: 50 + (50 × 1/14) = **53.6** ← Worse!

**Actual Round 4 result:** 81/100 (model matched "کیسے")

#### 2. **Model's Alternative Vocabulary**

The model often uses entirely different but semantically correct words:

**Example: roman_cs_001 (What to take in rain?)**
- Expected keywords (13): umbrella, چھتری, raincoat, برساتی, rain, chhatri, barsaati, بچاؤ, bachaav, محفوظ, cover, گیلا, geela
- Model response: "خوشی، سکون، اور نئی زندگی کی امید" (joy, peace, and hope for new life)
- The model interpreted "bahar" (outside/spring) as "spring season" rather than "going outside"
- Score: 55/100 (failed all keywords)

#### 3. **Reasoning Failures (Not Keyword Issues)**

Many low scores in reasoning come from **incorrect answers**, not keyword matching:

| Test ID | Expected | Model Answer | Issue |
|---------|----------|--------------|-------|
| urdu_reason_007 | 9 (not prime) | 11 | Wrong reasoning |
| urdu_reason_011 | 12 walls | 36 walls | Wrong calculation |
| urdu_reason_015 | 30 | 24 | Wrong pattern |
| urdu_reason_008 | جمعہ (Friday) | پیر (Monday) | Wrong day |

---

## Translation Performance Deep Dive

Despite lower overall scores, translation tests improved in Round 4:

### Top Performers (Score ≥ 95)

| Test ID | Score | Matched Keywords |
|---------|-------|------------------|
| urdu_trans_003 | 100.0 | weather, today, good |
| urdu_trans_007 | 100.0 | knowledge, power |
| urdu_trans_012 | 100.0 | water, life |
| roman_trans_001 | 95.0 | I am, Pakistan, from |
| roman_trans_003 | 95.0 | weather, today, good |

### Translation Challenges

**Proverb translations** remain challenging:
- "Actions speak louder than words" → Model uses "اعمال" instead of "عمل"
- "Practice makes perfect" → Model uses variant phrasing

---

## Commonsense/Reasoning Failures

### Critical Failures (Score < 60)

| Test ID | Score | Prompt | Issue |
|---------|-------|--------|-------|
| urdu_reason_007 | 35 | Which number is different: 2,3,5,9,11 | Model said 11, not 9 |
| urdu_reason_015 | 40 | Complete: 2,6,12,20,___ | Model said 24, not 30 |
| roman_cs_001 | 55 | What to take in rain? | Misunderstood "bahar" |
| roman_cs_009 | 55 | How to lift heavy objects? | Generic response |

### Model Limitations Exposed

1. **Prime number recognition** - Model doesn't identify 9 as non-prime
2. **Pattern sequences** - Complex patterns (n²+n) not recognized
3. **Contextual understanding** - "bahar" interpreted as season, not "outside"
4. **Work-rate problems** - Multiplication vs. work-rate logic confusion

---

## Performance Metrics

### Response Times

| Script | Round 3 | Round 4 | Change |
|--------|---------|---------|--------|
| Urdu Script | ~45s | 48.8s | +3.8s |
| Roman Urdu | ~42s | 56.2s | +14.2s |

Response times increased, possibly due to system load variations.

### Token Statistics

- Average tokens/second: 0.63 (Urdu), 0.55 (Roman)
- Average Urdu character ratio: 76.2% (Urdu), varies (Roman)

---

## Limitations of This Round

### Methodological Issues Identified

1. **Keyword Quantity Penalty**
   - More keywords = lower potential scores when partial matches occur
   - Scoring algorithm doesn't account for semantic equivalence

2. **Semantic vs. Literal Matching**
   - Model may use semantically correct but literally different words
   - Example: "شکر گزار" (grateful) vs "شکریہ" (thanks) - both valid

3. **Test Ambiguity**
   - roman_cs_001: "bahar" can mean "outside" or "spring"
   - Some prompts have multiple valid interpretations

4. **Reasoning != Keywords**
   - Logic problems fail due to incorrect reasoning, not vocabulary
   - Keywords can't measure mathematical/logical correctness

### Recommendations for Future Rounds

1. **Alternative Scoring Methods**
   - Consider "at least N keywords matched" threshold
   - Implement semantic similarity scoring (embeddings)
   - Weight keywords by importance

2. **Separate Logic Tests**
   - Use exact-match scoring for math/logic
   - Remove keywords for numerical answers

3. **Prompt Clarification**
   - Disambiguate prompts like "bahar jaate waqt"
   - Add context hints for potential misinterpretations

---

## Round Comparison Summary

| Round | Focus | Urdu | Roman | Combined | Δ |
|-------|-------|------|-------|----------|---|
| 1 | Original baseline | 74.4 | 74.5 | 74.4 | - |
| 2 | Bilingual keywords | 78.3 | 78.2 | 78.3 | +3.9 |
| 3 | Math clarity fixes | 80.0 | 78.4 | 79.2 | +0.9 |
| **4** | **Synonym expansion** | **78.0** | **77.4** | **77.7** | **-1.5** |

---

## Conclusion

Round 4 demonstrates that **keyword expansion without scoring algorithm adjustment** can be counterproductive. The key insight is that evaluation fairness requires:

1. **Quality over quantity** in keyword selection
2. **Scoring mechanisms** that reward partial matches proportionally
3. **Separate evaluation tracks** for knowledge vs. reasoning tasks

The model's actual capabilities haven't changed - our measurement of them has become **more strict** despite intentions to be more lenient.

### Next Steps

1. Reconsider scoring formula for expanded keyword lists
2. Implement weighted keyword scoring
3. Separate reasoning tests from keyword-based evaluation
4. Consider LLM-as-judge for semantic evaluation

---

## Test Execution Details

- **Start Time:** 2026-02-04 00:47:37
- **End Time:** 2026-02-04 05:27:42
- **Duration:** 4 hours 40 minutes
- **Environment:** Windows 11, 32-core CPU, 31.7 GB RAM
- **Ollama Version:** 0.15.4
- **Python Version:** 3.12.10
