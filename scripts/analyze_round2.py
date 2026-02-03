"""Round 2 Analysis Script"""
import json
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

urdu = json.load(open('data/baseline/urdu_script/urdu_script_tests_round2_results.json', 'r', encoding='utf-8'))
roman = json.load(open('data/baseline/roman_urdu/roman_urdu_tests_round2_results.json', 'r', encoding='utf-8'))

# Comprehensive Analysis
print("=" * 70)
print("QALB MODEL - ROUND 2 DEEP ANALYSIS")
print("=" * 70)

# 1. Category breakdown
def category_stats(results, name):
    cats = defaultdict(lambda: {'scores': [], 'times': [], 'urdu': [], 'tps': []})
    for r in results['results']:
        cats[r['category']]['scores'].append(r['score'])
        cats[r['category']]['times'].append(r['response_time_ms'])
        cats[r['category']]['urdu'].append(r['urdu_char_ratio'])
        cats[r['category']]['tps'].append(r['tokens_per_second'])
    
    print(f"\n{'='*70}")
    print(f"{name} - CATEGORY BREAKDOWN")
    print(f"{'='*70}")
    print(f"{'Category':<25} {'Score':>8} {'Time':>10} {'Urdu%':>8} {'TPS':>8} {'Pass%':>8}")
    print("-" * 70)
    
    all_scores = []
    for cat, d in sorted(cats.items(), key=lambda x: -sum(x[1]['scores'])/len(x[1]['scores'])):
        avg_score = sum(d['scores'])/len(d['scores'])
        avg_time = sum(d['times'])/len(d['times'])/1000
        avg_urdu = sum(d['urdu'])/len(d['urdu'])*100
        avg_tps = sum(d['tps'])/len(d['tps'])
        pass_rate = len([s for s in d['scores'] if s >= 70])/len(d['scores'])*100
        all_scores.extend(d['scores'])
        print(f"{cat:<25} {avg_score:>7.1f} {avg_time:>9.1f}s {avg_urdu:>7.0f}% {avg_tps:>7.2f} {pass_rate:>7.0f}%")
    
    return cats, all_scores

urdu_cats, urdu_scores = category_stats(urdu, "URDU SCRIPT")
roman_cats, roman_scores = category_stats(roman, "ROMAN URDU")

# 2. Score distribution analysis
print(f"\n{'='*70}")
print("SCORE DISTRIBUTION ANALYSIS")
print("=" * 70)

def dist_analysis(scores, name):
    ranges = {
        '95-100 (Excellent)': len([s for s in scores if s >= 95]),
        '90-94 (Very Good)': len([s for s in scores if 90 <= s < 95]),
        '85-89 (Good)': len([s for s in scores if 85 <= s < 90]),
        '80-84 (Above Avg)': len([s for s in scores if 80 <= s < 85]),
        '75-79 (Average)': len([s for s in scores if 75 <= s < 80]),
        '70-74 (Below Avg)': len([s for s in scores if 70 <= s < 75]),
        '60-69 (Poor)': len([s for s in scores if 60 <= s < 70]),
        '<60 (Critical)': len([s for s in scores if s < 60])
    }
    print(f"\n{name}:")
    for r, c in ranges.items():
        bar = '█' * int(c/2) + '░' * (40 - int(c/2))
        print(f"  {r:<20} {bar} {c:>3} ({c/len(scores)*100:.1f}%)")
    
    # Statistics
    sorted_scores = sorted(scores)
    median = sorted_scores[len(sorted_scores)//2]
    std_dev = (sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)) ** 0.5
    print(f"\n  Stats: Min={min(scores):.0f} | Max={max(scores):.0f} | Median={median:.0f} | StdDev={std_dev:.1f}")

dist_analysis(urdu_scores, "URDU SCRIPT")
dist_analysis(roman_scores, "ROMAN URDU")

# 3. Response time analysis
print(f"\n{'='*70}")
print("RESPONSE TIME ANALYSIS")
print("=" * 70)

for name, data in [("URDU", urdu), ("ROMAN", roman)]:
    times = [r['response_time_ms']/1000 for r in data['results']]
    fast = [r for r in data['results'] if r['response_time_ms'] < 15000]
    slow = [r for r in data['results'] if r['response_time_ms'] > 60000]
    print(f"\n{name}:")
    print(f"  Average: {sum(times)/len(times):.1f}s | Min: {min(times):.1f}s | Max: {max(times):.1f}s")
    print(f"  Fast (<15s): {len(fast)} tests | Slow (>60s): {len(slow)} tests")
    if slow:
        print(f"  Slowest: {sorted(slow, key=lambda x: -x['response_time_ms'])[0]['test_id']} ({sorted(slow, key=lambda x: -x['response_time_ms'])[0]['response_time_ms']/1000:.0f}s)")

# 4. Urdu Script Ratio Analysis
print(f"\n{'='*70}")
print("URDU SCRIPT OUTPUT ANALYSIS")
print("=" * 70)

for name, data in [("URDU", urdu), ("ROMAN", roman)]:
    ratios = [r['urdu_char_ratio'] for r in data['results']]
    full_urdu = len([r for r in ratios if r >= 0.95])
    mixed = len([r for r in ratios if 0.3 <= r < 0.95])
    english = len([r for r in ratios if r < 0.3])
    print(f"\n{name} Script Output:")
    print(f"  Pure Urdu (>95%): {full_urdu} tests ({full_urdu/len(ratios)*100:.0f}%)")
    print(f"  Mixed (30-95%): {mixed} tests ({mixed/len(ratios)*100:.0f}%)")
    print(f"  Mostly English (<30%): {english} tests ({english/len(ratios)*100:.0f}%)")

# 5. Keyword Analysis
print(f"\n{'='*70}")
print("KEYWORD MATCHING ANALYSIS")
print("=" * 70)

for name, data in [("URDU", urdu), ("ROMAN", roman)]:
    total_passed = sum(len(r['passed_keywords']) for r in data['results'])
    total_failed = sum(len(r['failed_keywords']) for r in data['results'])
    total = total_passed + total_failed
    perfect = len([r for r in data['results'] if len(r['failed_keywords']) == 0])
    zero_match = len([r for r in data['results'] if len(r['passed_keywords']) == 0])
    
    print(f"\n{name}:")
    print(f"  Keywords Passed: {total_passed}/{total} ({total_passed/total*100:.1f}%)")
    print(f"  Perfect Match (all keywords): {perfect} tests ({perfect/len(data['results'])*100:.1f}%)")
    print(f"  Zero Match (no keywords): {zero_match} tests ({zero_match/len(data['results'])*100:.1f}%)")

# 6. Error Pattern Analysis
print(f"\n{'='*70}")
print("FAILURE PATTERN ANALYSIS")
print("=" * 70)

def analyze_failures(data, name):
    failures = [r for r in data['results'] if r['score'] < 70]
    
    # Categorize failures
    math_fail = [r for r in failures if 'math' in r['category']]
    inst_fail = [r for r in failures if 'instruction' in r['category']]
    reason_fail = [r for r in failures if 'reason' in r['category']]
    qa_fail = [r for r in failures if 'question' in r['category']]
    conv_fail = [r for r in failures if 'conversation' in r['category']]
    other_fail = [r for r in failures if r not in math_fail + inst_fail + reason_fail + qa_fail + conv_fail]
    
    print(f"\n{name} - {len(failures)} failures:")
    print(f"  Math/Reasoning: {len(math_fail + reason_fail)} ({len(math_fail + reason_fail)/max(len(failures),1)*100:.0f}%)")
    print(f"  Instruction Following: {len(inst_fail)} ({len(inst_fail)/max(len(failures),1)*100:.0f}%)")
    print(f"  Question Answering: {len(qa_fail)} ({len(qa_fail)/max(len(failures),1)*100:.0f}%)")
    print(f"  Conversation: {len(conv_fail)} ({len(conv_fail)/max(len(failures),1)*100:.0f}%)")
    print(f"  Other: {len(other_fail)} ({len(other_fail)/max(len(failures),1)*100:.0f}%)")

analyze_failures(urdu, "URDU SCRIPT")
analyze_failures(roman, "ROMAN URDU")

# 7. Detailed Low Scores
print(f"\n{'='*70}")
print("CRITICAL FAILURES (<60)")
print("=" * 70)

for name, data in [("URDU", urdu), ("ROMAN", roman)]:
    critical = sorted([r for r in data['results'] if r['score'] < 60], key=lambda x: x['score'])
    print(f"\n{name} ({len(critical)} critical):")
    for r in critical[:10]:
        print(f"  {r['test_id']}: {r['score']:.0f}/100 - {r['category']}")

# 8. Top Performers
print(f"\n{'='*70}")
print("TOP PERFORMERS (>90)")
print("=" * 70)

for name, data in [("URDU", urdu), ("ROMAN", roman)]:
    top = sorted([r for r in data['results'] if r['score'] >= 90], key=lambda x: -x['score'])
    print(f"\n{name} ({len(top)} excellent):")
    for r in top[:5]:
        print(f"  {r['test_id']}: {r['score']:.0f}/100 - {r['category']}")
