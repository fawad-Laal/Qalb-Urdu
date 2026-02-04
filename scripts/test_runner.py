"""
Qalb Model Test Runner
======================
Automated testing framework for Qalb Urdu LLM evaluation.
Supports both Urdu Nastaliq and Roman Urdu test cases.

Features:
- System specs capture
- Error handling with automatic retry
- Resume from last checkpoint on failure
- Offline-capable (no internet required for Ollama local)

Author: Fawad Hussain
Website: fawadhs.dev
"""

import json
import os
import sys
import time
import platform
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any
from tqdm import tqdm

# Try importing ollama with error handling
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  ollama package not installed. Run: pip install ollama")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "enstazao/qalb:8b-instruct-fp16"
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TESTS_DIR = PROJECT_ROOT / "tests"
CHECKPOINT_DIR = DATA_DIR / "checkpoints"

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
CONNECTION_TIMEOUT = 30


# ============================================================
# System Specs Capture
# ============================================================

@dataclass
class SystemSpecs:
    """System specifications capture."""
    hostname: str = ""
    platform: str = ""
    platform_release: str = ""
    platform_version: str = ""
    architecture: str = ""
    processor: str = ""
    cpu_count: int = 0
    cpu_freq_mhz: float = 0.0
    ram_total_gb: float = 0.0
    ram_available_gb: float = 0.0
    disk_total_gb: float = 0.0
    disk_free_gb: float = 0.0
    python_version: str = ""
    ollama_version: str = ""
    model_name: str = ""
    timestamp: str = ""
    internet_available: bool = False


def get_system_specs(model_name: str = MODEL_NAME) -> SystemSpecs:
    """Capture current system specifications."""
    specs = SystemSpecs()
    specs.timestamp = datetime.now().isoformat()
    specs.model_name = model_name
    
    # Basic platform info
    specs.hostname = platform.node()
    specs.platform = platform.system()
    specs.platform_release = platform.release()
    specs.platform_version = platform.version()
    specs.architecture = platform.machine()
    specs.processor = platform.processor()
    specs.python_version = platform.python_version()
    
    # CPU info
    specs.cpu_count = os.cpu_count() or 0
    
    # Detailed system info with psutil
    if PSUTIL_AVAILABLE:
        try:
            # CPU frequency
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                specs.cpu_freq_mhz = cpu_freq.current
            
            # RAM
            memory = psutil.virtual_memory()
            specs.ram_total_gb = round(memory.total / (1024**3), 2)
            specs.ram_available_gb = round(memory.available / (1024**3), 2)
            
            # Disk
            disk = psutil.disk_usage('/')
            specs.disk_total_gb = round(disk.total / (1024**3), 2)
            specs.disk_free_gb = round(disk.free / (1024**3), 2)
        except Exception as e:
            print(f"⚠️  Could not get detailed system info: {e}")
    else:
        # Fallback for Windows without psutil
        try:
            if specs.platform == "Windows":
                # Get RAM using wmic
                result = subprocess.run(
                    ["wmic", "computersystem", "get", "TotalPhysicalMemory"],
                    capture_output=True, text=True, timeout=10
                )
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    ram_bytes = int(lines[1].strip())
                    specs.ram_total_gb = round(ram_bytes / (1024**3), 2)
        except Exception:
            pass
    
    # Ollama version
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True, text=True, timeout=10
        )
        specs.ollama_version = result.stdout.strip() or result.stderr.strip()
    except Exception:
        # Try with full path on Windows
        try:
            ollama_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
            result = subprocess.run(
                [ollama_path, "--version"],
                capture_output=True, text=True, timeout=10
            )
            specs.ollama_version = result.stdout.strip() or result.stderr.strip()
        except Exception:
            specs.ollama_version = "Unknown"
    
    # Internet connectivity check
    specs.internet_available = check_internet_connection()
    
    return specs


def check_internet_connection(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
    """Check if internet connection is available."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def check_ollama_connection() -> bool:
    """Check if Ollama service is running and accessible."""
    if not OLLAMA_AVAILABLE:
        return False
    
    try:
        # Try to list models - this will fail if Ollama isn't running
        ollama.list()
        return True
    except Exception:
        return False


# ============================================================
# Checkpoint Management (Resume Functionality)
# ============================================================

@dataclass
class Checkpoint:
    """Checkpoint for resuming interrupted tests."""
    test_file: str
    completed_test_ids: List[str] = field(default_factory=list)
    results: List[Dict] = field(default_factory=list)
    last_updated: str = ""
    system_specs: Dict = field(default_factory=dict)


def save_checkpoint(checkpoint: Checkpoint, checkpoint_file: Path):
    """Save checkpoint to disk."""
    checkpoint.last_updated = datetime.now().isoformat()
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(asdict(checkpoint), f, ensure_ascii=False, indent=2)


def load_checkpoint(checkpoint_file: Path) -> Optional[Checkpoint]:
    """Load checkpoint from disk if exists."""
    if not checkpoint_file.exists():
        return None
    
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Checkpoint(**data)
    except Exception as e:
        print(f"⚠️  Could not load checkpoint: {e}")
        return None


def clear_checkpoint(checkpoint_file: Path):
    """Delete checkpoint file after successful completion."""
    if checkpoint_file.exists():
        checkpoint_file.unlink()


# ============================================================
# Test Data Structures
# ============================================================

@dataclass
class TestCase:
    """Individual test case structure."""
    id: str
    category: str
    script_type: str  # "urdu" or "roman"
    prompt: str
    expected_language: str  # "urdu", "roman", "either"
    expected_keywords: List[str]
    difficulty: str  # "easy", "medium", "hard"
    tags: List[str]


@dataclass
class TestResult:
    """Result of a single test execution."""
    test_id: str
    category: str
    script_type: str
    prompt: str
    response: str
    response_time_ms: float
    tokens_per_second: float
    urdu_char_ratio: float
    passed_keywords: List[str]
    failed_keywords: List[str]
    score: float
    timestamp: str
    model: str
    error: Optional[str] = None
    retry_count: int = 0


# ============================================================
# Main Test Runner
# ============================================================

class QalbTestRunner:
    """Main test runner for Qalb model evaluation with error handling and resume."""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.results: List[TestResult] = []
        self.system_specs: Optional[SystemSpecs] = None
        self.current_checkpoint: Optional[Checkpoint] = None
        
    def initialize(self) -> bool:
        """Initialize the test runner and verify prerequisites."""
        print("\n🔍 Checking prerequisites...")
        
        # Capture system specs
        print("   📊 Capturing system specifications...")
        self.system_specs = get_system_specs(self.model_name)
        
        # Display specs
        print(f"\n   {'─'*50}")
        print(f"   System: {self.system_specs.platform} {self.system_specs.platform_release}")
        print(f"   CPU: {self.system_specs.processor} ({self.system_specs.cpu_count} cores)")
        print(f"   RAM: {self.system_specs.ram_available_gb:.1f} GB available / {self.system_specs.ram_total_gb:.1f} GB total")
        print(f"   Disk: {self.system_specs.disk_free_gb:.1f} GB free")
        print(f"   Python: {self.system_specs.python_version}")
        print(f"   Ollama: {self.system_specs.ollama_version}")
        print(f"   Internet: {'✅ Connected' if self.system_specs.internet_available else '❌ Offline'}")
        print(f"   {'─'*50}\n")
        
        # Check Ollama
        if not OLLAMA_AVAILABLE:
            print("❌ Ollama Python package not installed!")
            print("   Run: pip install ollama")
            return False
        
        # Check Ollama service
        print("   🔌 Checking Ollama service...")
        if not check_ollama_connection():
            print("❌ Ollama service not running!")
            print("   Start Ollama or run: ollama serve")
            
            # Try to start Ollama automatically
            print("   🔄 Attempting to start Ollama...")
            try:
                if self.system_specs.platform == "Windows":
                    subprocess.Popen(
                        ["cmd", "/c", "start", "/b", "ollama", "serve"],
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    subprocess.Popen(
                        ["ollama", "serve"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                time.sleep(5)  # Wait for service to start
                
                if check_ollama_connection():
                    print("   ✅ Ollama started successfully!")
                else:
                    print("   ❌ Could not start Ollama automatically")
                    return False
            except Exception as e:
                print(f"   ❌ Failed to start Ollama: {e}")
                return False
        else:
            print("   ✅ Ollama service is running")
        
        # Check if model is available
        print(f"   🤖 Checking model: {self.model_name}...")
        try:
            models = ollama.list()
            # Handle different ollama library versions
            model_list = models.get('models', []) if isinstance(models, dict) else getattr(models, 'models', [])
            model_names = []
            for m in model_list:
                # Handle both dict and Model object formats
                if isinstance(m, dict):
                    model_names.append(m.get('name', '') or m.get('model', ''))
                else:
                    model_names.append(getattr(m, 'model', '') or getattr(m, 'name', ''))
            
            model_found = any(self.model_name in name or name in self.model_name for name in model_names)
            if model_found:
                print(f"   ✅ Model found: {self.model_name}")
            else:
                print(f"   ⚠️  Model not found locally. Available: {model_names}")
                print(f"   Run: ollama pull {self.model_name}")
        except Exception as e:
            print(f"   ⚠️  Could not check models: {e}")
        
        print("\n✅ Prerequisites check complete!\n")
        return True
        
    def calculate_urdu_ratio(self, text: str) -> float:
        """Calculate ratio of Urdu characters in response."""
        if not text:
            return 0.0
        
        urdu_ranges = [
            (0x0600, 0x06FF),  # Arabic
            (0x0750, 0x077F),  # Arabic Supplement
            (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
            (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
        ]
        
        urdu_count = 0
        total_chars = 0
        
        for char in text:
            if char.isalpha():
                total_chars += 1
                code = ord(char)
                for start, end in urdu_ranges:
                    if start <= code <= end:
                        urdu_count += 1
                        break
        
        return urdu_count / total_chars if total_chars > 0 else 0.0
    
    def check_keywords(self, response: str, keywords: List[str]) -> tuple:
        """Check which expected keywords are present in response.
        
        Keywords are treated as OR conditions - finding ANY keyword is a pass.
        Also handles number variations (e.g., "1,000" matches "1000").
        """
        # Normalize response: remove commas from numbers, lowercase
        response_normalized = response.lower().replace(",", "").replace("،", "")
        
        passed = []
        failed = []
        
        for kw in keywords:
            kw_normalized = kw.lower().replace(",", "").replace("،", "")
            if kw_normalized in response_normalized:
                passed.append(kw)
            else:
                failed.append(kw)
        
        return passed, failed
    
    def calculate_score(self, result: TestResult, test_case: TestCase) -> float:
        """Calculate overall score for a test result.
        
        Scoring breakdown:
        - Response exists and is meaningful (20%)
        - Language appropriateness (30%) - adjusted for math/code content
        - Keywords matched - ANY keyword match = full points (30%)
        - Response time bonus (20%)
        """
        # If there was an error, score is 0
        if result.error:
            return 0.0
            
        score = 0.0
        
        # Response exists (20%)
        if result.response and len(result.response) > 10:
            score += 20.0
        
        # Language appropriateness (30%) - ADJUSTED
        # For math/reasoning, allow mixed scripts (numbers + Urdu)
        is_math_or_reasoning = test_case.category in ["mathematics", "mathematical_reasoning", "reasoning"]
        
        if test_case.expected_language == "urdu":
            if is_math_or_reasoning:
                # For math, be lenient - if there's ANY Urdu, give partial credit
                if result.urdu_char_ratio > 0:
                    score += 30.0 * min(1.0, result.urdu_char_ratio * 2)  # Double the ratio, cap at 1
                else:
                    score += 15.0  # Base score for correct math answer even without Urdu
            else:
                score += 30.0 * result.urdu_char_ratio
        elif test_case.expected_language == "roman":
            score += 30.0 * (1 - result.urdu_char_ratio)
        else:  # either
            score += 30.0
        
        # Keywords matched (30%) - ANY keyword match = success (OR logic)
        total_keywords = len(test_case.expected_keywords)
        if total_keywords > 0:
            # If ANY keyword matches, that's a success
            if len(result.passed_keywords) > 0:
                # Bonus for matching more keywords, but base success is achieved
                base_score = 20.0  # Found at least one
                bonus = 10.0 * (len(result.passed_keywords) / total_keywords)
                score += base_score + bonus
            else:
                score += 0.0  # No keywords matched
        else:
            score += 30.0  # No keywords required
        
        # Response time bonus (20%) - faster = better
        if result.response_time_ms < 5000:
            score += 20.0
        elif result.response_time_ms < 10000:
            score += 15.0
        elif result.response_time_ms < 20000:
            score += 10.0
        else:
            score += 5.0
        
        return min(100.0, score)
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case with retry logic."""
        last_error = None
        retry_count = 0
        
        for attempt in range(MAX_RETRIES):
            start_time = time.time()
            
            try:
                response = ollama.generate(
                    model=self.model_name,
                    prompt=test_case.prompt,
                    options={
                        "num_predict": 256,
                        "temperature": 0.7,
                    }
                )
                
                end_time = time.time()
                response_text = response.get("response", "")
                
                # Calculate metrics
                response_time_ms = (end_time - start_time) * 1000
                
                # Estimate tokens (rough: 1 token ≈ 4 chars for Urdu)
                approx_tokens = len(response_text) / 4
                tokens_per_sec = approx_tokens / (response_time_ms / 1000) if response_time_ms > 0 else 0
                
                urdu_ratio = self.calculate_urdu_ratio(response_text)
                passed_kw, failed_kw = self.check_keywords(response_text, test_case.expected_keywords)
                
                result = TestResult(
                    test_id=test_case.id,
                    category=test_case.category,
                    script_type=test_case.script_type,
                    prompt=test_case.prompt,
                    response=response_text,
                    response_time_ms=response_time_ms,
                    tokens_per_second=tokens_per_sec,
                    urdu_char_ratio=urdu_ratio,
                    passed_keywords=passed_kw,
                    failed_keywords=failed_kw,
                    score=0.0,
                    timestamp=datetime.now().isoformat(),
                    model=self.model_name,
                    error=None,
                    retry_count=retry_count
                )
                
                result.score = self.calculate_score(result, test_case)
                return result
                
            except Exception as e:
                last_error = str(e)
                retry_count = attempt + 1
                
                # Check if it's a connection error
                if "connection" in last_error.lower() or "refused" in last_error.lower():
                    print(f"\n   ⚠️  Connection error on {test_case.id}, retry {retry_count}/{MAX_RETRIES}...")
                    
                    # Wait before retry
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY_SECONDS)
                        
                        # Check if Ollama is still running
                        if not check_ollama_connection():
                            print("   🔄 Ollama connection lost. Waiting for reconnection...")
                            for _ in range(6):  # Wait up to 30 seconds
                                time.sleep(5)
                                if check_ollama_connection():
                                    print("   ✅ Reconnected!")
                                    break
                else:
                    # Non-connection error, don't retry
                    break
        
        # All retries failed
        end_time = time.time()
        return TestResult(
            test_id=test_case.id,
            category=test_case.category,
            script_type=test_case.script_type,
            prompt=test_case.prompt,
            response="",
            response_time_ms=(end_time - start_time) * 1000,
            tokens_per_second=0,
            urdu_char_ratio=0,
            passed_keywords=[],
            failed_keywords=test_case.expected_keywords,
            score=0.0,
            timestamp=datetime.now().isoformat(),
            model=self.model_name,
            error=f"FAILED after {retry_count} retries: {last_error}",
            retry_count=retry_count
        )
    
    def load_test_cases(self, file_path: Path) -> List[TestCase]:
        """Load test cases from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [TestCase(**tc) for tc in data.get("test_cases", [])]
    
    def run_test_suite(self, test_file: Path, output_dir: Path) -> Dict[str, Any]:
        """Run all tests from a test file with checkpoint support."""
        test_cases = self.load_test_cases(test_file)
        
        # Setup checkpoint
        checkpoint_file = CHECKPOINT_DIR / f"{test_file.stem}_checkpoint.json"
        checkpoint = load_checkpoint(checkpoint_file)
        
        # Determine which tests to run
        completed_ids = set()
        results = []
        
        if checkpoint and checkpoint.test_file == test_file.name:
            completed_ids = set(checkpoint.completed_test_ids)
            results = [TestResult(**r) if isinstance(r, dict) else r for r in checkpoint.results]
            print(f"\n📂 Resuming from checkpoint: {len(completed_ids)}/{len(test_cases)} tests completed")
        else:
            # Start fresh
            checkpoint = Checkpoint(
                test_file=test_file.name,
                system_specs=asdict(self.system_specs) if self.system_specs else {}
            )
        
        # Filter remaining tests
        remaining_tests = [tc for tc in test_cases if tc.id not in completed_ids]
        
        print(f"\n{'='*60}")
        print(f"Running: {test_file.name}")
        print(f"Total Tests: {len(test_cases)}")
        print(f"Remaining: {len(remaining_tests)}")
        print(f"{'='*60}\n")
        
        # Run tests with progress bar
        try:
            for tc in tqdm(remaining_tests, desc="Testing", initial=len(completed_ids), total=len(test_cases)):
                result = self.run_single_test(tc)
                results.append(result)
                self.results.append(result)
                
                # Update checkpoint after each test
                checkpoint.completed_test_ids.append(tc.id)
                checkpoint.results.append(asdict(result))
                save_checkpoint(checkpoint, checkpoint_file)
                
                # If there was an error, pause briefly
                if result.error:
                    print(f"\n   ⚠️  Error on {tc.id}: {result.error[:50]}...")
                    
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Test interrupted! Progress saved to checkpoint.")
            print(f"   Completed: {len(checkpoint.completed_test_ids)}/{len(test_cases)}")
            print(f"   Resume by running the script again.")
            raise
        
        # Calculate summary
        successful_results = [r for r in results if not r.error]
        error_results = [r for r in results if r.error]
        
        summary = {
            "test_file": test_file.name,
            "total_tests": len(results),
            "successful_tests": len(successful_results),
            "failed_tests": len(error_results),
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "system_specs": asdict(self.system_specs) if self.system_specs else {},
            "metrics": {
                "average_score": sum(r.score for r in successful_results) / len(successful_results) if successful_results else 0,
                "average_response_time_ms": sum(r.response_time_ms for r in successful_results) / len(successful_results) if successful_results else 0,
                "average_tokens_per_second": sum(r.tokens_per_second for r in successful_results) / len(successful_results) if successful_results else 0,
                "average_urdu_ratio": sum(r.urdu_char_ratio for r in successful_results) / len(successful_results) if successful_results else 0,
                "total_retries": sum(r.retry_count for r in results),
            },
            "errors": [{"test_id": r.test_id, "error": r.error} for r in error_results],
            "results": [asdict(r) if hasattr(r, '__dataclass_fields__') else r for r in results]
        }
        
        # Save results
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{test_file.stem}_results.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # Clear checkpoint on successful completion
        clear_checkpoint(checkpoint_file)
        
        print(f"\n✅ Results saved: {output_file}")
        print(f"   Successful: {len(successful_results)}/{len(results)}")
        print(f"   Average Score: {summary['metrics']['average_score']:.1f}/100")
        print(f"   Avg Response Time: {summary['metrics']['average_response_time_ms']:.0f}ms")
        if error_results:
            print(f"   ⚠️  {len(error_results)} tests had errors")
        
        return summary
    
    def run_all_baseline_tests(self, round_num: int = 4):
        """Run all baseline tests for both Urdu and Roman scripts.
        
        Args:
            round_num: Test round number (1 = original, 2 = improved keywords, 3 = math fixes, 4 = expanded synonyms)
        """
        if round_num == 4:
            urdu_tests = TESTS_DIR / "baseline" / "urdu_script_tests_round4.json"
            roman_tests = TESTS_DIR / "baseline" / "roman_urdu_tests_round4.json"
        elif round_num == 3:
            urdu_tests = TESTS_DIR / "baseline" / "urdu_script_tests_round3.json"
            roman_tests = TESTS_DIR / "baseline" / "roman_urdu_tests_round3.json"
        elif round_num == 2:
            urdu_tests = TESTS_DIR / "baseline" / "urdu_script_tests_round2.json"
            roman_tests = TESTS_DIR / "baseline" / "roman_urdu_tests_round2.json"
        else:
            urdu_tests = TESTS_DIR / "baseline" / "urdu_script_tests.json"
            roman_tests = TESTS_DIR / "baseline" / "roman_urdu_tests.json"
        
        all_summaries = []
        
        if urdu_tests.exists():
            try:
                summary = self.run_test_suite(
                    urdu_tests, 
                    DATA_DIR / "baseline" / "urdu_script"
                )
                all_summaries.append(summary)
            except KeyboardInterrupt:
                print("\n⚠️  Urdu tests interrupted. You can resume later.")
                return
        else:
            print(f"⚠️  Not found: {urdu_tests}")
        
        if roman_tests.exists():
            try:
                summary = self.run_test_suite(
                    roman_tests,
                    DATA_DIR / "baseline" / "roman_urdu"
                )
                all_summaries.append(summary)
            except KeyboardInterrupt:
                print("\n⚠️  Roman Urdu tests interrupted. You can resume later.")
                return
        else:
            print(f"⚠️  Not found: {roman_tests}")
        
        # Generate combined summary
        if all_summaries:
            combined = {
                "phase": "baseline",
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "system_specs": asdict(self.system_specs) if self.system_specs else {},
                "test_suites": all_summaries,
                "overall_metrics": {
                    "total_tests": sum(s["total_tests"] for s in all_summaries),
                    "successful_tests": sum(s["successful_tests"] for s in all_summaries),
                    "failed_tests": sum(s["failed_tests"] for s in all_summaries),
                    "average_score": sum(s["metrics"]["average_score"] for s in all_summaries) / len(all_summaries),
                    "total_retries": sum(s["metrics"]["total_retries"] for s in all_summaries),
                }
            }
            
            combined_file = DATA_DIR / "baseline" / "combined_results.json"
            combined_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(combined, f, ensure_ascii=False, indent=2)
            
            print(f"\n{'='*60}")
            print("BASELINE COMPLETE")
            print(f"{'='*60}")
            print(f"Total Tests: {combined['overall_metrics']['total_tests']}")
            print(f"Successful: {combined['overall_metrics']['successful_tests']}")
            print(f"Failed: {combined['overall_metrics']['failed_tests']}")
            print(f"Overall Score: {combined['overall_metrics']['average_score']:.1f}/100")
            print(f"Results: {combined_file}")


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("QALB MODEL TEST RUNNER - ROUND 4")
    print("fawadhs.dev")
    print("="*60)
    
    runner = QalbTestRunner()
    
    # Initialize and check prerequisites
    if not runner.initialize():
        print("\n❌ Prerequisites check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Run tests - Round 4 with expanded synonym keywords
    try:
        runner.run_all_baseline_tests(round_num=4)
    except KeyboardInterrupt:
        print("\n\n👋 Test run interrupted. Progress has been saved.")
        print("   Run the script again to resume from where you left off.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   Progress has been saved. Run again to resume.")
        sys.exit(1)


if __name__ == "__main__":
    main()
