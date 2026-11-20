import sys
import io
import time
import traceback
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class TestCase(BaseModel):
    input: Optional[str] = ""
    expected_output: str

class CodeExecutionRequest(BaseModel):
    language: str = "python"
    code: str
    test_cases: List[TestCase] = []
    timeout_seconds: float = 3.0

class TestCaseResult(BaseModel):
    test_idx: int
    passed: bool
    input: Optional[str] = ""
    expected_output: str
    actual_output: str
    error: Optional[str] = None

class CodeExecutionResponse(BaseModel):
    language: str
    passed_all: bool
    total_tests: int
    passed_tests: int
    execution_time_ms: float
    results: List[TestCaseResult]
    stdout: Optional[str] = ""
    error: Optional[str] = None

FORBIDDEN_PATTERNS = [
    "import os", "from os import", "import sys", "import subprocess",
    "shutil", "socket", "open(", "eval(", "exec(", "__import__",
    "input(", "breakpoint", "compile"
]

def sanitize_python_code(code: str) -> Optional[str]:
    for pat in FORBIDDEN_PATTERNS:
        if pat in code:
            return f"Security restriction: '{pat}' is not permitted in sandbox environment."
    return None

def execute_python_code(code: str, test_cases: List[TestCase], timeout_seconds: float = 3.0) -> CodeExecutionResponse:
    start_time = time.time()
    
    # Check security blacklist
    violation = sanitize_python_code(code)
    if violation:
        return CodeExecutionResponse(
            language="python",
            passed_all=False,
            total_tests=len(test_cases),
            passed_tests=0,
            execution_time_ms=0.0,
            results=[],
            error=violation
        )

    # Safe builtins
    safe_builtins = {
        'abs': abs, 'all': all, 'any': any, 'bin': bin, 'bool': bool,
        'dict': dict, 'enumerate': enumerate, 'filter': filter, 'float': float,
        'format': format, 'int': int, 'isinstance': isinstance, 'len': len,
        'list': list, 'map': map, 'max': max, 'min': min, 'next': next,
        'pow': pow, 'print': print, 'range': range, 'reversed': reversed,
        'round': round, 'set': set, 'sorted': sorted, 'str': str,
        'sum': sum, 'tuple': tuple, 'zip': zip,
        'True': True, 'False': False, 'None': None,
        'Exception': Exception, 'ValueError': ValueError, 'TypeError': TypeError,
        'IndexError': IndexError, 'KeyError': KeyError
    }
    
    global_env = {"__builtins__": safe_builtins}
    local_env: Dict[str, Any] = {}

    # Compile and execute student definition
    old_stdout = sys.stdout
    captured_stdout = io.StringIO()
    try:
        sys.stdout = captured_stdout
        exec(code, global_env, local_env)
    except Exception as e:
        sys.stdout = old_stdout
        elapsed = (time.time() - start_time) * 1000
        return CodeExecutionResponse(
            language="python",
            passed_all=False,
            total_tests=len(test_cases),
            passed_tests=0,
            execution_time_ms=round(elapsed, 2),
            results=[],
            stdout=captured_stdout.getvalue(),
            error=f"Syntax/Runtime Error during definition: {traceback.format_exc(limit=1)}"
        )
    finally:
        sys.stdout = old_stdout

    # Now run against test cases
    results: List[TestCaseResult] = []
    passed_count = 0

    if not test_cases:
        # Standalone execution
        elapsed = (time.time() - start_time) * 1000
        return CodeExecutionResponse(
            language="python",
            passed_all=True,
            total_tests=0,
            passed_tests=0,
            execution_time_ms=round(elapsed, 2),
            results=[],
            stdout=captured_stdout.getvalue(),
            error=None
        )

    for idx, tc in enumerate(test_cases):
        test_stdout = io.StringIO()
        try:
            sys.stdout = test_stdout
            # If tc.input is a function call expression, evaluate it against local_env
            expr_to_eval = tc.input.strip() if tc.input else ""
            if expr_to_eval:
                res = eval(expr_to_eval, global_env, local_env)
                actual_output = str(res).strip()
            else:
                actual_output = test_stdout.getvalue().strip()
                
            expected = tc.expected_output.strip()
            passed = (actual_output == expected)
            if passed:
                passed_count += 1

            results.append(TestCaseResult(
                test_idx=idx + 1,
                passed=passed,
                input=tc.input,
                expected_output=expected,
                actual_output=actual_output,
                error=None
            ))
        except Exception as e:
            results.append(TestCaseResult(
                test_idx=idx + 1,
                passed=False,
                input=tc.input,
                expected_output=tc.expected_output,
                actual_output="",
                error=str(e)
            ))
        finally:
            sys.stdout = old_stdout

    elapsed = (time.time() - start_time) * 1000
    all_passed = (passed_count == len(test_cases))

    return CodeExecutionResponse(
        language="python",
        passed_all=all_passed,
        total_tests=len(test_cases),
        passed_tests=passed_count,
        execution_time_ms=round(elapsed, 2),
        results=results,
        stdout=captured_stdout.getvalue(),
        error=None if all_passed else f"{len(test_cases) - passed_count} test case(s) failed."
    )
