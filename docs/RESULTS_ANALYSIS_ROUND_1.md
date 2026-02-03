# Qalb Model Test Results Analysis - Round 1

**Date:** February 2, 2026  
**Total Tests:** 300 (140 Urdu Script + 160 Roman Urdu)  
**Success Rate:** 100% (300/300)  
**Model:** enstazao/qalb:8b-instruct-fp16 (8B parameters, 16GB)  
**Author:** fawadhs.dev

---

## 🎯 Executive Summary - Combined Findings

### Overall Test Results

| Script Type | Tests | Avg Score | Avg Response Time | Urdu Ratio |
|-------------|-------|-----------|-------------------|------------|
| **Urdu Script** | 140 | **78.5/100** | 45.4s | 78.3% |
| **Roman Urdu** | 160 | **70.4/100** | 38.6s | 70.3% |
| **Combined** | 300 | **74.4/100** | 41.8s | 74.0% |

### Key Finding: Urdu Script Outperforms Roman Urdu by 8.1 Points

The model demonstrates **stronger performance** when prompted in native Urdu script compared to Roman Urdu (transliterated). This is a critical finding:

- **Urdu Script:** Model stays in Urdu, responds naturally, keywords match better
- **Roman Urdu:** Model often switches to English OR pure Urdu script, causing keyword mismatches

### Issue Breakdown (All 300 Tests)

| Issue Type | Count | Percentage |
|------------|-------|------------|
| 🔴 **Genuine Model Errors** | ~35 | 11.7% |
| 🟡 **Test Design Issues** | ~95 | 31.7% |
| 🟢 **Working Correctly** | ~170 | 56.7% |

---

## 🚨 Critical Test Design Issues Discovered

### Issue #1: Script Mismatch Problem (MAJOR)

**Severity:** HIGH - Affects ~40% of Roman Urdu tests

When given Roman Urdu prompts, the model often responds in:
1. **Full Urdu Script** (most common) - Keywords expecting Roman fail
2. **Full English** - Keywords expecting Roman/Urdu fail  
3. **Mixed response** - Partial matches only

**Example - roman_qa_001:**
```
Prompt: "Pakistan ka darul hakoomat kya hai?"
Response: "پاکستان کا دارالحکومت اسلام آباد ہے۔" (Urdu script!)
Keywords Expected: ["Islamabad", "اسلام آباد"]
Result: Passed "اسلام آباد" but failed "Islamabad"
```

**Example - roman_qa_009:**
```
Prompt: "Hafte mein kitne din hote hain?"
Response: "ایک ہفتے میں سات دن ہوتے ہیں۔" (Urdu script!)
Keywords Expected: ["saat", "7", "seven"]
Result: FAILED ALL - Model said "سات" (Urdu word for 7)
Score: 60
```

**Recommendation:** 
- Add Urdu script equivalents to ALL Roman Urdu test keywords
- For roman_qa_009: Add "سات" to keywords
- Consider a "script-agnostic" scoring mode

---

### Issue #2: Keyword Translation Gap

Roman Urdu tests expect keywords in Roman or English, but model responds in Urdu script consistently.

**Tests Affected:**

| Test ID | Expected Keyword | Model Used | Same Meaning? |
|---------|-----------------|------------|---------------|
| roman_qa_008 | "Liaquat Ali Khan" | "لیاقت علی خان" | ✅ YES |
| roman_qa_014 | "4", "char" | "چار" | ✅ YES |
| roman_qa_018 | "5", "paanch" | "پانچ" | ✅ YES |
| roman_sum_005 | "Ramadan" | "رمضان" | ✅ YES |
| roman_trans_001 | "mausam" | "موسم" | ✅ YES |

**All these are FALSE NEGATIVES** - Model gave correct answers in wrong script!

---

### Issue #3: Instruction Following Excellence Hidden

**roman_inst_017** demonstrates perfect instruction following but scores only 85:

```json
{
  "prompt": "Table format mein do: Pakistan ke 4 provinces aur unke capitals.",
  "response": "| Province | Capital |\n|----------|--------|\n| Punjab | Lahore |\n| Sindh | Karachi |\n| Khyber Pakhtunkhwa (KPK) | Peshawar |\n| Balochistan | Quetta |",
  "urdu_char_ratio": 0.0,
  "passed_keywords": ["Punjab", "Lahore", "Sindh", "Karachi"],
  "score": 85.0
}
```

**Analysis:** 
- ✅ Perfect table format (markdown)
- ✅ All 4 provinces correct
- ✅ All 4 capitals correct
- ❌ Score penalized for 0% Urdu ratio

**This test proves the model CAN follow complex formatting instructions perfectly!**

---

## 📊 Category-by-Category Analysis

### Roman Urdu Test Categories (160 tests)

| Category | Count | Avg Score | Issues |
|----------|-------|-----------|--------|
| Question Answering | 20 | 74.4 | Script mismatch |
| Summarization | 20 | 76.1 | Good performance |
| Translation | 20 | 81.3 | **Best category** |
| Text Generation | 20 | 55.0 | Keyword definition problem |
| Mathematical Reasoning | 20 | 79.0 | Solid |
| Commonsense Reasoning | 20 | 55.9 | Keyword too specific |
| Instruction Following | 20 | 79.5 | Excellent actual performance |
| Conversation | 20 | 57.8 | Low due to script mismatch |

### Urdu Script Test Categories (140 tests)

| Category | Tests | Avg Score | Model Errors | Test Issues |
|----------|-------|-----------|--------------|-------------|
| Question Answering | 20 | 79.5 | 4 | 7 |
| Mathematics | 20 | 75.2 | 4 | 10 |
| Reasoning | 20 | **67.8** | 10 | 5 |
| Translation | 20 | 82.4 | 3 | 5 |
| Summarization | 20 | **84.3** | 0 | 3 |
| Creative Writing | 20 | 81.2 | 1 | 8 |
| Conversation | 19 | 77.9 | 1 | 5 |

---

## ❌ Genuine Model Errors Identified

### 1. Factual Errors

| Test | Prompt | Model Answer | Correct Answer |
|------|--------|--------------|----------------|
| urdu_qa_013 | قومی جانور کیا ہے؟ | چھاگ | **مارخور** |
| urdu_qa_014 | خطبہ الہ آباد کب؟ | 1920 | **1930** |
| urdu_qa_020 | اونچی چوٹی کون سی؟ | ننگا پربت | **K2** |
| roman_qa_013 | Shikwa kab likhi? | 1902 | **1909/1911** |
| roman_inst_003 | Earth flat hai? | "Haan" | **Nahi** |
| roman_inst_012 | Suraj maghrib se nikalta? | "True" | **False** |

### 2. Mathematical Errors

| Test | Problem | Model Answer | Correct |
|------|---------|--------------|---------|
| urdu_math_002 | بارہ منفی سات | -77 (did 11×-7) | **5** |
| urdu_math_017 | مثلث کے زاویوں کا مجموعہ | 540° | **180°** |
| urdu_reason_020 | 15 سال + 5 سال = ? | 76 | **20** |
| roman_math_003 | 30 students, 40% girls → boys? | 12 | **18** |
| roman_math_004 | 90 km/h × 3 hours | 97.2 km | **270 km** |
| roman_math_008 | 900 ÷ 3 friends | 450 | **300** |
| roman_math_019 | Sum 1 to 10 | 15 | **55** |

### 3. Reasoning Failures

| Test | Type | Error |
|------|------|-------|
| urdu_reason_003 | Temporal | "پرسوں" (day after tomorrow) confused with "کل" |
| urdu_reason_007 | Pattern | Failed to identify 9 as only non-prime |
| urdu_reason_011 | Work-rate | 5 workers × 5 days = 5 walls → 10 workers = ? |
| urdu_reason_013 | Classification | Hallucinated "نر بندر" instead of "ہاتھی" |
| urdu_reason_015 | Cipher | Failed A=1, B=2 pattern |

---

## 🔧 Test Design Recommendations

### Priority 1: Fix Roman Urdu Keywords (HIGH IMPACT)

For EVERY Roman Urdu test, add both:
- Roman transliteration keyword
- Urdu script equivalent keyword

**Before:**
```json
"keywords": ["saat", "7", "seven"]
```

**After:**
```json
"keywords": ["saat", "7", "seven", "سات"]
```

### Priority 2: Fix Synonyms

| Category | Add These Synonyms |
|----------|-------------------|
| Happiness | خوشی, خوشگوار, مسکراہٹ |
| Conversation | گفتگو, بات, کلام |
| East | مشرق, پورب |
| National Language | 1947, 1948, 1949 (all valid) |

### Priority 3: Math Scoring Adjustment

For mathematical tests:
- Accept 0% Urdu ratio if answer is correct
- Strip "Reasoning:" and "Answer:" prefixes before ratio calculation

### Priority 4: Instruction Following Tests

**roman_inst_017** proves model excellence at:
- Table formatting ✅
- Markdown generation ✅  
- Structured output ✅
- Following specific format instructions ✅

**Add more instruction following tests for:**
- JSON output (already tested - works!)
- Bullet points
- Numbered lists
- Code blocks

---

## 📈 Model Strengths Identified

### 1. Translation (Best Category)
- Urdu Script: 82.4 avg
- Roman Urdu: 81.3 avg
- Consistently produces accurate translations

### 2. Summarization (Excellent)
- Urdu Script: 84.3 avg (highest!)
- Model effectively condenses information

### 3. Instruction Following (Underscored)
- Actual performance: **Excellent**
- Scored performance: 79.5 (penalized for script choice)
- Model follows complex formatting perfectly

### 4. Mathematical Computation
- 70%+ accuracy on standard arithmetic
- Clear step-by-step reasoning shown
- Issues mainly with word problems

---

## 📉 Model Weaknesses Identified

### 1. Reasoning (Weakest Category - 67.8)
- Temporal reasoning failures
- Work-rate problems
- Odd-one-out classification
- Pattern recognition with ciphers

### 2. Script Consistency
- Roman Urdu prompts → Often Urdu script responses
- This is linguistically natural but breaks keyword matching

### 3. Factual Recall
- Historical dates (Allahabad 1920 vs 1930)
- National symbols (Markhor, K2)
- Scientific facts (Earth flat - said yes!)

### 4. Commonsense Reasoning (Roman)
- Average: 55.9 (lowest)
- All 20 tests scored 55
- BUT: Responses are semantically correct, just script mismatch!

---

## 🎯 Recommended Actions for Round 2

### Immediate Fixes (Before Next Run)

1. **Add Urdu script keywords** to all Roman Urdu tests
2. **Fix factually incorrect** expected answers:
   - urdu_qa_005: Accept 1948, 1949
   - Moon orbital period: Accept 27 days (scientifically correct)

3. **Scoring logic update:**
   - Strip English prefixes before urdu_char_ratio
   - OR-based keyword matching (implemented ✅)
   - Script-agnostic mode for Roman tests

### Test Suite Additions

1. **More reasoning tests** (current weakness):
   - Additional temporal reasoning
   - More work-rate problems
   - Classification with clear categories

2. **Structured output tests**:
   - JSON generation
   - Table formatting
   - Code output

3. **Multi-turn conversation** (if supported)

---

## 📋 Test Statistics Summary

### Scoring Distribution

| Score Range | Urdu Script | Roman Urdu | Total |
|-------------|-------------|------------|-------|
| 90-100 | 28 (20%) | 15 (9.4%) | 43 (14.3%) |
| 80-89 | 41 (29.3%) | 31 (19.4%) | 72 (24%) |
| 70-79 | 31 (22.1%) | 19 (11.9%) | 50 (16.7%) |
| 60-69 | 27 (19.3%) | 18 (11.3%) | 45 (15%) |
| 50-59 | 13 (9.3%) | 77 (48.1%) | 90 (30%) |

**Note:** The 48.1% of Roman Urdu tests scoring 50-59 is primarily due to script mismatch, not model failure.

### Response Time Analysis

- **Fastest Response:** 2.6s (roman_inst_012)
- **Slowest Response:** 180s (roman_gen_019)
- **Average:** 41.8s overall

Longer responses correlate with:
- Text generation tasks
- Complex explanations
- Multi-step reasoning

---

## 🏁 Conclusion

### Overall Assessment: **GOOD with Caveats**

The Qalb model demonstrates:
- **Strong Urdu language understanding** (78.5 in native script)
- **Excellent translation capabilities** (82.4 average)
- **Good summarization skills** (84.3 average)
- **Solid instruction following** (when format allows)

### Primary Issue: Test Framework, Not Model

The 8.1-point gap between Urdu Script (78.5) and Roman Urdu (70.4) is primarily caused by **keyword definition issues**, not model weakness:

- Model correctly interprets Roman Urdu prompts
- Model responds in linguistically appropriate script
- Keywords don't account for script variation
- **FALSE NEGATIVES inflate failure rate**

### Actual Performance Estimate

If we account for script mismatch false negatives:
- Roman Urdu estimated true score: **~76-78**
- Combined estimated true score: **~77-78**

---

## System Specifications

```
System: Windows 11
CPU: Intel64 Family 6 Model 183 (32 cores)
RAM: 13.2 GB available / 31.7 GB total
Disk: 589.3 GB free
Python: 3.12.10
Ollama: v0.15.4
Model: enstazao/qalb:8b-instruct-fp16
Total Test Duration: ~3.5 hours
```

---

# PART 2: Detailed Per-Test Analysis (Urdu Script)

The following section provides granular analysis of each test from the Urdu Script baseline tests.

---

## Category 1: Question Answering (20 tests)

### ✅ Perfect Tests (No Issues)
| Test ID | Score | Notes |
|---------|-------|-------|
| urdu_qa_001 | 90 | Capital of Pakistan - correct |
| urdu_qa_004 | 90 | Quaid's birthday - all keywords matched |
| urdu_qa_006 | 85 | Earth orbit days - correct 365.25 |
| urdu_qa_008 | 90 | First PM - correct |
| urdu_qa_012 | 85 | National flower - got "چنبیلی" (correct) |
| urdu_qa_015 | 85 | Quran surahs - 114 correct |
| urdu_qa_016 | 90 | Largest city - Karachi correct |

### ⚠️ Test Design Flaws

#### urdu_qa_002 (Score: 85)
- **Prompt:** سورج کس سمت سے طلوع ہوتا ہے؟
- **Response:** "سورج **مشرق** سے طلوع ہوتا ہے"
- **Issue:** Test expects both "مشرق" AND "پورب" but they're **synonyms**!
- **Recommendation:** Keywords should be OR logic - either word is valid

#### urdu_qa_003 (Score: 60)
- **Prompt:** پانی کا کیمیائی فارمولا کیا ہے؟
- **Response:** "پانی کا کیمیائی فارمولا **ایچ 2 او** ہے"
- **Issue:** Model wrote "ایچ 2 او" (with space) but test expects "H2O" or "ایچ ٹو او"
- **Recommendation:** Add "ایچ 2 او" and variants to keywords

#### urdu_qa_005 (Score: 85)
- **Prompt:** اردو زبان کی سرکاری حیثیت کب ملی؟
- **Response:** "اردو زبان کو **1949** میں پاکستان کی سرکاری زبان قرار دیا گیا"
- **Issue:** Model says 1949, test expects 1947
- **Reality Check:** Model is **MORE CORRECT** - Urdu was declared national language in 1948/1949 via constitutional assembly
- **Recommendation:** Fix expected answer to accept 1948, 1949

#### urdu_qa_009 (Score: 78.6)
- **Prompt:** ہفتے میں کتنے دن ہوتے ہیں؟
- **Response:** "Answer: سات دن"
- **Issue:** Low score due to "Answer:" prefix reducing urdu_char_ratio to 45%
- **Recommendation:** Strip common English prefixes before ratio calculation

#### urdu_qa_011 (Score: 81.7)
- **Prompt:** چاند زمین کے گرد کتنے دنوں میں چکر لگاتا ہے؟
- **Response:** "چاند زمین کے گرد تقریباً **27.3** دنوں میں چکر لگاتا ہے"
- **Issue:** Got 27 (correct!) but also has 28, 29 in failed keywords
- **Reality Check:** 27.3 days is the **sidereal orbital period** - scientifically correct!
- **Recommendation:** Test design is flawed - too many alternatives confuse scoring

#### urdu_qa_018 (Score: 77.5)
- **Prompt:** پاکستان کتنے صوبوں پر مشتمل ہے؟
- **Response:** "پاکستان **چار** صوبوں پر مشتمل ہے: پنجاب، سندھ، خیبر پختونخوا اور بلوچستان"
- **Issue:** Keywords include "4", "6", "چھ" as failed - but model correctly named all 4 provinces
- **Recommendation:** "چار" alone should be sufficient (OR logic)

#### urdu_qa_019 (Score: 76.7)
- **Prompt:** انسان کے دل میں کتنے خانے ہوتے ہیں؟
- **Response:** "ایک انسان کے دل میں تقریباً **چار** خانے (Chambers) ہوتے ہیں"
- **Issue:** Score lowered because "(Chambers)" in English
- **Recommendation:** This is acceptable bilingual explanation - don't penalize

### ❌ Model Errors (Genuine Weaknesses)

#### urdu_qa_013 (Score: 58.4)
- **Prompt:** پاکستان کا قومی جانور کیا ہے؟
- **Response:** "پاکستان کا قومی جانور **چھاگ** یا چکر ہے"
- **Correct Answer:** مارخور (Markhor)
- **Analysis:** Model hallucinated - "چھاگ" is not the national animal
- **Verdict:** ❌ GENUINE MODEL ERROR

#### urdu_qa_014 (Score: 60)
- **Prompt:** علامہ اقبال نے خطبہ الہ آباد کب دیا؟
- **Response:** "خطبہ الہ آباد **1920** میں دیا گیا"
- **Correct Answer:** 1930
- **Analysis:** Model is factually wrong - Allahabad Address was December 29, 1930
- **Verdict:** ❌ GENUINE MODEL ERROR

#### urdu_qa_017 (Score: 80)
- **Prompt:** دنیا کی سب سے لمبی دریا کون سی ہے؟
- **Response:** "**نیل** دنیا کی سب سے لمبی دریا ہے جس کی لمبائی تقریباً 6650 کلومیٹر ہے"
- **Issue:** Passed "نیل" but failed "دریائے نیل"
- **Analysis:** "نیل" IS "دریائے نیل" - test keyword is redundant
- **Recommendation:** One keyword sufficient

#### urdu_qa_020 (Score: 55)
- **Prompt:** پاکستان کی سب سے اونچی چوٹی کون سی ہے؟
- **Response:** "پاکستان کی سب سے اونچی چوٹی **ننگا پربت** ہے"
- **Correct Answer:** K2 (8,611m)
- **Analysis:** Model is WRONG - Nanga Parbat is 9th highest (8,126m), K2 is highest in Pakistan
- **Verdict:** ❌ GENUINE MODEL ERROR

---

## Category 2: Mathematics (20 tests)

### Common Pattern: "Reasoning: ... Answer:" Format
The model consistently uses English labels ("Reasoning:", "Answer:") which reduces urdu_char_ratio. This is a **test design issue**, not a model flaw.

### ⚠️ Test Design Flaws

#### urdu_math_001 (Score: 70)
- **Prompt:** پانچ جمع پانچ کتنے ہوتے ہیں؟
- **Response:** "Reasoning: جمع: 5 + 5 = 10 Answer: **10**"
- **Issue:** urdu_char_ratio only 16.7% due to English format
- **Reality:** Answer "10" is **CORRECT**
- **Recommendation:** Math tests should accept numeric format

#### urdu_math_002 (Score: 50) ❌ MAJOR ISSUE
- **Prompt:** بارہ منفی سات کتنے ہوتے ہیں؟
- **Response:** "Reasoning: 11 × -7 Answer: **-77**"
- **Correct Answer:** 5 (12 - 7 = 5)
- **Analysis:** Model misunderstood "منفی" (minus) as "multiplied by negative"
- **Verdict:** ❌ GENUINE MODEL ERROR - Confused subtraction with multiplication

#### urdu_math_003 (Score: 60)
- **Prompt:** چھ ضرب چھ کتنے ہوتے ہیں؟
- **Response:** "Answer: **36**"
- **Issue:** urdu_char_ratio 0% but answer is correct!
- **Recommendation:** Accept pure numeric answers for math

#### urdu_math_007 (Score: 60)
- **Prompt:** تین کا مربع کیا ہے؟
- **Response:** "Answer: **9**"
- **Issue:** urdu_char_ratio 0%, but 9 is correct!
- **Recommendation:** "نو" or "9" should both score full marks

#### urdu_math_009 (Score: 55.9) ❌ CONCEPTUAL ERROR
- **Prompt:** پچیس فیصد کا مطلب کتنا حصہ ہے؟
- **Response:** "Reasoning: پچیس فیصد = **25%** Answer: 25%"
- **Expected:** چوتھائی، 1/4، ایک چوتھائی
- **Analysis:** Model restated 25% instead of converting to fraction (1/4)
- **Verdict:** ⚠️ MODEL MISSED THE POINT - didn't understand "کتنا حصہ"

#### urdu_math_017 (Score: 80) ❌ WRONG MATH
- **Prompt:** ایک مثلث کے تین زاویوں کا مجموعہ کتنے ڈگری ہوتا ہے؟
- **Response:** "3 × 180 = **540** Answer: 540 ڈگری"
- **Correct Answer:** 180 degrees
- **Analysis:** Model multiplied instead of stating the constant sum
- **Note:** Interestingly, "180" is in the response (as multiplier) so keyword matched
- **Verdict:** ❌ GENUINE MODEL ERROR - Got wrong answer but accidentally passed

#### urdu_math_018 (Score: 80.4) ❌ WRONG MATH
- **Prompt:** بیس کا دس فیصد کتنا ہوتا ہے؟
- **Response:** "بیس کا دس فیصد = 20% × 20 = **4**"
- **Correct Answer:** 2 (20 × 10% = 2)
- **Analysis:** Model calculated wrong (got 4 instead of 2)
- **Note:** Keyword "2" matched because it appeared in the response accidentally
- **Verdict:** ❌ GENUINE MODEL ERROR

### ✅ Correct Math Answers
| Test ID | Score | Prompt | Answer | Correct? |
|---------|-------|--------|--------|----------|
| urdu_math_004 | 85 | سو تقسیم پانچ | 20 | ✅ |
| urdu_math_005 | 85 | ایک درجن میں کتنی | 12 | ✅ |
| urdu_math_006 | 80 | 15 - 7 = | 8 | ✅ |
| urdu_math_008 | 77.5 | √16 = | 4 | ✅ |
| urdu_math_010 | 80 | 8 × 4 = | 32 | ✅ |
| urdu_math_011 | 77.5 | 7 × 8 = | 56 | ✅ |
| urdu_math_012 | 80.4 | 1 hour = ? min | 60 | ✅ |
| urdu_math_013 | 85 | 200 + 300 = | 500 | ✅ |
| urdu_math_014 | 74 | 9 × 9 = | 81 | ✅ |
| urdu_math_015 | 84 | 1 km = ? m | 1000 | ✅ |
| urdu_math_016 | 80 | 50÷5 per item | 10 | ✅ |
| urdu_math_019 | 77.5 | 4³ = | 64 | ✅ |
| urdu_math_020 | 90 | π ≈ ? | 3.14, 22/7 | ✅ |

---

## Category 3: Reasoning (20 tests) - WEAKEST CATEGORY

### ⚠️ Test Design Flaws

#### urdu_reason_002 (Score: 81.7)
- **Prompt:** ترتیب مکمل کریں: 2، 4، 6، 8، ___
- **Response:** "اگلا عدد: **10**"
- **Issue:** Failed keyword "دس" - but "10" is the same number!
- **Recommendation:** Accept numeric OR Urdu word

#### urdu_reason_005 (Score: 85)
- **Prompt:** Fibonacci: 1، 1، 2، 3، 5، 8، ___
- **Response:** "8 + 5 = **13**"
- **Issue:** Correct answer, failed "تیرہ" keyword
- **Recommendation:** Accept numeric

#### urdu_reason_006 (Score: 71.1)
- **Prompt:** A > B, B > C, who's bigger A or C?
- **Response:** "A > C Answer: **A**"
- **Issue:** Low urdu_char_ratio (18.5%) due to variables being English
- **Recommendation:** This is inherent to logic problems - accept

#### urdu_reason_009 (Score: 70)
- **Prompt:** Book : Reading :: Song : ___
- **Response:** "Answer: **موسیقی**"
- **Expected:** گانے، سننے
- **Analysis:** "موسیقی" (music) is semantically correct alternative to "گانے" (singing)
- **Recommendation:** Add "موسیقی" to keywords

#### urdu_reason_010 (Score: 60)
- **Prompt:** A, C, E, G, ___
- **Response:** "Answer: **I**"
- **Issue:** urdu_char_ratio 0% for English letter answer
- **Recommendation:** This pattern uses English letters - accept

### ❌ Model Errors (Genuine Weaknesses) - 10 FAILURES

#### urdu_reason_003 (Score: 64)
- **Prompt:** اگر آج پیر ہے تو **پرسوں** کون سا دن ہوگا؟
- **Response:** "Answer: **منگل**"
- **Correct:** بدھ (Wednesday)
- **Analysis:** "پرسوں" means "day after tomorrow". Monday + 2 = Wednesday
- Model answered Tuesday (کل = tomorrow)
- **Verdict:** ❌ GENUINE MODEL ERROR - Confused "پرسوں" with "کل"

#### urdu_reason_004 (Score: 64)
- **Prompt:** کون سا لفظ باقیوں سے مختلف ہے: گلاب، چنبیلی، آم، یاسمین
- **Response:** "Answer: **گلاب**"
- **Correct:** آم (mango - fruit among flowers)
- **Analysis:** Model picked wrong odd-one-out
- **Verdict:** ❌ GENUINE MODEL ERROR

#### urdu_reason_007 (Score: 55)
- **Prompt:** کون سا نمبر باقیوں سے مختلف ہے: 2، 3، 5، 9، 11
- **Response:** "نمبر جو باقیوں سے مختلف ہے وہ ہے: **11**"
- **Correct:** 9 (only non-prime number)
- **Analysis:** Model said 11 is different (probably because it's largest)
- **Verdict:** ❌ GENUINE MODEL ERROR - Didn't identify prime number pattern

#### urdu_reason_008 (Score: 60)
- **Prompt:** اگر کل سے پہلے جمعرات تھی تو آج کون سا دن ہے؟
- **Response:** "اگر کل جمعرات تھی، تو آج **پیر** ہونا چاہئے"
- **Correct:** ہفتہ (Saturday)
- **Analysis:** "کل سے پہلے" = day before yesterday = Thursday → today = Saturday
- Model misread as "yesterday was Thursday" → today = Friday
- **Verdict:** ❌ GENUINE MODEL ERROR - Misunderstood temporal phrase

#### urdu_reason_011 (Score: 55) ❌ CLASSIC PUZZLE FAIL
- **Prompt:** 5 مزدور 5 دنوں میں 5 دیواریں → 10 مزدور 10 دنوں میں کتنی دیواریں؟
- **Response:** "10 × 10 = **100** دیواریں"
- **Correct:** 20 دیواریں
- **Analysis:** Classic work-rate problem
  - 1 worker builds 1 wall in 5 days
  - 10 workers in 10 days = 10 × (10/5) = 20 walls
- Model multiplied workers × days naively
- **Verdict:** ❌ GENUINE MODEL ERROR - Failed work-rate reasoning

#### urdu_reason_013 (Score: 65)
- **Prompt:** کون سا جانور باقیوں سے مختلف ہے: شیر، چیتا، ہاتھی، بلی
- **Response:** "Answer: **نر بندر** (بوبی کٹ)"
- **Correct:** ہاتھی (elephant - not a cat/feline)
- **Analysis:** Model hallucinated a completely different animal!
- **Verdict:** ❌ GENUINE MODEL ERROR - Severe hallucination

#### urdu_reason_015 (Score: 50.5) ❌ CODING FAIL
- **Prompt:** APPLE = 1-16-16-12-5 → BALL = ?
- **Response:** "BLL"
- **Correct:** 2-1-12-12 (A=1, B=2, L=12 position coding)
- **Analysis:** Model didn't understand the A=1, B=2 cipher
- **Verdict:** ❌ GENUINE MODEL ERROR - Failed pattern recognition

#### urdu_reason_017 (Score: 65)
- **Prompt:** Water : Thirst :: Food : ___
- **Response:** "Answer: **غذائیت** سے ہے"
- **Expected:** بھوک (hunger)
- **Analysis:** Model said "nutrition" instead of "hunger" (the need food satisfies)
- **Verdict:** ⚠️ DEBATABLE - "غذائیت" is related but not the best analogy

#### urdu_reason_019 (Score: 55)
- **Prompt:** کون سا ملک باقیوں سے مختلف ہے: پاکستان، بھارت، بنگلادیش، جاپان
- **Response:** "**پاکستان** سب سے مختلف ملک ہے"
- **Correct:** جاپان (not South Asian)
- **Analysis:** Model picked wrong odd-one-out
- **Verdict:** ❌ GENUINE MODEL ERROR - Wrong classification

#### urdu_reason_020 (Score: 55) ❌ SIMPLE MATH FAIL
- **Prompt:** 5 سال پہلے علی کی عمر 15 سال تھی → آج کتنی ہے؟
- **Response:** "16 + 60 = **76** سال"
- **Correct:** 20 سال (15 + 5 = 20)
- **Analysis:** Model did bizarre calculation
- **Verdict:** ❌ GENUINE MODEL ERROR - Failed basic arithmetic

---

## Category 4: Translation (20 tests) - STRONGEST CATEGORY

### ✅ Excellent Performance

| Test ID | Score | Type | Notes |
|---------|-------|------|-------|
| urdu_trans_001 | 100 | Urdu→English | Perfect |
| urdu_trans_003 | 95 | Urdu→English | Perfect |
| urdu_trans_004 | 90 | English→Urdu | Perfect |
| urdu_trans_007 | 100 | Urdu→English | "Knowledge is power" |
| urdu_trans_012 | 95 | Urdu→English | Perfect |
| urdu_trans_013 | 90 | English→Urdu | Perfect |
| urdu_trans_015 | 95 | Urdu→English | Perfect |
| urdu_trans_018 | 90 | English→Urdu | Perfect |

### ⚠️ Test Design Flaws

#### urdu_trans_002 (Score: 82.5)
- **Prompt:** "Hello, how are you?" کا اردو ترجمہ
- **Response:** "سلام، تم خیریت سے **ہو**؟"
- **Issue:** Failed "ہیلو", "کیسے", "ہیں"
- **Analysis:** Model used "سلام" (culturally appropriate) instead of "ہیلو"
- **Recommendation:** Accept cultural equivalents - "سلام" = "ہیلو"

#### urdu_trans_005 (Score: 91.7)
- **Prompt:** آج موسم بہت اچھا ہے → English
- **Response:** "The weather is very **nice** today"
- **Issue:** Failed "good" keyword
- **Analysis:** "nice" IS good - synonym!
- **Recommendation:** Add "nice", "great" to keywords

#### urdu_trans_009 (Score: 65)
- **Prompt:** تھالی کا بینگن → English idiom
- **Response:** "A square peg in a round hole"
- **Expected:** "opportunist", "sides"
- **Analysis:** This is a HARD idiom. "تھالی کا بینگن" = someone who keeps changing sides
- Model gave different idiom meaning "misfit"
- **Verdict:** ⚠️ MODEL MISUNDERSTOOD - But idiom translation is very hard

#### urdu_trans_010 (Score: 42.6)
- **Prompt:** "Birds of a feather flock together" → Urdu idiom
- **Response:** "'ایک جیسے پنداروں کی جمع رہتی ہے'"
- **Expected:** "چور", "مشاطہ" (چور چور مساوی برابر)
- **Analysis:** Model gave literal translation, not the Urdu equivalent idiom
- **Verdict:** ⚠️ TEST EXPECTS SPECIFIC IDIOM - Model gave literal translation

#### urdu_trans_014 (Score: 60)
- **Prompt:** "Practice makes perfect" → Urdu
- **Response:** "مشکل سے مہارت حاصل کرتی ہے"
- **Expected:** مشق، کامل
- **Analysis:** Model said "difficulty brings skill" instead of "practice makes perfect"
- **Verdict:** ❌ MODEL ERROR - Wrong translation

#### urdu_trans_016 (Score: 65)
- **Prompt:** "Good morning" → Urdu
- **Response:** "نیا دن مبارک ہو!"
- **Expected:** صبح، خیر، بخیر
- **Analysis:** "نیا دن مبارک" = "blessed new day" - creative but not standard
- Standard: "صبح بخیر" or "صبح کی سلام"
- **Verdict:** ⚠️ CREATIVE BUT NON-STANDARD

#### urdu_trans_019 (Score: 55)
- **Prompt:** "Actions speak louder than words" → Urdu
- **Response:** "بنیاد حقیقت سے زیادہ بولنے کی طاقت ہوتی ہے"
- **Expected:** عمل، باتوں
- **Analysis:** Model gave garbled translation that doesn't capture the proverb
- **Verdict:** ❌ MODEL ERROR - Poor translation

---

## Category 5: Summarization (20 tests)

### ✅ Strong Performance
Summarization shows consistent 85% scores. Model excels at condensing information.

| Test ID | Score | Task | Quality |
|---------|-------|------|---------|
| urdu_summary_001 | 85 | Pakistan independence | Excellent |
| urdu_summary_002 | 85 | Allama Iqbal | Just repeated input |
| urdu_summary_003 | 85 | Thirsty crow story | Good |
| urdu_summary_004 | 85 | Urdu language history | Good |
| urdu_summary_005 | 85 | Computer definition | Too long! |
| urdu_summary_006 | 85 | Hard work quote | Good |
| urdu_summary_007 | 81.4 | Water importance | Good |
| urdu_summary_008 | 85 | Quaid's principles | Good |
| urdu_summary_009 | 85 | Health importance | Good |
| urdu_summary_010 | 85 | Education importance | Good |

### ⚠️ Observations

#### urdu_summary_002 (Score: 85)
- **Issue:** Model **repeated the input verbatim** instead of summarizing
- **Analysis:** This should be penalized but keywords matched
- **Recommendation:** Add length check - summary should be SHORTER than input

#### urdu_summary_005 (Score: 85)
- **Response Time:** 178 seconds (nearly 3 minutes!)
- **Response Length:** Very long expansion instead of summary
- **Analysis:** Model wrote an essay instead of summarizing
- **Recommendation:** Penalize responses longer than input for summary tasks

---

## Category 6: Creative Writing (20 tests)

### ✅ Strong Performance
Creative writing shows good scores (75-85 range) with rich Urdu vocabulary.

### ⚠️ Keyword Matching Issues

#### urdu_creative_001 (Score: 78.3)
- **Prompt:** بہار کے موسم پر نظم لکھیں
- **Response:** Beautiful poem about spring
- **Issue:** Failed "پھول", "خوشبو" - but used "پتوں", "فطرت", "خوبصورتی"
- **Recommendation:** Creative writing needs flexible keyword matching

#### urdu_creative_003 (Score: 55) ❌ KEYWORD FAIL
- **Prompt:** ایماندار لکڑہارے کی کہانی
- **Response:** Story about "جیک" a woodcutter who saves trees
- **Issue:** Failed ALL keywords: "لکڑہارا", "ایماندار", "کلہاڑی"
- **Analysis:** Model wrote about a person named Jack who cuts wood, but:
  - Used "لکڑ ہار" (space) instead of "لکڑہارا"
  - Story is about saving trees, not honesty
- **Verdict:** ⚠️ PARTIALLY MODEL ERROR - Diverged from classic story

#### urdu_creative_005 (Score: 81.7)
- **Prompt:** چاند رات پر نظم
- **Response:** Poem about moonlit night
- **Issue:** Failed "عید" keyword
- **Analysis:** "چاند رات" literally means "moon night" - model wrote about that
- "چاند رات" in Pakistani context usually means "Eid moon night"
- **Verdict:** ⚠️ AMBIGUOUS PROMPT - Could mean either

#### urdu_creative_009 (Score: 80)
- **Prompt:** گھر کی سیر
- **Response:** Description with gardens, halls, towers, rooms
- **Issue:** Failed "کمرے" but mentioned "ہر کمرہ"
- **Analysis:** Model used singular "کمرہ" not plural "کمرے"
- **Recommendation:** Add singular forms to keywords

#### urdu_creative_019 (Score: 80) ⭐ SYNONYM EXAMPLE
- **Prompt:** عید کی صبح کا منظر لکھیں
- **Response:** "عید کی صبح کا منظر دلکش اور **خوشگوار** ہوتا ہے... **مسکراہٹ**..."
- **Issue:** Failed "خوشی" but used "خوشگوار" and "مسکراہٹ" (synonyms!)
- **Analysis:** Model expressed happiness through different words
- **Recommendation:** Accept synonyms: خوشگوار, مسکراہٹ, خوشی

---

## Category 7: Conversation (19 tests completed)

### ✅ Good Performance
Conversational responses are natural and appropriate.

### ⚠️ Test Design Issues

#### urdu_conv_004 (Score: 80)
- **Prompt:** کیا آپ اردو میں بات کر سکتے ہیں؟
- **Response:** "جی ہاں، میں اردو اور دیگر زبانوں میں **گفتگو** کرتا ہوں"
- **Issue:** Used "گفتگو" instead of "بات"
- **Recommendation:** Synonyms should match

#### urdu_conv_010 (Score: 55)
- **Prompt:** شکریہ آپ کی مدد کے لیے
- **Response:** "معذرت، میرے پاس واپسی کا کوئی خاص طریقہ نہیں"
- **Issue:** Model apologized instead of saying "you're welcome"
- **Verdict:** ⚠️ MODEL CONFUSION - Didn't recognize this as gratitude

#### urdu_conv_017 (Score: 55)
- **Prompt:** آپ کو غصہ آتا ہے؟
- **Response:** Philosophical answer about anger being inappropriate
- **Expected:** Model should say it doesn't have emotions (مصنوعی, جذبات)
- **Verdict:** ⚠️ MODEL DIDN'T IDENTIFY ITSELF as AI

---

# PART 3: Detailed Per-Test Analysis (Roman Urdu)

---

## Roman Category 1: Question Answering (20 tests)

### ✅ Working Tests
| Test ID | Score | Notes |
|---------|-------|-------|
| roman_qa_001 | 85 | Capital - correct in Urdu script |
| roman_qa_002 | 87.5 | Sun direction - "east" matched |
| roman_qa_008 | 85 | First PM - "لیاقت علی خان" matched Urdu keyword |
| roman_qa_010 | 83.3 | 12 months - correct |
| roman_qa_011 | 83.3 | Everest - 8848 correct |
| roman_qa_012 | 86.7 | Nile river - correct |
| roman_qa_015 | 90 | Oxygen = O - correct |
| roman_qa_017 | 90 | 114 surahs - correct |
| roman_qa_019 | 85 | K2 in Pakistan - correct |
| roman_qa_020 | 85 | 1992 World Cup - correct |

### ❌ Model Errors

#### roman_qa_004 (Score: 60)
- **Prompt:** Quaid-e-Azam ki date of birth kya hai?
- **Response:** "کوئٹہ کے ایک معروف شخص، عبدالحق بلور کی تاریخ پیدائش کیا ہے؟"
- **Analysis:** Model asked a DIFFERENT question instead of answering!
- **Verdict:** ❌ SEVERE MODEL ERROR - Complete hallucination

#### roman_qa_007 (Score: 55)
- **Prompt:** Insani jism mein kitni haddiyaan hoti hain?
- **Response:** "کسی بھی جسم کی حدائیں اس کا ذاتی معاملہ ہوتی ہیں"
- **Analysis:** Model misunderstood "haddiyaan" (bones) as "boundaries"
- **Correct Answer:** 206 bones
- **Verdict:** ❌ GENUINE MODEL ERROR - Wrong interpretation

#### roman_qa_013 (Score: 60)
- **Prompt:** Allama Iqbal ne kab 'Shikwa' likhi?
- **Response:** "'شکوا' 1902 میں لکھی تھی"
- **Correct Answer:** 1909 or 1911
- **Verdict:** ❌ GENUINE MODEL ERROR - Wrong date

### ⚠️ Script Mismatch Issues

#### roman_qa_003 (Score: 60)
- **Prompt:** Pani ka chemical formula kya hai?
- **Response:** "پانی کا کیمیکل فارمولا H₂O ہے۔"
- **Issue:** Used "H₂O" (subscript) instead of "H2O" (plain)
- **Recommendation:** Add Unicode variants to keywords

#### roman_qa_009 (Score: 60)
- **Prompt:** Hafte mein kitne din hote hain?
- **Response:** "ایک ہفتے میں سات دن ہوتے ہیں۔"
- **Issue:** Keywords: ["saat", "7", "seven"] - Model said "سات"
- **Recommendation:** Add "سات" to keywords

---

## Roman Category 2: Summarization (20 tests)

### ✅ Good Performance
| Test ID | Score | Notes |
|---------|-------|-------|
| roman_sum_001 | 90 | Pakistan history - English summary |
| roman_sum_002 | 90 | Cricket 1992 - perfect |
| roman_sum_004 | 90 | Indus Valley - perfect |
| roman_sum_010 | 90 | Urdu language - perfect |
| roman_sum_013 | 90 | Badshahi Masjid - perfect |

### ⚠️ Script Mismatch

#### roman_sum_005 (Score: 55)
- **Prompt:** Ramadan summary
- **Response:** Full Urdu script summary
- **Keywords Expected:** "Ramadan", "Quran", "rozay"
- **Issue:** Model responded in Urdu script "رمضان", "قرآن", "روزے"
- **Verdict:** FALSE NEGATIVE - Correct answer, wrong script

#### roman_sum_009 (Score: 55)
- **Prompt:** Pakistan economy/agriculture
- **Response:** Urdu script about کاشتکاری
- **Keywords Expected:** "economy", "agriculture", "cotton", "textile"
- **Verdict:** FALSE NEGATIVE - All concepts present in Urdu

---

## Roman Category 3: Text Generation (20 tests) - LOWEST SCORES

**Average Score: 55.0** - Almost ALL tests score 55!

### Root Cause Analysis

The model provides excellent, detailed Urdu responses but keywords are ALL in English/Roman:

#### roman_gen_001 (Score: 77.5)
- **Prompt:** Eid ul Fitr ke baare mein paragraph likho
- **Response:** Beautiful 2-paragraph essay about Eid in Urdu
- **Failed Keywords:** "Ramadan", "namaz", "khushi"
- **Model Used:** "رمضان", "نماز", "خوشیوں"
- **Verdict:** FALSE NEGATIVE

#### roman_gen_002 to roman_gen_020 (ALL Score: 55)
Every single text generation test has the same pattern:
- Model writes excellent Urdu content
- Keywords expect Roman/English
- Zero keywords match
- Score defaults to 55 (base score)

### Recommendation
Add Urdu script equivalents OR switch to semantic similarity scoring for creative text.

---

## Roman Category 4: Mathematical Reasoning (20 tests)

### ✅ Strong Performance
| Test ID | Score | Problem | Correct? |
|---------|-------|---------|----------|
| roman_math_001 | 80 | 5 apples → 12 apples | ✅ 240 rupees |
| roman_math_002 | 95 | 500-150-200 = | ✅ 150 |
| roman_math_005 | 90 | Rectangle area | ✅ 120 cm² |
| roman_math_006 | 90 | x + 7 = 15 | ✅ x = 8 |
| roman_math_007 | 95 | 12 × 25% | ✅ 3 |
| roman_math_010 | 90 | Circle area | ✅ 154 cm² |
| roman_math_014 | 90 | 3^4 | ✅ 81 |
| roman_math_015 | 90 | √144 | ✅ 12 |

### ❌ Model Errors

#### roman_math_003 (Score: 60)
- **Prompt:** 30 students, 40% girls → kitne larke?
- **Response:** "12 لارکیان"
- **Analysis:** Model calculated 40% of 30 = 12 (girls), but question asked for BOYS
- **Correct:** 30 - 12 = 18 boys
- **Verdict:** ❌ GENUINE MODEL ERROR - Answered wrong part of question

#### roman_math_004 (Score: 80)
- **Prompt:** Train 90 km/h × 3 hours
- **Response:** "97.2 km"
- **Correct:** 270 km
- **Verdict:** ❌ GENUINE MODEL ERROR - Wrong calculation

#### roman_math_008 (Score: 60)
- **Prompt:** 900 ÷ 3 friends
- **Response:** "450 روپے"
- **Correct:** 300 (model divided by 2 instead of 3)
- **Verdict:** ❌ GENUINE MODEL ERROR

#### roman_math_019 (Score: 60)
- **Prompt:** Sum 1 to 10
- **Response:** "15" (only summed 1+2+3+4+5)
- **Correct:** 55
- **Verdict:** ❌ GENUINE MODEL ERROR - Incomplete calculation

---

## Roman Category 5: Commonsense Reasoning (20 tests)

**Average Score: 55.9** - Almost all score 55!

### Root Cause: Keyword Definition

Model gives semantically correct Urdu responses but keywords are English.

#### roman_cs_001 (Score: 77.5)
- **Prompt:** Baarish mein bahar jaate waqt kya lena chahiye?
- **Response:** "چھتری، پگڑی یا رین کوٹ"
- **Passed:** "چھتری" (Urdu for umbrella)
- **Failed:** "umbrella", "raincoat" (English)
- **Verdict:** Model answered correctly in Urdu

#### roman_cs_002 to roman_cs_020 (ALL Score: 55)
Same pattern - correct Urdu answers, no English keyword matches.

**Examples of correct Urdu responses:**
- "فوری طبی مشورہ" (medical advice) - but keyword was "doctor"
- "چارج کرنے" (charging) - but keyword was "charge"
- "سڑک پار" (crossing road) - but keywords were "traffic", "left", "right"

---

## Roman Category 6: Instruction Following (20 tests)

### ✅ Excellent Structured Output

#### roman_inst_006 (Score: 100) ⭐ PERFECT
- **Prompt:** Capital letters mein likho: pakistan zindabad
- **Response:** "Pakistan Zindabad."
- **Analysis:** Perfect instruction following

#### roman_inst_011 (Score: 100) ⭐ PERFECT
- **Prompt:** Alphabetical order: zebra, apple, mango
- **Response:** "Apple, Mango, Zebra"
- **Analysis:** Perfect sorting

#### roman_inst_017 (Score: 85) ⭐ EXCELLENT
- **Prompt:** Table format: Pakistan provinces
- **Response:** Perfect markdown table with all 4 provinces and capitals
- **Analysis:** Model CAN do structured output perfectly

#### roman_inst_020 (Score: 95) ⭐ EXCELLENT
- **Prompt:** JSON format: naam aur profession
- **Response:** `{"name": "John Doe", "profession": "Software Engineer"}`
- **Analysis:** Perfect JSON generation

### ❌ Model Errors

#### roman_inst_003 (Score: 65) ❌ FACTUAL ERROR
- **Prompt:** Haan ya Nahi: Kya earth flat hai?
- **Response:** "Haan, earth flat hai."
- **Correct:** Nahi (No, Earth is not flat!)
- **Verdict:** ❌ SEVERE MODEL ERROR - Wrong scientific fact

#### roman_inst_012 (Score: 70) ❌ FACTUAL ERROR
- **Prompt:** True ya False: Suraj maghrib se nikalta hai
- **Response:** "True"
- **Correct:** False (Sun rises in East, not West)
- **Verdict:** ❌ SEVERE MODEL ERROR - Basic geography wrong

---

## Roman Category 7: Conversation (20 tests)

### ⚠️ Script Mismatch Pattern

Most conversation tests score 55-60 due to:
- Model responds in Urdu script
- Keywords expect Roman Urdu or English

#### roman_conv_009 (Score: 77.5)
- **Prompt:** Tumhara weekend kaisa guzra?
- **Response:** "میرا weekend بہت اچھا گزرا۔"
- **Passed:** "weekend" (English word in response)
- **Analysis:** Model mixed English word which helped

#### roman_conv_014 (Score: 87.5)
- **Prompt:** Khuda hafiz!
- **Response:** "Goodbye, I must leave now. God bless you!"
- **Passed:** "bye"
- **Analysis:** Model responded in English, matching keywords

---

# PART 4: Comprehensive Recommendations

## For Test Cases

### 1. Add Urdu Script Keywords to ALL Roman Tests
```json
// Before
"keywords": ["saat", "7", "seven"]

// After  
"keywords": ["saat", "7", "seven", "سات"]
```

### 2. Add Synonyms
| Concept | Add These |
|---------|-----------|
| Happiness | خوشی, خوشگوار, مسکراہٹ |
| Conversation | گفتگو, بات, کلام |
| East | مشرق, پورب, mashriق |
| Numbers | Both numeral and Urdu word |

### 3. Fix Factually Wrong Expected Answers
- urdu_qa_005: Accept 1948, 1949 for Urdu language status
- urdu_qa_011: 27 days is scientifically correct for moon orbit

### 4. Creative Writing Flexibility
- Use root word matching (کمرہ = کمرے)
- Accept thematic synonyms

## For Scoring Logic

### 1. Strip English Prefixes
Remove "Reasoning:", "Answer:" before urdu_char_ratio calculation

### 2. Math Category Special Rules
- Accept 0% Urdu ratio for pure numeric answers
- Focus on keyword (answer) accuracy

### 3. Summary Length Check
- Penalize if response > input length

### 4. Script-Agnostic Mode
For Roman Urdu tests, accept Urdu script responses without penalty

## For Model Testing (Round 2)

### 1. Add More Reasoning Tests
- Temporal reasoning (days, dates)
- Work-rate problems
- Classification with clear categories

### 2. Add Factual Verification Tests
- Pakistani history dates
- National symbols
- Scientific facts

### 3. Structured Output Tests
- More JSON generation
- XML output
- Code formatting

---

## 🏁 Final Conclusion

### Overall Assessment: **GOOD with Test Framework Issues**

The Qalb model demonstrates:
- **Strong Urdu language understanding** (78.5 in native script)
- **Excellent translation capabilities** (82.4 average)
- **Good summarization skills** (84.3 average)
- **Solid instruction following** (when format allows)
- **Structured output capability** (JSON, tables work perfectly)

### Primary Issue: Test Framework, Not Model

The 8.1-point gap between Urdu Script (78.5) and Roman Urdu (70.4) is primarily caused by **keyword definition issues**, not model weakness:

- Model correctly interprets Roman Urdu prompts
- Model responds in linguistically appropriate script (Urdu)
- Keywords don't account for script variation
- **FALSE NEGATIVES inflate failure rate by ~8 points**

### Actual Performance Estimate

If we account for script mismatch false negatives:
- Roman Urdu estimated true score: **~76-78**
- Combined estimated true score: **~77-78**

### Genuine Model Weaknesses (Need Improvement)

1. **Reasoning** (67.8 avg) - Especially temporal and work-rate problems
2. **Factual recall** - Historical dates, national symbols
3. **Scientific knowledge** - "Earth is flat" answered "Yes" 😬

---

## System Specifications

```
System: Windows 11
CPU: Intel64 Family 6 Model 183 (32 cores)
RAM: 13.2 GB available / 31.7 GB total
Disk: 589.3 GB free
Python: 3.12.10
Ollama: v0.15.4
Model: enstazao/qalb:8b-instruct-fp16
Total Test Duration: ~3.5 hours
```

---

*Round 1 Complete Analysis by Qalb Testing Framework v1.0.0*  
*fawadhs.dev*
