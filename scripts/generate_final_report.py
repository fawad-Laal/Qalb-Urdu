#!/usr/bin/env python3
"""
Comprehensive Report Generator for Qalb Urdu AI Evaluation
Uses OpenAI GPT-5-mini to analyze all test results and generate a detailed report.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_DIR = PROJECT_ROOT / "data" / "baseline"
REPORTS_DIR = PROJECT_ROOT / "reports"

def read_markdown_files():
    """Read all analysis markdown files."""
    md_files = {}
    
    files_to_read = [
        "ROUND_2_ANALYSIS.md",
        "ROUND_3_ANALYSIS.md", 
        "ROUND_4_ANALYSIS.md",
        "PROGRESS.md"
    ]
    
    for filename in files_to_read:
        filepath = DOCS_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                md_files[filename] = f.read()
                print(f"✅ Loaded {filename}")
        else:
            print(f"⚠️ {filename} not found")
    
    return md_files

def read_test_results():
    """Read combined test results JSON."""
    results_file = DATA_DIR / "combined_results.json"
    
    if results_file.exists():
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Loaded test results: {data['overall_metrics']['total_tests']} tests")
            return data
    else:
        print("⚠️ combined_results.json not found")
        return None

def extract_category_examples(results_data, num_examples=3):
    """Extract example tests from each category for the report."""
    examples = {}
    
    for suite in results_data.get('test_suites', []):
        script_type = "Urdu" if "urdu_script" in suite['test_file'] else "Roman"
        
        # Group by category
        categories = {}
        for result in suite['results']:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        # Get best and worst examples from each category
        for cat, tests in categories.items():
            key = f"{script_type}_{cat}"
            sorted_tests = sorted(tests, key=lambda x: x['score'], reverse=True)
            
            examples[key] = {
                'best': sorted_tests[:num_examples],
                'worst': sorted_tests[-num_examples:],
                'avg_score': sum(t['score'] for t in tests) / len(tests)
            }
    
    return examples

def generate_section_with_gpt(section_name, context, prompt):
    """Generate a report section using GPT-5 mini."""
    
    system_prompt = """You are an expert technical writer creating a comprehensive evaluation report for an Urdu language AI model called Qalb. 
    
Write in a professional, academic style suitable for publication. Include:
- Clear explanations of methodology and findings
- Specific examples with Urdu/Roman text where relevant
- Data-driven insights with percentages and scores
- Limitations and recommendations

Format using proper markdown with headers, tables, and bullet points."""

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Section: {section_name}\n\nContext:\n{context}\n\nTask:\n{prompt}"}
            ],
            max_completion_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generating {section_name}: {e}")
        return f"[Error generating section: {e}]"

def generate_comprehensive_report(md_files, results_data, examples):
    """Generate the complete report using GPT-5-mini for each section."""
    
    report_sections = []
    
    # Title Page
    report_sections.append("""
# Qalb Urdu AI Model Evaluation Report
## Comprehensive Assessment of enstazao/qalb:8b-instruct-fp16

**Prepared by:** Qalb Evaluation Framework  
**Date:** February 4, 2026  
**Version:** Final Report v1.0

---

**Model Under Evaluation:** enstazao/qalb:8b-instruct-fp16  
**Total Tests Conducted:** 320 (160 Urdu Script + 160 Roman Urdu)  
**Testing Rounds:** 4 iterative rounds  
**Final Score:** 77.7/100  
**Peak Score:** 79.2/100 (Round 3)

---
""")

    print("\n📝 Generating report sections with GPT-5-mini...\n")
    
    # Section 1: Executive Summary
    print("1️⃣ Generating Executive Summary...")
    exec_summary_context = f"""
Round scores:
- Round 1: 74.4/100 (baseline)
- Round 2: 78.3/100 (+3.9, bilingual keywords)
- Round 3: 79.2/100 (+0.9, math clarity fixes)
- Round 4: 77.7/100 (-1.5, keyword expansion backfired)

Key findings from PROGRESS.md:
{md_files.get('PROGRESS.md', '')[:3000]}
"""
    exec_summary = generate_section_with_gpt(
        "Executive Summary",
        exec_summary_context,
        "Write a comprehensive executive summary (500-700 words) covering the evaluation objectives, methodology overview, key findings, and recommendations. Include the score progression and explain why Round 4 showed a decrease."
    )
    report_sections.append(f"## Chapter 1: Executive Summary\n\n{exec_summary}\n\n---\n")

    # Section 2: Methodology
    print("2️⃣ Generating Methodology Chapter...")
    methodology_context = f"""
Test Framework Details:
- 320 total tests across 8 categories
- Categories: Question Answering, Mathematics, Reasoning, Translation, Summarization, Creative Writing, Conversation, Instruction Following
- Scoring formula: score = 50 + (50 × passed_keywords / total_keywords)
- Keyword matching approach with bilingual support

From Round 2 Analysis:
{md_files.get('ROUND_2_ANALYSIS.md', '')[:2500]}
"""
    methodology = generate_section_with_gpt(
        "Methodology",
        methodology_context,
        "Write a detailed methodology chapter (600-800 words) explaining the test framework design, category selection rationale, scoring algorithm, and iterative improvement approach. Discuss the strengths and limitations of keyword-based evaluation."
    )
    report_sections.append(f"## Chapter 2: Evaluation Methodology\n\n{methodology}\n\n---\n")

    # Section 3: Round-by-Round Analysis
    print("3️⃣ Generating Round Analysis Chapter...")
    rounds_context = f"""
Round 2 Analysis:
{md_files.get('ROUND_2_ANALYSIS.md', '')[:2000]}

Round 3 Analysis:
{md_files.get('ROUND_3_ANALYSIS.md', '')[:2000]}

Round 4 Analysis:
{md_files.get('ROUND_4_ANALYSIS.md', '')[:2000]}
"""
    rounds_analysis = generate_section_with_gpt(
        "Round Analysis",
        rounds_context,
        "Write a comprehensive round-by-round analysis chapter (800-1000 words) detailing what changed in each round, the impact on scores, and lessons learned. Include specific examples of tests that improved or declined."
    )
    report_sections.append(f"## Chapter 3: Round-by-Round Analysis\n\n{rounds_analysis}\n\n---\n")

    # Section 4: Category Performance
    print("4️⃣ Generating Category Performance Chapter...")
    
    # Build category summary
    category_summary = "Category Performance Summary:\n\n"
    for key, data in examples.items():
        category_summary += f"- {key}: {data['avg_score']:.1f}/100\n"
        if data['best']:
            best = data['best'][0]
            category_summary += f"  Best: {best['test_id']} ({best['score']:.0f}/100)\n"
        if data['worst']:
            worst = data['worst'][-1]
            category_summary += f"  Worst: {worst['test_id']} ({worst['score']:.0f}/100)\n"
    
    category_analysis = generate_section_with_gpt(
        "Category Performance",
        category_summary,
        "Write a detailed category performance chapter (700-900 words) analyzing each test category's results. Identify the strongest and weakest categories, explain why certain categories performed better, and provide insights into the model's capabilities."
    )
    report_sections.append(f"## Chapter 4: Category Performance Analysis\n\n{category_analysis}\n\n---\n")

    # Section 5: Translation Tests Deep Dive
    print("5️⃣ Generating Translation Analysis...")
    trans_examples = {k: v for k, v in examples.items() if 'translation' in k.lower()}
    trans_context = f"""
Translation Test Performance:
{json.dumps({k: {'avg': v['avg_score'], 'best_score': v['best'][0]['score'] if v['best'] else 0, 'worst_score': v['worst'][-1]['score'] if v['worst'] else 0} for k, v in trans_examples.items()}, indent=2)}

Example translation tests:
- "Hello, how are you?" → Expected: ہیلو، سلام، کیسے، خیریت
- "Knowledge is power" → Expected: علم، طاقت
- Proverbs and idioms translation challenges
"""
    translation_section = generate_section_with_gpt(
        "Translation Tests",
        trans_context,
        "Write a detailed analysis of translation performance (500-600 words). Discuss English-to-Urdu vs Urdu-to-English performance, proverb/idiom challenges, and the impact of synonym expansion in Round 4."
    )
    report_sections.append(f"## Chapter 5: Translation Capability Assessment\n\n{translation_section}\n\n---\n")

    # Section 6: Reasoning & Mathematics
    print("6️⃣ Generating Reasoning & Math Analysis...")
    reason_math_context = f"""
Reasoning Performance (lowest category):
- Urdu reasoning: 67.6/100
- Roman commonsense: 72.0/100

Critical failures:
- Prime number recognition (model answered 11 instead of 9)
- Pattern sequences (2,6,12,20,___ model said 24 not 30)
- Work-rate problems (6 workers × 6 days = 36 walls, not 12)

From Round 4 Analysis:
{md_files.get('ROUND_4_ANALYSIS.md', '')[-2000:]}
"""
    reasoning_section = generate_section_with_gpt(
        "Reasoning Analysis",
        reason_math_context,
        "Write a detailed analysis of reasoning and mathematical performance (600-700 words). Identify specific failure patterns, discuss whether these are keyword issues or genuine reasoning limitations, and suggest improvements."
    )
    report_sections.append(f"## Chapter 6: Reasoning & Mathematical Capabilities\n\n{reasoning_section}\n\n---\n")

    # Section 7: Limitations & Recommendations
    print("7️⃣ Generating Limitations & Recommendations...")
    limitations_context = f"""
Key Limitations Identified:
1. Keyword dilution effect - more keywords can decrease scores
2. Numeric vs word format (model outputs "10" not "دس")
3. Semantic equivalence not captured by keyword matching
4. Reasoning failures are logic issues, not vocabulary
5. Test ambiguity (e.g., "bahar" = outside or spring)

From analysis documents:
{md_files.get('ROUND_4_ANALYSIS.md', '')[-1500:]}
"""
    limitations_section = generate_section_with_gpt(
        "Limitations & Recommendations",
        limitations_context,
        "Write comprehensive limitations and recommendations chapter (600-800 words). Cover framework limitations, model limitations, and provide specific actionable recommendations for future evaluation and model improvement."
    )
    report_sections.append(f"## Chapter 7: Limitations & Recommendations\n\n{limitations_section}\n\n---\n")

    # Section 8: Conclusion
    print("8️⃣ Generating Conclusion...")
    conclusion_context = f"""
Final Results:
- Peak: 79.2/100 (Round 3)
- Final: 77.7/100 (Round 4)
- Net improvement from baseline: +3.3 points

Key Achievements:
- Established bilingual evaluation framework
- Identified scoring formula limitations
- Documented model strengths (translation, summarization) and weaknesses (reasoning)
"""
    conclusion = generate_section_with_gpt(
        "Conclusion",
        conclusion_context,
        "Write a compelling conclusion (400-500 words) summarizing the evaluation journey, key findings about the Qalb model's Urdu language capabilities, and the significance of this work for Urdu NLP research."
    )
    report_sections.append(f"## Chapter 8: Conclusion\n\n{conclusion}\n\n---\n")

    # Appendix
    print("9️⃣ Adding Appendices...")
    appendix = """
## Appendix A: Test Categories and Counts

| Category | Urdu Script | Roman Urdu | Total |
|----------|-------------|------------|-------|
| Question Answering | 20 | 20 | 40 |
| Mathematics/Math Reasoning | 20 | 20 | 40 |
| Reasoning/Commonsense | 20 | 20 | 40 |
| Translation | 20 | 20 | 40 |
| Summarization | 20 | 20 | 40 |
| Creative Writing/Text Gen | 20 | 20 | 40 |
| Conversation | 20 | 20 | 40 |
| Instruction Following | 20 | 20 | 40 |
| **Total** | **160** | **160** | **320** |

## Appendix B: Score Evolution

| Round | Urdu | Roman | Combined | Change |
|-------|------|-------|----------|--------|
| 1 | 74.4 | 74.5 | 74.4 | — |
| 2 | 78.3 | 78.2 | 78.3 | +3.9 |
| 3 | 80.0 | 78.4 | 79.2 | +0.9 |
| 4 | 78.0 | 77.4 | 77.7 | -1.5 |

## Appendix C: Technical Specifications

- **Model:** enstazao/qalb:8b-instruct-fp16
- **Ollama Version:** 0.15.4
- **Hardware:** Windows 11, 32-core CPU, 31.7 GB RAM
- **Test Duration:** ~4-6 hours per round (CPU inference)
- **Python Version:** 3.12.10

## Appendix D: Repository

All test files, results, and analysis documents are available at:
https://github.com/fawad-Laal/Qalb-Urdu

---

*Report generated on February 4, 2026 using GPT-5-mini for analysis synthesis.*
"""
    report_sections.append(appendix)
    
    return "\n".join(report_sections)

def main():
    """Main entry point."""
    print("="*60)
    print("QALB URDU AI - COMPREHENSIVE REPORT GENERATOR")
    print("="*60)
    
    # Load all data
    print("\n📂 Loading data files...")
    md_files = read_markdown_files()
    results_data = read_test_results()
    
    if not results_data:
        print("❌ Cannot generate report without test results")
        return
    
    # Extract examples
    print("\n🔍 Extracting test examples...")
    examples = extract_category_examples(results_data)
    print(f"   Found {len(examples)} category groups")
    
    # Generate report
    print("\n" + "="*60)
    print("\n📝 Generating report sections with GPT-5-mini...\n")
    report = generate_comprehensive_report(md_files, results_data, examples)
    
    # Save report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as Markdown
    md_file = REPORTS_DIR / f"FINAL_EVALUATION_REPORT_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✅ Report saved: {md_file}")
    
    # Also save a latest version
    latest_file = REPORTS_DIR / "FINAL_EVALUATION_REPORT.md"
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ Latest version: {latest_file}")
    
    print("\n" + "="*60)
    print("REPORT GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
