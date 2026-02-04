#!/usr/bin/env python3
"""Analyze Round 4 test results by category."""

import json
from collections import defaultdict
from pathlib import Path

def analyze_results():
    results_file = Path("data/baseline/combined_results.json")
    
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n" + "="*70)
    print("ROUND 4 DETAILED ANALYSIS")
    print("="*70)
    
    all_categories = defaultdict(list)
    
    # Analyze by category for each test suite
    for suite in data['test_suites']:
        print(f"\n{'='*70}")
        print(f"Test Suite: {suite['test_file']}")
        print(f"Average Score: {suite['metrics']['average_score']:.1f}/100")
        print(f"Avg Response Time: {suite['metrics']['average_response_time_ms']:.0f}ms")
        print(f"{'='*70}")
        
        categories = defaultdict(list)
        for result in suite['results']:
            categories[result['category']].append({
                'score': result['score'],
                'test_id': result['test_id'],
                'passed': result['passed_keywords'],
                'failed': result['failed_keywords'],
                'prompt': result['prompt'],
                'response': result['response'][:200] if len(result['response']) > 200 else result['response']
            })
            all_categories[result['category']].append(result['score'])
        
        print(f"\n{'Category':<30} {'Tests':<8} {'Avg':<10} {'Min':<8} {'Max':<8}")
        print("-"*70)
        for cat, results in sorted(categories.items()):
            scores = [r['score'] for r in results]
            avg = sum(scores)/len(scores)
            print(f"{cat:<30} {len(scores):<8} {avg:<10.1f} {min(scores):<8.1f} {max(scores):<8.1f}")
        
        # Show examples of lowest scoring tests
        print(f"\n--- Lowest Scoring Tests (< 60) ---")
        low_scores = []
        for cat, results in categories.items():
            for r in results:
                if r['score'] < 60:
                    low_scores.append((cat, r))
        
        low_scores.sort(key=lambda x: x[1]['score'])
        for cat, r in low_scores[:5]:
            print(f"\n  {r['test_id']} ({cat}): {r['score']:.0f}/100")
            print(f"    Prompt: {r['prompt'][:80]}...")
            print(f"    Failed keywords: {r['failed']}")
    
    # Overall category comparison
    print(f"\n{'='*70}")
    print("COMBINED CATEGORY ANALYSIS (Both Urdu + Roman)")
    print(f"{'='*70}")
    print(f"\n{'Category':<30} {'Tests':<8} {'Avg':<10} {'Min':<8} {'Max':<8}")
    print("-"*70)
    for cat, scores in sorted(all_categories.items()):
        avg = sum(scores)/len(scores)
        print(f"{cat:<30} {len(scores):<8} {avg:<10.1f} {min(scores):<8.1f} {max(scores):<8.1f}")
    
    print(f"\n{'='*70}")
    print(f"OVERALL SCORE: {data['overall_metrics']['average_score']:.1f}/100")
    print(f"Total Tests: {data['overall_metrics']['total_tests']}")
    print(f"Successful: {data['overall_metrics']['successful_tests']}")
    print(f"{'='*70}")
    
    # Compare with previous rounds
    print("\n" + "="*70)
    print("ROUND COMPARISON")
    print("="*70)
    print(f"\n{'Round':<12} {'Urdu':<12} {'Roman':<12} {'Combined':<12} {'Change':<12}")
    print("-"*60)
    print(f"{'Round 1':<12} {'74.4':<12} {'74.5':<12} {'74.4':<12} {'-':<12}")
    print(f"{'Round 2':<12} {'78.3':<12} {'78.2':<12} {'78.3':<12} {'+3.9':<12}")
    print(f"{'Round 3':<12} {'80.0':<12} {'78.4':<12} {'79.2':<12} {'+0.9':<12}")
    
    urdu_score = data['test_suites'][0]['metrics']['average_score']
    roman_score = data['test_suites'][1]['metrics']['average_score']
    combined = data['overall_metrics']['average_score']
    change = combined - 79.2
    print(f"{'Round 4':<12} {urdu_score:<12.1f} {roman_score:<12.1f} {combined:<12.1f} {change:+.1f}")

if __name__ == "__main__":
    analyze_results()
