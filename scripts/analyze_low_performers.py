#!/usr/bin/env python3
"""Detailed translation and reasoning analysis for Round 4."""

import json
from pathlib import Path

def analyze_low_performers():
    with open("data/baseline/combined_results.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*70)
    print("TRANSLATION TEST ANALYSIS (Round 4)")
    print("="*70)
    
    for suite in data['test_suites']:
        print(f"\n{suite['test_file']}:")
        trans_tests = [r for r in suite['results'] if r['category'] == 'translation']
        
        scores = [t['score'] for t in trans_tests]
        print(f"  Average: {sum(scores)/len(scores):.1f}/100")
        print(f"  Tests below 85:")
        
        for t in trans_tests:
            if t['score'] < 85:
                print(f"\n    {t['test_id']}: {t['score']:.0f}/100")
                print(f"      Passed: {t['passed_keywords']}")
                print(f"      Failed: {t['failed_keywords']}")
    
    print("\n" + "="*70)
    print("REASONING/COMMONSENSE TEST ANALYSIS")
    print("="*70)
    
    for suite in data['test_suites']:
        print(f"\n{suite['test_file']}:")
        reason_tests = [r for r in suite['results'] 
                       if r['category'] in ['reasoning', 'commonsense_reasoning']]
        
        if reason_tests:
            scores = [t['score'] for t in reason_tests]
            print(f"  Average: {sum(scores)/len(scores):.1f}/100")
            print(f"  Tests below 70:")
            
            for t in reason_tests:
                if t['score'] < 70:
                    print(f"\n    {t['test_id']}: {t['score']:.0f}/100")
                    print(f"      Prompt: {t['prompt'][:100]}...")
                    print(f"      Passed: {t['passed_keywords']}")
                    print(f"      Failed: {t['failed_keywords']}")
                    print(f"      Response: {t['response'][:150]}...")

if __name__ == "__main__":
    analyze_low_performers()
