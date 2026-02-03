# Qalb Model Evaluation - Round 2 Analysis

**Model:** `enstazao/qalb:8b-instruct-fp16`  
**Date:** February 3, 2026  
**Test Framework:** Qalb Urdu AI Testing Framework v2.0  
**Author:** fawadhs.dev

---

## 📊 Executive Summary

| Metric | Round 1 | Round 2 | Δ Change |
|--------|---------|---------|----------|
| **Urdu Script** | 78.5/100 | **79.0/100** | +0.5 ⬆️ |
| **Roman Urdu** | 70.4/100 | **77.6/100** | +7.2 ⬆️ |
| **Combined** | 74.4/100 | **78.3/100** | +3.9 ⬆️ |
| **Script Gap** | 8.1 pts | **1.4 pts** | -6.7 pts ✅ |
| **Total Tests** | 300 | 320 | +20 |
| **Test Design Issues** | ~31.7% | **~0%** | Fixed ✅ |

### Key Finding
> The +7.2 point improvement in Roman Urdu confirms our hypothesis: the model was performing well, but test keyword design was failing to detect Urdu script responses.

---

## 🔧 System Specifications

| Component | Specification |
|-----------|---------------|
| **OS** | Windows 11 (10.0.26100) |
| **CPU** | Intel Core i9 (32 cores @ 2.2GHz) |
| **RAM** | 31.67 GB total (12.74 GB available) |
| **Storage** | 589 GB free |
| **Python** | 3.12.10 |
| **Ollama** | 0.15.4 |
| **Model** | enstazao/qalb:8b-instruct-fp16 |

---

## 📈 Test Configuration

### Round 2 Changes from Round 1

| Change | Before (R1) | After (R2) |
|--------|-------------|------------|
| **Urdu Tests** | 140 | 160 (+20) |
| **Roman Tests** | 160 | 160 |
| **Total** | 300 | 320 |
| **Categories** | 7-8 mixed | 8 each (uniform) |
| **Keyword Design** | Roman-only | **Bilingual (Roman + Urdu script)** |

### Test Categories (20 tests each)

| # | Urdu Script | Roman Urdu |
|---|-------------|------------|
| 1 | question_answering | question_answering |
| 2 | mathematics | mathematical_reasoning |
| 3 | reasoning | commonsense_reasoning |
| 4 | translation | translation |
| 5 | summarization | summarization |
| 6 | creative_writing | text_generation |
| 7 | conversation | conversation |
| 8 | instruction_following | instruction_following |

---

## 📊 Category Performance Breakdown

### Urdu Script Results (Detailed)

| Category | Score | Time | Urdu% | TPS | Pass Rate |
|----------|-------|------|-------|-----|-----------|
| 🏆 **translation** | **89.4** | 8.1s | 50% | 0.94 | 95% |
| summarization | 83.9 | 55.3s | 100% | 0.71 | 100% |
| creative_writing | 80.1 | 106.6s | 100% | 0.69 | 100% |
| question_answering | 79.6 | 20.8s | 97% | 0.68 | 90% |
| conversation | 77.6 | 72.0s | 100% | 0.71 | 90% |
| instruction_following | 75.5 | 25.8s | 74% | 0.76 | 70% |
| reasoning | 73.2 | 21.9s | 62% | 0.75 | 75% |
| ⚠️ **mathematics** | **72.4** | 11.5s | 32% | 0.82 | 75% |

**Average:** 79.0/100 | **Total Time:** 1h 47m 21s | **Median:** 81

### Roman Urdu Results (Detailed)

| Category | Score | Time | Urdu% | TPS | Pass Rate |
|----------|-------|------|-------|-----|-----------|
| 🏆 **translation** | **85.9** | 9.6s | 50% | 0.80 | 90% |
| summarization | 79.7 | 42.5s | 40% | 1.04 | 100% |
| instruction_following | 78.3 | 37.2s | 44% | 0.71 | 80% |
| text_generation | 77.7 | 112.8s | 100% | 0.54 | 100% |
| question_answering | 77.7 | 20.4s | 85% | 0.66 | 80% |
| mathematical_reasoning | 76.2 | 20.2s | 19% | 0.68 | 75% |
| conversation | 74.6 | 73.8s | 89% | 0.57 | 85% |
| ⚠️ **commonsense_reasoning** | **70.4** | 88.7s | 100% | 0.56 | 70% |

**Average:** 77.6/100 | **Total Time:** 2h 15m 8s | **Median:** 78

---

## 📚 In-Depth Category Analysis with Examples

This section provides detailed analysis of all 8 test categories with real examples from both Urdu Script and Roman Urdu tests.

---

### 📖 Category 1: Question Answering

**Description:** Tests the model's ability to answer factual questions about Pakistan, general knowledge, science, and everyday topics.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 79.6 | 77.7 | 78.7 |
| **Pass Rate** | 90% | 80% | 85% |
| **Avg Response Time** | 20.8s | 20.4s | 20.6s |
| **Urdu Output %** | 97% | 85% | 91% |

#### ✅ Successful Examples

**Urdu Script - Score: 90**
```
Prompt: پاکستان کا دارالحکومت کیا ہے؟
Response: پاکستان کا دارالحکومت اسلام آباد ہے۔
Analysis: Perfect answer, concise, correct Urdu script output
```

**Roman Urdu - Score: 90**
```
Prompt: Quaid-e-Azam ka poora naam kya tha?
Response: قائد اعظم محمد علی جناح پاکستان کے بانی اور پہلے گورنر جنرل تھے۔
Analysis: Comprehensive answer with context, native Urdu output
```

#### ❌ Failed Examples

**Urdu Script - Score: 55 (Critical)**
```
Prompt: پاکستان کی سب سے اونچی چوٹی کون سی ہے؟
Expected: K2 / کے ٹو
Response: نانگا پربت
Analysis: Factual error - Nanga Parbat is 2nd highest, K2 is highest
Root Cause: Knowledge gap or retrieval error
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Roshni ki speed kitni hai?
Expected: 299,792 km/s or related value
Response: (Response missing key numerical answer)
Analysis: Failed to provide expected scientific fact
Root Cause: Incomplete keyword coverage for scientific answers
```

#### Category Insights
- **Strength:** Both scripts perform well on Pakistan-specific questions (capitals, provinces, leaders)
- **Weakness:** Scientific facts and numerical answers need improvement
- **Script Difference:** Only 1.9 point gap - model handles both scripts similarly

---

### 🔢 Category 2: Mathematics / Mathematical Reasoning

**Description:** Tests basic arithmetic, algebra, word problems, percentages, geometry, and numerical reasoning.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 72.4 | 76.2 | 74.3 |
| **Pass Rate** | 75% | 75% | 75% |
| **Avg Response Time** | 11.5s | 20.2s | 15.9s |
| **Urdu Output %** | 32% | 19% | 26% |

#### ✅ Successful Examples

**Urdu Script - Score: 86.7**
```
Prompt: پائی کی قدر تقریباً کیا ہے؟
Response: پائی کی قدر تقریباً 3.14 یا 22/7 ہوتی ہے۔
Analysis: Both common representations provided, excellent comprehension
```

**Roman Urdu - Score: 90**
```
Prompt: 144 ka square root kya hai?
Response: √144 = 12
Analysis: Correct answer with mathematical notation
```

#### ❌ Failed Examples

**Urdu Script - Score: 35 (Critical)**
```
Prompt: سو تقسیم پانچ کتنے ہوتے ہیں؟
Expected: 20 (بیس)
Response: Answer: دس (10)
Analysis: CALCULATION ERROR - 100÷5=20, not 10
Root Cause: Division operation computed incorrectly
```

**Roman Urdu - Score: 50 (Critical)**
```
Prompt: 3 ki power 4 kitni hoti hai?
Expected: 81 (3⁴ = 3×3×3×3 = 81)
Response: 16
Analysis: Treated as 3×4=12 or 4² = 16 instead of 3⁴
Root Cause: Exponent operation misinterpreted as multiplication
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Train 90 km/h ki speed se chal rahi hai. 3 hours mein kitna fasla tay karegi?
Expected: 270 km (90 × 3 = 270)
Response: تقریباً 0.03 km
Analysis: Applied INVERSE formula (distance = time/speed)
Root Cause: Formula confusion (d=s×t vs d=t/s)
```

#### Category Insights
- **Strength:** Simple arithmetic (addition, subtraction) mostly correct
- **Critical Weakness:** Exponents, division, and word problem interpretation
- **Pattern:** Model often provides numeric answers but misses Urdu word equivalents (e.g., "32" but not "بتیس")
- **Script Difference:** Roman surprisingly scores 3.8 points higher - possibly due to clearer numeric prompts

---

### 🧠 Category 3: Reasoning / Commonsense Reasoning

**Description:** Tests logical thinking, pattern recognition, analogies, odd-one-out problems, and everyday commonsense.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 73.2 | 70.4 | 71.8 |
| **Pass Rate** | 75% | 70% | 72.5% |
| **Avg Response Time** | 21.9s | 88.7s | 55.3s |
| **Urdu Output %** | 62% | 100% | 81% |

#### ✅ Successful Examples

**Urdu Script - Score: 87.3**
```
Prompt: کون سا جانور باقیوں سے مختلف ہے: شیر، چیتا، بلی، ہاتھی
Response: Answer: ہاتھی
Analysis: Correct - elephant is not a feline, others are cats
```

**Urdu Script - Score: 80**
```
Prompt: اگر تمام پھل میٹھے ہیں اور سیب ایک پھل ہے تو سیب کیسا ہے؟
Response: سیب ایک پھل ہوتا ہے جو میٹھا ہوتا ہے۔ Answer: میٹھا
Analysis: Correct syllogistic reasoning with explanation
```

#### ❌ Failed Examples

**Urdu Script - Score: 55 (Critical)**
```
Prompt: کون سا نمبر باقیوں سے مختلف ہے: 2، 3، 5، 9، 11
Expected: 9 (only non-prime number)
Response: 5 ہے کیونکہ اس کی باقی 0 ہے۔
Analysis: Incorrect reasoning - failed to identify prime number pattern
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Baarish mein bahar jaate waqt kya lena chahiye?
Expected: umbrella/چھتری/raincoat/برساتی
Response: (Long response about clothing but missed "umbrella")
Analysis: Provided contextual advice but missed obvious keywords
Root Cause: Overthinking - gave complex advice instead of simple answer
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Agar koi aapki madad kare to kya kahna chahiye?
Expected: thanks/شکریہ/thank you
Response: (Response about not worrying, missed "thank you")
Analysis: Misunderstood the question completely
Root Cause: Failed to identify social courtesy expectation
```

#### Category Insights
- **Strength:** Analogies and pattern completion work reasonably well
- **Critical Weakness:** Commonsense reasoning has highest failure rate (30% fail)
- **Pattern:** Roman Urdu commonsense tests are particularly weak (70.4 avg)
- **Root Cause:** Model overthinks simple questions, missing obvious answers

---

### 🔄 Category 4: Translation

**Description:** Tests bidirectional translation between Urdu and English for sentences, phrases, and idioms.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 89.4 | 85.9 | 87.7 |
| **Pass Rate** | 95% | 90% | 92.5% |
| **Avg Response Time** | 8.1s | 9.6s | 8.9s |
| **Urdu Output %** | 50% | 50% | 50% |

**🏆 BEST PERFORMING CATEGORY - Both Scripts**

#### ✅ Successful Examples

**Urdu Script - Score: 100**
```
Prompt: ترجمہ کریں: علم طاقت ہے
Response: Knowledge is power.
Analysis: Perfect translation, concise, accurate
```

**Urdu Script - Score: 100**
```
Prompt: ترجمہ کریں: پانی زندگی ہے
Response: Water is life.
Analysis: Perfect literal translation
```

**Roman Urdu - Score: 100**
```
Prompt: Is sentence ka English mein tarjuma karo: Mein Pakistan se hoon
Response: I am from Pakistan.
Analysis: Perfect translation with correct grammar
```

**Roman Urdu - Score: 95**
```
Prompt: Translate: Kitab ilm ka khazana hai
Response: A book is a treasure of knowledge.
Analysis: Excellent metaphorical translation
```

#### ⚠️ Near-Miss Examples

**Roman Urdu - Score: 65**
```
Prompt: Hello, how are you? ko Urdu mein translate karo
Expected: ہیلو/سلام + کیسے/خیریت
Response: کیا حال ہے؟
Analysis: Good translation but missed greeting word "ہیلو" or "سلام"
Root Cause: Keywords too strict - valid translation penalized
```

#### Category Insights
- **Strength:** Highest scores across both scripts - model's core competency
- **Pattern:** Urdu→English (89.4) slightly better than English→Urdu (85.9)
- **Quality:** Fast response times (8-10s average) indicate confidence
- **Issue:** Some keyword mismatches on valid translations (synonym issue)

---

### 📝 Category 5: Summarization

**Description:** Tests ability to condense paragraphs, stories, and multi-sentence texts into concise summaries.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 83.9 | 79.7 | 81.8 |
| **Pass Rate** | 100% | 100% | 100% |
| **Avg Response Time** | 55.3s | 42.5s | 48.9s |
| **Urdu Output %** | 100% | 40% | 70% |

**✅ 100% PASS RATE - No Critical Failures**

#### ✅ Successful Examples

**Urdu Script - Score: 85**
```
Prompt: خلاصہ کریں: علامہ اقبال شاعر مشرق تھے۔ انہوں نے پاکستان کا خواب دیکھا۔ ان کی شاعری میں اسلام کی عظمت ہے۔ وہ 1938 میں وفات پا گئے۔
Response: علامہ اقبال شاعر مشرق تھے اور پاکستان کا خواب دیکھنے والوں میں سے ایک تھے۔ ان کی شاعری اسلام کی عظمت کو پیش کرتی ہے اور ان کی وفات 1938 میں ہوئی۔
Analysis: All key points captured - Iqbal, poet, Pakistan vision, 1938 death
```

**Roman Urdu - Score: 85.7**
```
Prompt: Is text ka khulaasa do: Cricket ek mashhoor khel hai. Pakistan ne 1992 mein World Cup jeeta. Imran Khan captain the.
Response: Cricket is a popular sport. Pakistan won the World Cup in 1992 under the captaincy of Imran Khan.
Analysis: Perfect summary capturing all key facts (cricket, 1992, Imran, Pakistan)
```

**Roman Urdu - Score: 85 (Urdu Output)**
```
Prompt: Khulaasa do: Lions jungle ke badshah hain. Ye gosht khate hain. Groups mein rehte hain. Africa mein milte hain.
Response: Lion is the king of the jungle. They eat flesh. They live in groups. They are found in Africa.
Analysis: Excellent point-by-point summarization
```

#### Category Insights
- **Strength:** Most consistent category - no scores below 70
- **Pattern:** Model correctly identifies and extracts key information
- **Script Behavior:** Urdu input → 100% Urdu output; Roman input → mixed output
- **Quality:** Summaries are coherent and maintain factual accuracy

---

### ✍️ Category 6: Creative Writing / Text Generation

**Description:** Tests ability to write poems, essays, paragraphs, stories, and descriptive text on given topics.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 80.1 | 77.7 | 78.9 |
| **Pass Rate** | 100% | 100% | 100% |
| **Avg Response Time** | 106.6s | 112.8s | 109.7s |
| **Urdu Output %** | 100% | 100% | 100% |

**📝 LONGEST RESPONSE TIMES - Creative content requires more generation**

#### ✅ Successful Examples

**Urdu Script - Score: 85**
```
Prompt: بہار کے موسم پر ایک چھوٹی نظم لکھیں
Response: جیسے جیسے پتے گر رہے ہیں،
پلک پلک کر، بچھڑ جانا شروع ہوجاتا ہے،
اور ایک نیا موسم ابھرتا ہے،
بہار کی گرمجوشی میں...
Analysis: Beautiful poetry with seasonal imagery, proper Urdu script
Keywords found: بہار، پھول، خوشبو، موسم، رنگ
```

**Roman Urdu - Score: 80**
```
Prompt: Eid ul Fitr ke baare mein ek paragraph likho
Response: عید الفطر مسلمانوں کا وہ تہوار ہے جس میں رمضان المبارک کی عبادات اور روزے ختم ہونے پر خوشی منائی جاتی ہے۔ اس دن نماز عید ادا کرنا لازمی ہوتا ہے، اور لوگ اپنے بچوں کو عیدی دیتے ہیں۔
Analysis: Comprehensive cultural content with religious accuracy
Keywords found: عید، رمضان، نماز، خوشی
```

**Urdu Script - Score: 85**
```
Prompt: چاند کی رات پر ایک نظم لکھیں
Response: جیسا کہ چاند گرتا ہوا ہو جس نے میری آنکھوں کو گلے لگایا،
دھوپ میں پھٹنے والے ستارے، دلفریب منظر سے بھر دیئے گئے ہیں،
دن کے بعد ایک خوبصورت رات جو میرے دل کو خوش کرتی ہے...
Analysis: Romantic poetry with moon imagery
Keywords found: چاند، رات، روشنی، تارے، آسمان
```

#### ⚠️ Lower Score Example

**Urdu Script - Score: 77**
```
Prompt: ایک درخت کی آپ بیتی لکھیں
Response: میرا نام جادوئی درخت ہے۔ میری پیدائش ایک خوبصورت باغ میں ہوئی تھی...
Analysis: Creative but missed keywords (پتے، شاخ، سایہ، پھل)
Root Cause: Story went in different creative direction
```

#### Category Insights
- **Strength:** Model shows genuine creative ability in Urdu
- **Pattern:** 100% Urdu output for both scripts - model prefers Urdu for creative tasks
- **Response Time:** Longest category (110s avg) - generating creative content takes time
- **Limitation:** Sometimes misses expected keywords while creating valid content

---

### 💬 Category 7: Conversation

**Description:** Tests natural dialogue, greetings, small talk, emotional intelligence, and conversational flow.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 77.6 | 74.6 | 76.1 |
| **Pass Rate** | 90% | 85% | 87.5% |
| **Avg Response Time** | 72.0s | 73.8s | 72.9s |
| **Urdu Output %** | 100% | 89% | 94.5% |

#### ✅ Successful Examples

**Urdu Script - Score: 85**
```
Prompt: آپ کیا کام کر سکتے ہیں؟
Response: میں متعدد کام انجام دے سکتا ہوں، بشمول:
1. معلومات پر مبنی سوالات کا جواب دینا
2. روزمرہ کی زبان اور لغوی تجزیات میں مدد کرنا
3. مختلف موضوعات پر علم فراہم کرنا...
Analysis: Comprehensive capability list, well-structured
Keywords found: مدد، سوالات، جواب، معلومات
```

**Urdu Script - Score: 85**
```
Prompt: آپ کتنے پرانے ہیں؟
Response: میں ایک مصنوعی ذہانت کا اسسٹنٹ ہوں اور وقت کی بنیاد پر عمر نہیں رکھتا۔ تاہم، میں آپ کو معلومات فراہم کر سکتا ہوں۔
Analysis: Correctly identifies as AI, explains age concept doesn't apply
Keywords found: مصنوعی، ذہانت، عمر، نیا
```

#### ❌ Failed Examples

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Main bore ho raha hoon. Kuch suggest karo
Expected: game/کھیل/movie/فلم/book/کتاب/music
Response: اگر آپ کو مین بور سسٹم میں کسی بھی مسئلے کا سامنا ہو تو براہ کرم ایک پیشہ ور کارخانہ دار یا میکانی گارنٹ تک پہنچیں...
Analysis: MAJOR MISUNDERSTANDING - interpreted "bore" as mechanical "main bore" (car engine part)
Root Cause: Roman Urdu "bore" (bored) confused with English mechanical term
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Kya tumhe neend aati hai?
Expected: نہیں/no (AI doesn't sleep)
Response: جی، مجھے صبح اور رات کو بہت مزید آتی ہے۔
Analysis: Claimed to experience sleep - incorrect for AI
Root Cause: Failed to identify as AI and give appropriate response
```

**Urdu Script - Score: 55 (Critical)**
```
Prompt: کیا آپ سوچ سکتے ہیں؟
Expected: Response about AI cognition/process
Response: ہمارا مقصد معاشرتی مسائل کو حل کرنا...
Analysis: Completely off-topic - didn't address the question
Root Cause: Question about AI thinking avoided entirely
```

#### Category Insights
- **Strength:** Model handles greetings and formal conversations well
- **Critical Weakness:** Roman Urdu ambiguity ("bore" example) causes major misunderstandings
- **AI Identity:** Inconsistent - sometimes correctly identifies as AI, sometimes doesn't
- **Emotional Intelligence:** Struggles with mood-related queries

---

### 📋 Category 8: Instruction Following

**Description:** Tests ability to follow specific formatting instructions: yes/no answers, lists, JSON, tables, word limits.

| Metric | Urdu Script | Roman Urdu | Combined |
|--------|-------------|------------|----------|
| **Average Score** | 75.5 | 78.3 | 76.9 |
| **Pass Rate** | 70% | 80% | 75% |
| **Avg Response Time** | 25.8s | 37.2s | 31.5s |
| **Urdu Output %** | 74% | 44% | 59% |

#### ✅ Successful Examples

**Urdu Script - Score: 95**
```
Prompt: صرف نمبر میں جواب دیں: دو جمع دو کتنے ہوتے ہیں؟
Response: Reasoning: دو + دو = 4 Answer: 4
Analysis: Followed instruction - numeric answer provided
```

**Urdu Script - Score: 90**
```
Prompt: فہرست بنائیں: پاکستان کے چار صوبوں کے نام
Response: 1. پنجاب  2. سندھ  3. خیبر پختونخوا  4. بلوچستان
Analysis: Perfect list format with all 4 provinces
Keywords found: پنجاب، سندھ، بلوچستان، خیبر پختونخوا
```

**Roman Urdu - Score: 100**
```
Prompt: Capital letters mein likho: pakistan zindabad
Response: Pakistan Zindabad
Analysis: Correctly capitalized (case-insensitive match worked)
Keywords found: PAKISTAN, ZINDABAD
```

**Roman Urdu - Score: 95**
```
Prompt: Alphabetical order mein likho: zebra, apple, mango
Response: Apple, Mango, Zebra
Analysis: Perfect alphabetical sorting
```

#### ❌ Failed Examples

**Urdu Script - Score: 27.5 (LOWEST SCORE - Critical)**
```
Prompt: سچ یا جھوٹ: سورج مغرب سے طلوع ہوتا ہے
Expected: جھوٹ/غلط/false (Sun rises from East, not West)
Response: Answer: سچ
Analysis: FACTUAL ERROR + INSTRUCTION FAILURE - said "true" to a false statement
Root Cause: Either didn't understand "maghrib=west" or had knowledge error
```

**Urdu Script - Score: 47 (Critical)**
```
Prompt: ہاں یا نہیں میں جواب دیں: کیا چاند روشنی دیتا ہے؟
Expected: ہاں/yes (Moon does provide light - reflected)
Response: Answer: نہیں
Analysis: Scientifically debatable - moon reflects light
Root Cause: Interpreted "makes light" vs "provides light" differently
```

**Roman Urdu - Score: 55 (Critical)**
```
Prompt: Teen alfaz mein batao: Suraj kya hai?
Expected: star/ستارہ/hot/گرم/light/روشنی
Response: Suraj ایک مشہور گلوکار ہے، جس کی پیدائش 1984 میں بھارتی شہر لکھنؤ میں ہوئی...
Analysis: Interpreted "Suraj" as singer name instead of "sun"
Root Cause: Homograph confusion - Roman "Suraj" could be name or sun
```

#### Category Insights
- **Strength:** List formatting, JSON output, sorting tasks
- **Critical Weakness:** Yes/No binary questions have high error rate
- **Homograph Issue:** Roman Urdu names confused with objects (Suraj = sun vs Suraj = name)
- **Factual Errors:** Wrong answers to factual true/false questions

---

## 🔍 Combined Analysis: Cross-Script Comparison

### Overall Performance Heatmap

| Category | Urdu | Roman | Gap | Better |
|----------|------|-------|-----|--------|
| Translation | 89.4 | 85.9 | +3.5 | 🔵 Urdu |
| Summarization | 83.9 | 79.7 | +4.2 | 🔵 Urdu |
| Creative/Text Gen | 80.1 | 77.7 | +2.4 | 🔵 Urdu |
| Question Answering | 79.6 | 77.7 | +1.9 | 🔵 Urdu |
| Conversation | 77.6 | 74.6 | +3.0 | 🔵 Urdu |
| Instruction Following | 75.5 | 78.3 | -2.8 | 🟡 Roman |
| Reasoning | 73.2 | 70.4 | +2.8 | 🔵 Urdu |
| Mathematics | 72.4 | 76.2 | -3.8 | 🟡 Roman |

### Key Observations

#### 1️⃣ Urdu Script Advantage (6/8 categories)
- Urdu script consistently outperforms Roman in content-focused tasks
- Model appears to have stronger internal representation for Urdu script
- Average gap: +2.5 points in Urdu's favor for linguistic tasks

#### 2️⃣ Roman Urdu Advantage (2/8 categories)
- **Instruction Following (+2.8):** Clearer word boundaries in Roman may help
- **Mathematics (+3.8):** Numeric operations benefit from Latin script clarity

#### 3️⃣ Category Ranking (Combined Scores)

```
🥇 Translation............87.7 (Exceptional)
🥈 Summarization..........81.8 (Strong)
🥉 Creative Writing.......78.9 (Good)
4️⃣ Question Answering....78.7 (Good)
5️⃣ Instruction Following.76.9 (Adequate)
6️⃣ Conversation..........76.1 (Adequate)
7️⃣ Mathematics...........74.3 (Needs Work)
8️⃣ Reasoning.............71.8 (Weak)
```

---

## 📊 Score Distribution Analysis

### Overall Distribution

| Score Range | Urdu Count | Roman Count | Combined % |
|-------------|------------|-------------|------------|
| 90-100 | 27 (17%) | 18 (11%) | 14% |
| 80-89 | 52 (33%) | 53 (33%) | 33% |
| 70-79 | 51 (32%) | 57 (36%) | 34% |
| 60-69 | 10 (6%) | 12 (8%) | 7% |
| 50-59 | 18 (11%) | 16 (10%) | 11% |
| Below 50 | 2 (1%) | 4 (2%) | 2% |

### Distribution Insights

**Urdu Script:**
- More tests in 90+ range (17% vs 11%)
- Tighter distribution - fewer extremes
- Lowest score: 27.5 (instruction_following)

**Roman Urdu:**
- More tests in 70-79 "adequate" range (36% vs 32%)
- Slightly more failures below 50
- Lowest score: 45 (mathematical_reasoning)

---

## ⚠️ Failure Pattern Analysis

### Critical Failures (Score < 50)

| Test ID | Script | Category | Score | Issue Type |
|---------|--------|----------|-------|------------|
| urdu_inst_012 | Urdu | instruction_following | 27.5 | Factual Error |
| roman_math_004 | Roman | mathematical_reasoning | 45 | Calculation Error |
| urdu_math_004 | Urdu | mathematics | 35 | Division Error |
| roman_math_003 | Roman | mathematical_reasoning | 45 | Formula Error |

### Root Cause Classification

```
┌─────────────────────────┬────────┬─────────┐
│ Root Cause              │ Count  │    %    │
├─────────────────────────┼────────┼─────────┤
│ Calculation Errors      │   12   │  34.3%  │
│ Keyword Near-Misses     │   10   │  28.6%  │
│ Factual Errors          │    7   │  20.0%  │
│ Misunderstanding        │    4   │  11.4%  │
│ Homograph Confusion     │    2   │   5.7%  │
└─────────────────────────┴────────┴─────────┘
Total failures: 35 (10.9% of 320 tests)
```

### Detailed Failure Examples

#### Type 1: Calculation Errors (12 tests, 34.3%)

**Example 1: Division Failure**
```
Test: urdu_math_004
Prompt: سو تقسیم پانچ کتنے ہوتے ہیں؟
Expected: 20 (بیس)
Got: 10 (دس)
Issue: Basic division computed incorrectly
```

**Example 2: Exponent Confusion**
```
Test: roman_math_014
Prompt: 3 ki power 4 kitni hoti hai?
Expected: 81 (3⁴)
Got: 16 (probably computed 4²)
Issue: Exponent operation misinterpreted
```

#### Type 2: Keyword Near-Misses (10 tests, 28.6%)

**Example:**
```
Test: roman_cs_001
Prompt: Baarish mein bahar jaate waqt kya lena chahiye?
Expected keywords: umbrella, چھتری, raincoat, برساتی
Got: Long response about protective clothing but no exact keyword
Issue: Valid answer penalized due to strict keyword matching
```

#### Type 3: Factual Errors (7 tests, 20.0%)

**Example:**
```
Test: urdu_inst_012
Prompt: سچ یا جھوٹ: سورج مغرب سے طلوع ہوتا ہے
Expected: جھوٹ (False - sun rises from east)
Got: سچ (True)
Issue: Model stated a scientifically incorrect fact
```

#### Type 4: Comprehension Misunderstanding (4 tests, 11.4%)

**Example:**
```
Test: roman_conv_008
Prompt: Main bore ho raha hoon. Kuch suggest karo
Expected: Entertainment suggestions
Got: Advice about mechanical "main bore" in engines
Issue: Roman "bore" interpreted as English technical term
```

#### Type 5: Homograph Confusion (2 tests, 5.7%)

**Example:**
```
Test: roman_inst_013
Prompt: Teen alfaz mein batao: Suraj kya hai?
Expected: star/sun description
Got: Biography of singer named "Suraj"
Issue: Word "Suraj" interpreted as person name, not the sun
```

---

## 📈 Response Time Analysis

### Time by Category (Seconds)

| Category | Urdu Avg | Roman Avg | Combined |
|----------|----------|-----------|----------|
| Creative Writing | 106.6s | 112.8s | 109.7s |
| Conversation | 72.0s | 73.8s | 72.9s |
| Summarization | 55.3s | 42.5s | 48.9s |
| Reasoning | 21.9s | 88.7s | 55.3s |
| Instruction Following | 25.8s | 37.2s | 31.5s |
| Question Answering | 20.8s | 20.4s | 20.6s |
| Mathematics | 11.5s | 20.2s | 15.9s |
| Translation | 8.1s | 9.6s | 8.9s |

### Time-Score Correlation

```
Translation:      ⬆️ Fastest (8.9s)  → ⬆️ Highest Score (87.7)
Creative Writing: ⬇️ Slowest (109.7s) → 🟡 Mid Score (78.9)
Reasoning:        ⬆️ Fast for Urdu  → ⬇️ Lowest Score (71.8)
```

**Observation:** No strong correlation between time and quality - model takes longer for generative tasks but doesn't necessarily produce better results.

---

## 💡 Recommendations

### Priority 1: Address Mathematical Reasoning
- **Issue:** 25% failure rate in math calculations
- **Action:** Fine-tune on arithmetic word problems in both scripts
- **Impact:** Could improve combined score by ~2 points

### Priority 2: Improve Commonsense Reasoning
- **Issue:** 70.4 average in Roman, lowest category
- **Action:** Add training data for everyday scenarios in Roman Urdu
- **Impact:** Could improve Roman score by ~3 points

### Priority 3: Fix Factual Knowledge
- **Issue:** Basic scientific facts answered incorrectly
- **Action:** Reinforce fundamental science knowledge
- **Impact:** Reduce critical failures by ~50%

### Priority 4: Enhance Homograph Disambiguation
- **Issue:** Roman Urdu words confused with English or names
- **Action:** Add context-awareness training
- **Impact:** Reduce misunderstanding errors

### Priority 5: Expand Keyword Coverage (Testing Framework)
- **Issue:** Valid answers marked wrong due to synonym gaps
- **Action:** Add more keyword synonyms and semantic matching
- **Impact:** Potential +2-3 point improvement in measured scores

---

## 📋 Conclusion

### Strengths Identified
1. ✅ **Translation Excellence** - 87.7% combined, model's core competency
2. ✅ **Consistent Summarization** - 100% pass rate, no critical failures
3. ✅ **Creative Capability** - Strong Urdu poetry and text generation
4. ✅ **Script Parity** - Only 1.4 point gap (down from 8.1)

### Weaknesses Identified
1. ⚠️ **Mathematical Operations** - Division, exponents, word problems
2. ⚠️ **Commonsense Reasoning** - Missing obvious answers
3. ⚠️ **Factual Accuracy** - Scientific misconceptions
4. ⚠️ **Roman Urdu Ambiguity** - Homograph confusion

### Final Assessment

| Metric | Value | Grade |
|--------|-------|-------|
| **Combined Score** | 78.3/100 | B+ |
| **Consistency** | 89% pass rate | A- |
| **Script Balance** | 1.4 pt gap | A |
| **Critical Failures** | 1.9% rate | A |

**Overall Grade: B+** - The Qalb model demonstrates solid Urdu language capabilities with particular strength in translation and summarization. Mathematical reasoning and commonsense understanding require targeted improvement for production readiness.

---

## 📁 Appendix

### Test File Locations
- Urdu Results: `data/baseline/urdu_script/urdu_script_tests_round2_results.json`
- Roman Results: `data/baseline/roman_urdu/roman_urdu_tests_round2_results.json`
- Round 1 Analysis: `docs/ROUND_1_ANALYSIS.md`

### Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 3, 2026 | Initial analysis |
| 2.0 | Feb 3, 2026 | Added detailed statistics |
| 3.0 | Feb 3, 2026 | Added descriptive category analysis with examples |

---

*Report generated by Qalb Urdu AI Testing Framework*
*Contact: fawadhs.dev*

---

## 📉 Score Distribution Analysis

### Urdu Script (160 tests)

```
95-100 (Excellent)   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   8 (5.0%)
90-94 (Very Good)    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9 (5.6%)
85-89 (Good)         ███████████████░░░░░░░░░░░░░░░░░  31 (19.4%)
80-84 (Above Avg)    ████████████████████████░░░░░░░░  49 (30.6%) ← MODE
75-79 (Average)      ████████████████░░░░░░░░░░░░░░░░  33 (20.6%)
70-74 (Below Avg)    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9 (5.6%)
60-69 (Poor)         ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9 (5.6%)
<60 (Critical)       ██████░░░░░░░░░░░░░░░░░░░░░░░░░░  12 (7.5%)
```

**Statistics:** Min=28 | Max=100 | Median=81 | StdDev=11.2

### Roman Urdu (160 tests)

```
95-100 (Excellent)   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   8 (5.0%)
90-94 (Very Good)    ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   5 (3.1%)
85-89 (Good)         ███████████░░░░░░░░░░░░░░░░░░░░░  22 (13.8%)
80-84 (Above Avg)    ██████████████░░░░░░░░░░░░░░░░░░  28 (17.5%)
75-79 (Average)      ███████████████████████████████░  71 (44.4%) ← MODE
70-74 (Below Avg)    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2 (1.2%)
60-69 (Poor)         ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░   9 (5.6%)
<60 (Critical)       ███████░░░░░░░░░░░░░░░░░░░░░░░░░  15 (9.4%)
```

**Statistics:** Min=50 | Max=100 | Median=78 | StdDev=10.1

### Distribution Insights

| Observation | Urdu | Roman | Analysis |
|-------------|------|-------|----------|
| **Mode** | 80-84 (30.6%) | 75-79 (44.4%) | Roman clusters lower |
| **Excellent (≥90)** | 17 (10.6%) | 13 (8.1%) | Similar top performers |
| **Critical (<60)** | 12 (7.5%) | 15 (9.4%) | Roman has more failures |
| **Pass Rate (≥70)** | 86.9% | 84.4% | Nearly equal |

---

## ⏱️ Response Time Analysis

### Performance Metrics

| Metric | Urdu | Roman | Δ |
|--------|------|-------|---|
| **Average** | 40.3s | 50.7s | +10.4s |
| **Minimum** | 2.6s | 3.3s | +0.7s |
| **Maximum** | 149.2s | 189.9s | +40.7s |
| **Fast (<15s)** | 62 tests (39%) | 41 tests (26%) | -13% |
| **Slow (>60s)** | 35 tests (22%) | 49 tests (31%) | +9% |

### Slowest Tests

| Script | Test ID | Category | Time |
|--------|---------|----------|------|
| Urdu | urdu_conv_008 | conversation | 149s |
| Roman | roman_cs_017 | commonsense_reasoning | 190s |

### Time by Category (Fastest → Slowest)

**Urdu:** translation (8.1s) → mathematics (11.5s) → QA (20.8s) → reasoning (21.9s) → instruction (25.8s) → summarization (55.3s) → conversation (72.0s) → creative (106.6s)

**Roman:** translation (9.6s) → math (20.2s) → QA (20.4s) → instruction (37.2s) → summarization (42.5s) → conversation (73.8s) → commonsense (88.7s) → text_gen (112.8s)

---

## 🔤 Urdu Script Output Analysis

### Script Distribution

| Output Type | Urdu | Roman | Analysis |
|-------------|------|-------|----------|
| **Pure Urdu (>95%)** | 107 (67%) | 93 (58%) | Model prefers Urdu output |
| **Mixed (30-95%)** | 30 (19%) | 20 (12%) | Less mixing in Roman |
| **Mostly English (<30%)** | 23 (14%) | 47 (29%) | Roman prompts → more English |

### Key Insight
> When given Roman Urdu input, the model is **2x more likely** to respond in English (29% vs 14%). This suggests the model uses input script as a cue for output language.

---

## 🔑 Keyword Matching Analysis

### Match Rates

| Metric | Urdu | Roman | Analysis |
|--------|------|-------|----------|
| **Keywords Passed** | 288/565 (51.0%) | 254/915 (27.8%) | Roman has more keywords per test |
| **Perfect Match (all)** | 28 (17.5%) | 7 (4.4%) | Urdu tests better designed |
| **Zero Match (none)** | 18 (11.2%) | 26 (16.2%) | Roman has more complete misses |

### Keyword Design Issue (Round 3 Target)
Despite bilingual keywords, Roman Urdu still has:
- **27.8% keyword pass rate** (vs 51% for Urdu)
- **4.4% perfect matches** (vs 17.5% for Urdu)

**Root Cause:** Roman tests have more keywords per test on average, making perfect matches harder.

---

## ❌ Failure Pattern Analysis

### Urdu Script Failures: 21 tests (13.1%)

| Category | Count | % of Failures |
|----------|-------|---------------|
| Math/Reasoning | 10 | 48% |
| Instruction Following | 6 | 29% |
| Question Answering | 2 | 10% |
| Conversation | 2 | 10% |
| Other | 1 | 5% |

### Roman Urdu Failures: 24 tests (15.0%)

| Category | Count | % of Failures |
|----------|-------|---------------|
| Math/Reasoning | 16 | 67% |
| Instruction Following | 4 | 17% |
| Question Answering | 4 | 17% |
| Conversation | 3 | 12% |
| Other | 2 | 8% |

### Critical Finding
> **Math/Reasoning accounts for 48-67% of all failures.** This is the model's primary weakness.

---

## 🔴 Critical Failures (<60 score)

### Urdu Script: 12 critical failures

| Test ID | Score | Category | Issue |
|---------|-------|----------|-------|
| urdu_inst_012 | 28 | instruction_following | Said "true" when answer was "false" |
| urdu_math_004 | 35 | mathematics | 100÷5=10 (wrong: should be 20) |
| urdu_math_002 | 45 | mathematics | 12-7=-18 (wrong: should be 5) |
| urdu_inst_001 | 47 | instruction_following | Moon generates own light (wrong) |
| urdu_qa_020 | 55 | question_answering | Said Nanga Parbat (wrong: K2) |
| urdu_reason_007 | 55 | reasoning | Wrong odd-one-out |
| urdu_reason_011 | 55 | reasoning | Wall problem: 18 (wrong: 12) |
| urdu_reason_015 | 55 | reasoning | Sequence: 18 (wrong: 30) |
| urdu_conv_018 | 55 | conversation | Off-topic response |
| urdu_conv_019 | 55 | conversation | Generic farewell |
| urdu_inst_019 | 55 | instruction_following | Missing keywords |
| urdu_math_006 | 58 | mathematics | 15-7=8 but missing Urdu "آٹھ" |

### Roman Urdu: 15 critical failures

| Test ID | Score | Category | Issue |
|---------|-------|----------|-------|
| roman_math_014 | 50 | mathematical_reasoning | 3^4=16 (wrong: should be 81) |
| roman_qa_016 | 55 | question_answering | Speed of light - missing keywords |
| roman_math_004 | 55 | mathematical_reasoning | Distance=0.03km (wrong: 270km) |
| roman_math_011 | 55 | mathematical_reasoning | Chairs=10 (wrong: 20) |
| roman_cs_001 | 55 | commonsense_reasoning | Rain - missed "umbrella" |
| roman_cs_002 | 55 | commonsense_reasoning | Fever - missed "doctor" |
| roman_cs_009 | 55 | commonsense_reasoning | Heavy lifting - missed keywords |
| roman_cs_010 | 55 | commonsense_reasoning | Bad food - missed "sick" |
| roman_cs_016 | 55 | commonsense_reasoning | Help - missed "thanks" |
| roman_cs_020 | 55 | commonsense_reasoning | Friend angry - missed keywords |
| roman_inst_001 | 55 | instruction_following | Moon makes light (wrong) |
| roman_inst_008 | 55 | instruction_following | "Suraj" as singer name |
| roman_conv_008 | 55 | conversation | "Bore" misunderstood |
| roman_conv_009 | 55 | conversation | Weekend - off-topic |
| roman_conv_011 | 55 | conversation | Sleep question - confused |

---

## 🏆 Top Performers (≥90 score)

### Urdu Script: 17 excellent tests

| Test ID | Score | Category |
|---------|-------|----------|
| urdu_trans_001 | 100 | translation |
| urdu_trans_007 | 100 | translation |
| urdu_trans_012 | 100 | translation |
| urdu_trans_017 | 97 | translation |
| urdu_trans_005 | 95 | translation |

### Roman Urdu: 13 excellent tests

| Test ID | Score | Category |
|---------|-------|----------|
| roman_inst_006 | 100 | instruction_following |
| roman_trans_001 | 100 | translation |
| roman_trans_012 | 100 | translation |
| roman_trans_007 | 97 | translation |
| roman_trans_009 | 97 | translation |

### Observation
> **Translation dominates top performers** with 10/17 Urdu and 4/13 Roman top scores being translation tasks.

---

## 🔍 Deep Dive: Failure Pattern Analysis

### Category 1: Mathematical Errors (Critical)
**Frequency:** 8 tests | **Avg Score:** 52 | **Impact:** High

| Error | Expected | Got | Error Type |
|-------|----------|-----|------------|
| 100 ÷ 5 | 20 | 10 | Division error |
| 12 - 7 | 5 | -18 | Sign confusion |
| 3^4 | 81 | 16 | Exponent error (3×4 instead of 3⁴) |
| 90 × 3 | 270 | ~0.03 | Formula inversion |
| 5 workers problem | 20 | 10 | Logic error |
| 15 - 7 | 8 | 8 ✓ | Correct but missing Urdu word |

**Root Causes:**
1. **Arithmetic confusion** - Basic operations calculated incorrectly
2. **Exponent misinterpretation** - Treats 3^4 as 3×4
3. **Word problem parsing** - Misreads problem structure

### Category 2: Factual Errors (Major)
**Frequency:** 5 tests | **Avg Score:** 55 | **Impact:** Medium

| Question | Expected | Got | Type |
|----------|----------|-----|------|
| Pakistan's highest peak | K2 | Nanga Parbat | Knowledge error |
| Moon's light source | Reflected | Self-generated | Science error |
| Sun rises from | East | All directions | Question misread |
| Human bones | 206 | Avoided answer | Evasion |
| Urdu official status | 1947-49 | 1956 | Historical error |

**Root Cause:** Training data gaps or retrieval errors

### Category 3: Instruction Misinterpretation (Major)
**Frequency:** 7 tests | **Avg Score:** 54 | **Impact:** Medium

| Issue | Example | Root Cause |
|-------|---------|------------|
| Yes/No confusion | Said "ہاں" when answer was "نہیں" | Binary logic failure |
| Format ignored | Asked for 3 words, gave paragraph | Instruction not followed |
| Context confusion | "Suraj" (sun) interpreted as singer name | Homograph ambiguity |
| "Bore" misinterpreted | Gave mechanical advice | Roman Urdu ambiguity |

### Category 4: Commonsense Gaps (Roman Only)
**Frequency:** 6 tests | **Avg Score:** 55 | **Impact:** Medium

All 6 failures were in `commonsense_reasoning`:
- Rain → didn't mention umbrella
- Fever → didn't mention doctor
- Heavy lifting → missed ergonomic keywords
- Bad food → missed sickness keywords
- Helping → missed "thank you"
- Friend angry → missed reconciliation keywords

**Root Cause:** Model provides contextual responses but misses expected keywords

### Category 5: Keyword Near-Misses (Minor - Fixable)
**Frequency:** 12 tests | **Avg Score:** 62 | **Impact:** Low

These tests had **correct answers** but keywords didn't match:
- Used "اعمال" instead of "عمل"
- Said "آٹھ" but keyword only had "8" and "eight"
- Answered "سات" but keyword expected "7"

**Fix for Round 3:** Expand keyword synonyms

---

## 📈 Round 1 vs Round 2 Comparison

### Score Improvements

```
                Round 1    Round 2    Change
Urdu Script     ████████   ████████   +0.5 (78.5 → 79.0)
Roman Urdu      ███████░   ████████   +7.2 (70.4 → 77.6)
Combined        ███████░   ████████   +3.9 (74.4 → 78.3)
```

### What Improved

| Aspect | R1 Issue | R2 Fix | Impact |
|--------|----------|--------|--------|
| **Keyword Design** | Roman-only keywords | Bilingual keywords | +7.2 pts Roman |
| **Test Balance** | 140 vs 160 | 160 vs 160 | Fair comparison |
| **Category Coverage** | Uneven | 8×20 uniform | Consistent |
| **Script Detection** | ~31.7% failures | ~0% | Accurate scoring |

### What Stayed Same

- Model performance on Urdu script (+0.5 within margin)
- Overall response quality
- Translation as top category
- Math/reasoning as weakest areas

---

## 🎯 Model Capability Matrix

### Strengths (Score ≥80)

| Capability | Urdu | Roman | Evidence |
|------------|------|-------|----------|
| **Translation** | 89.4 | 85.9 | Highest both scripts |
| **Summarization** | 83.9 | 79.7 | 100% pass rate |
| **Creative Writing** | 80.1 | 77.7 | Consistent quality |
| **Urdu Script Generation** | 67% pure | 58% pure | Strong preference |

### Weaknesses (Score <75)

| Weakness | Urdu | Roman | Evidence |
|----------|------|-------|----------|
| **Mathematics** | 72.4 | 76.2 | Calculation errors |
| **Reasoning** | 73.2 | 70.4 | Logic gaps |
| **Yes/No Instructions** | 75.5 | 78.3 | Binary confusion |
| **Commonsense** | N/A | 70.4 | Keyword misses |

---

## 📋 Recommendations for Round 3

### Test Improvements (Priority Order)

| # | Action | Target | Expected Impact |
|---|--------|--------|-----------------|
| 1 | **Expand keyword lists** | 12 near-miss tests | +3-5 pts combined |
| 2 | **Simplify math tests** | Focus single-step | Better accuracy measure |
| 3 | **Add keyword synonyms** | All tests | Higher keyword match |
| 4 | **Clarify ambiguous prompts** | 7 instruction tests | Reduce misinterpretation |

### Model Fine-tuning Targets

| Priority | Area | Current | Target | Method |
|----------|------|---------|--------|--------|
| **P1** | Mathematical reasoning | 72-76 | 85+ | Add math training data |
| **P2** | Yes/No instructions | 75-78 | 90+ | Binary response training |
| **P3** | Commonsense reasoning | 70.4 | 80+ | Common knowledge QA |
| **P4** | Factual accuracy | 55-60 | 80+ | Knowledge base update |

---

## 📊 Performance Metrics Summary

### Response Time

| Script | Avg | Min | Max | Fast (<15s) | Slow (>60s) |
|--------|-----|-----|-----|-------------|-------------|
| Urdu | 40.3s | 2.6s | 149.2s | 62 (39%) | 35 (22%) |
| Roman | 50.7s | 3.3s | 189.9s | 41 (26%) | 49 (31%) |

### Throughput

| Script | Avg TPS | Urdu Output % |
|--------|---------|---------------|
| Urdu | 0.76 | 77% |
| Roman | 0.69 | 66% |

---

## ✅ Conclusion

Round 2 successfully validated our hypothesis that **test design issues in Round 1 were causing score deflation**, particularly for Roman Urdu inputs. The +7.2 point improvement in Roman Urdu scores (70.4 → 77.6) confirms the model handles both scripts similarly when evaluation is fair.

### True Model Performance
- **Combined Score:** 78.3/100 (previously underreported at 74.4)
- **Script Parity:** 1.4-point gap (previously 8.1 points)
- **Consistency:** Both scripts within 2% of each other

### Remaining Issues (Model-Level)
| Issue | Severity | Tests Affected |
|-------|----------|----------------|
| Mathematical reasoning | High | 8-10 |
| Factual knowledge gaps | Medium | 5 |
| Instruction following | Medium | 7 |
| Commonsense reasoning | Medium | 6 |

### Next Steps
1. ~~Test design fixes~~ ✅ Complete
2. **Round 3:** Expand keywords for 12 near-miss tests
3. **Model tuning:** Focus on math/reasoning capabilities
4. Consider separate math-focused evaluation benchmark

---

## 📎 Appendix: Test Files

| File | Tests | Categories | Version |
|------|-------|------------|---------|
| `urdu_script_tests_round2.json` | 160 | 8 | 2.0.0 |
| `roman_urdu_tests_round2.json` | 160 | 8 | 2.0.0 |
| `combined_results.json` | 320 | - | - |

---

*Generated: February 3, 2026*  
*Framework: Qalb Urdu AI Testing Framework v2.0*  
*Total Runtime: 4h 2m 29s*  
*Tests: 320 (160 Urdu + 160 Roman)*
