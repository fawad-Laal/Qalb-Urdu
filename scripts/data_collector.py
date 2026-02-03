"""
QALB Evaluation - Data Collector
================================

Collects and logs all test data throughout the evaluation process.
Data is stored in JSON format for final PDF report generation.

Author: Fawad Hussain (fawadhs.dev)
"""

import json
import os
import time
import platform
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import re


@dataclass
class TestResult:
    """Single test result data structure."""
    test_id: str
    category: str
    script_type: str  # urdu_nastaliq, roman_urdu, mixed
    input_text: str
    expected_output: Optional[str]
    actual_output: str
    is_correct: bool
    confidence_score: float
    response_time_seconds: float
    tokens_generated: int
    urdu_purity_score: float
    timestamp: str
    model_version: str
    prompting_strategy: str  # zero-shot, few-shot, chain-of-thought
    
    def to_dict(self) -> dict:
        return asdict(self)


class DataCollector:
    """Collects and manages all test data for Qalb evaluation."""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.setup_directories()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_directories(self):
        """Create required data directories."""
        directories = [
            self.base_path,
            f"{self.base_path}/baseline/urdu_script",
            f"{self.base_path}/baseline/roman_urdu",
            f"{self.base_path}/urdubench",
            f"{self.base_path}/evaluation",
            f"{self.base_path}/stress",
            "reports"
        ]
        for dir_path in directories:
            os.makedirs(dir_path, exist_ok=True)
    
    def log_setup(self, model_version: str = "enstazao/qalb:8b-instruct-fp16"):
        """Log system and model setup information."""
        setup_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "system": {
                "os": platform.system(),
                "os_version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "model": {
                "name": "Qalb-1.0-8B-Instruct",
                "version": model_version,
                "source": "Ollama"
            },
            "project": {
                "name": "QALB Urdu AI Testing",
                "author": "Fawad Hussain",
                "website": "fawadhs.dev",
                "repository": "https://github.com/fawad-Laal/Qalb-Urdu"
            }
        }
        
        self._save_json(f"{self.base_path}/setup_log.json", setup_data)
        print(f"✅ Setup logged: {self.base_path}/setup_log.json")
        return setup_data
    
    def calculate_urdu_purity(self, text: str) -> float:
        """
        Calculate the percentage of Urdu characters in the text.
        Urdu Unicode range: 0600-06FF (Arabic) + 0750-077F (Arabic Supplement)
        """
        if not text:
            return 0.0
        
        # Urdu/Arabic character pattern
        urdu_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')
        
        # Count Urdu characters
        urdu_chars = len(urdu_pattern.findall(text))
        
        # Count total non-whitespace characters
        total_chars = len(re.findall(r'\S', text))
        
        if total_chars == 0:
            return 0.0
        
        return (urdu_chars / total_chars) * 100
    
    def log_test_result(
        self,
        test_id: str,
        category: str,
        script_type: str,
        input_text: str,
        actual_output: str,
        expected_output: Optional[str] = None,
        is_correct: Optional[bool] = None,
        response_time: float = 0.0,
        prompting_strategy: str = "zero-shot",
        model_version: str = "enstazao/qalb:8b-instruct-fp16"
    ) -> TestResult:
        """Log a single test result."""
        
        # Calculate Urdu purity
        urdu_purity = self.calculate_urdu_purity(actual_output)
        
        # Estimate tokens (rough: 1 token ≈ 4 chars for Urdu)
        tokens_generated = len(actual_output) // 4
        
        # Auto-determine correctness if expected_output provided
        if is_correct is None and expected_output:
            is_correct = expected_output.lower() in actual_output.lower()
        
        result = TestResult(
            test_id=test_id,
            category=category,
            script_type=script_type,
            input_text=input_text,
            expected_output=expected_output,
            actual_output=actual_output,
            is_correct=is_correct or False,
            confidence_score=0.0,  # Can be set by model
            response_time_seconds=response_time,
            tokens_generated=tokens_generated,
            urdu_purity_score=urdu_purity,
            timestamp=datetime.now().isoformat(),
            model_version=model_version,
            prompting_strategy=prompting_strategy
        )
        
        # Determine save path
        if "urdubench" in category.lower():
            save_path = f"{self.base_path}/urdubench/{category}_results.json"
        elif script_type == "mixed":
            save_path = f"{self.base_path}/evaluation/code_switching_results.json"
        else:
            save_path = f"{self.base_path}/baseline/{script_type}/{category}_results.json"
        
        # Append to existing results
        self._append_result(save_path, result.to_dict())
        
        return result
    
    def _append_result(self, filepath: str, result: dict):
        """Append a result to a JSON file."""
        results = []
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                results = json.load(f)
        
        results.append(result)
        self._save_json(filepath, results)
    
    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_final_report_data(self) -> dict:
        """Aggregate all test data for final report."""
        report_data = {
            "report_date": datetime.now().strftime("%B %d, %Y"),
            "session_id": self.session_id,
            "model_name": "Qalb-1.0-8B-Instruct",
            "model_version": "enstazao/qalb:8b-instruct-fp16",
            "total_tests": 0,
            "summary": {
                "overall_accuracy": 0.0,
                "urdu_script_accuracy": 0.0,
                "roman_urdu_accuracy": 0.0,
                "avg_response_time": 0.0,
                "urdu_purity": 0.0
            },
            "categories": {},
            "recommendations": []
        }
        
        all_results = []
        urdu_results = []
        roman_results = []
        
        # Collect all baseline results
        for script_type in ["urdu_script", "roman_urdu"]:
            script_dir = f"{self.base_path}/baseline/{script_type}"
            if os.path.exists(script_dir):
                for filename in os.listdir(script_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(script_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            results = json.load(f)
                            all_results.extend(results)
                            if script_type == "urdu_script":
                                urdu_results.extend(results)
                            else:
                                roman_results.extend(results)
                            
                            # Category stats
                            category = filename.replace('_results.json', '')
                            if category not in report_data["categories"]:
                                report_data["categories"][category] = {
                                    "urdu_accuracy": 0.0,
                                    "roman_accuracy": 0.0,
                                    "overall": 0.0,
                                    "total_tests": 0
                                }
        
        # Calculate statistics
        if all_results:
            report_data["total_tests"] = len(all_results)
            
            correct = sum(1 for r in all_results if r.get("is_correct"))
            report_data["summary"]["overall_accuracy"] = (correct / len(all_results)) * 100
            
            if urdu_results:
                urdu_correct = sum(1 for r in urdu_results if r.get("is_correct"))
                report_data["summary"]["urdu_script_accuracy"] = (urdu_correct / len(urdu_results)) * 100
            
            if roman_results:
                roman_correct = sum(1 for r in roman_results if r.get("is_correct"))
                report_data["summary"]["roman_urdu_accuracy"] = (roman_correct / len(roman_results)) * 100
            
            # Average response time
            times = [r.get("response_time_seconds", 0) for r in all_results if r.get("response_time_seconds")]
            if times:
                report_data["summary"]["avg_response_time"] = sum(times) / len(times)
            
            # Average Urdu purity
            purities = [r.get("urdu_purity_score", 0) for r in all_results if r.get("urdu_purity_score")]
            if purities:
                report_data["summary"]["urdu_purity"] = sum(purities) / len(purities)
        
        # Generate recommendations based on results
        report_data["recommendations"] = self._generate_recommendations(report_data)
        
        # Save final report data
        self._save_json(f"{self.base_path}/final_report.json", report_data)
        print(f"✅ Final report data generated: {self.base_path}/final_report.json")
        
        return report_data
    
    def _generate_recommendations(self, report_data: dict) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        summary = report_data.get("summary", {})
        
        urdu_acc = summary.get("urdu_script_accuracy", 0)
        roman_acc = summary.get("roman_urdu_accuracy", 0)
        purity = summary.get("urdu_purity", 0)
        
        if urdu_acc > roman_acc + 10:
            recommendations.append(
                "Qalb performs significantly better with Urdu script. "
                "Consider transliterating Roman Urdu inputs to Nastaliq for production use."
            )
        
        if purity < 90:
            recommendations.append(
                "Urdu purity is below 90%. Implement post-processing to filter "
                "non-Urdu characters from outputs."
            )
        
        if summary.get("avg_response_time", 0) > 30:
            recommendations.append(
                "Response times are high. Consider using quantized model (Q4) "
                "for faster inference in latency-sensitive applications."
            )
        
        recommendations.extend([
            "Use few-shot prompting for complex reasoning tasks to improve accuracy.",
            "Implement appropriate system prompts for specific use cases.",
            "Monitor outputs for cultural sensitivity in production deployments."
        ])
        
        return recommendations


def main():
    """Demo the data collector."""
    collector = DataCollector()
    
    # Log setup
    collector.log_setup()
    
    # Example test logging
    collector.log_test_result(
        test_id="QA-001",
        category="question_answering",
        script_type="urdu_script",
        input_text="پاکستان کا دارالحکومت کیا ہے؟",
        actual_output="پاکستان کا دارالحکومت اسلام آباد ہے۔",
        expected_output="اسلام آباد",
        response_time=12.5
    )
    
    print("✅ Data collector initialized and test logged!")
    print(f"📁 Data directory: {collector.base_path}/")


if __name__ == "__main__":
    main()
