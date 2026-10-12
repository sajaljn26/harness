import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# --------------------------------------------------------------------------
# 1. CONNECT YOUR AGENT HERE
# --------------------------------------------------------------------------
from agent_engine.llm import call_llm
from agent_engine.tools import TOOLS
from agent_engine.session import Session
from agent_engine.ui import ui

def run_agent(prompt: str) -> dict:
    """
    Runs the agent in a isolated temporary directory.
    """
    # Create a unique session for this specific benchmark task
    session = Session(f"bench_{int(time.time())}")
    history = session.history
    
    metrics = {
        "steps": 0,
        "tool_calls": 0,
        "tool_failures": 0,
        "recovered": 0,
        "tokens": 0,
    }
    
    # Add the prompt to history
    history.append({"role": "user", "content": prompt})
    
    # Agent Loop
    while True:
        try:
            message = call_llm(history)
            metrics["steps"] += 1
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    metrics["tool_calls"] += 1
                    fn_name = tool_call.function.name
                    
                    try:
                        args = json.loads(tool_call.function.arguments)
                        result = TOOLS[fn_name](**args)
                        
                        if "Error" in result or "SECURITY ERROR" in result:
                            metrics["tool_failures"] += 1
                        else:
                            if metrics["tool_failures"] > 0:
                                metrics["recovered"] += 1
                                
                    except Exception as e:
                        result = f"Tool execution error: {str(e)}"
                        metrics["tool_failures"] += 1
                    
                    history.append(message)
                    history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": fn_name,
                        "content": result,
                    })
                continue
            
            if message.content:
                history.append({"role": "assistant", "content": message.content})
            
            break 
            
        except Exception as e:
            print(f"Agent crashed during benchmark: {e}")
            break

    return metrics

# --------------------------------------------------------------------------
# 2. TASKS  (prompt + an independent check that exits 0 on success)
# --------------------------------------------------------------------------
PY = sys.executable
SLEEP_BETWEEN_TASKS = 10  # seconds; avoids provider rate limits

TASKS = [
    {
        "name": "fizzbuzz",
        "prompt": "Create fizzbuzz.py with a function fizzbuzz(n) that returns 'Fizz', 'Buzz', 'FizzBuzz', or str(n).",
        "verify": f"{PY} -c \"from fizzbuzz import fizzbuzz as f; assert f(15)=='FizzBuzz' and f(3)=='Fizz' and f(5)=='Buzz' and f(7)=='7'\"",
    },
    {
        "name": "palindrome",
        "prompt": "Create palindrome.py with is_palindrome(s) that ignores case and non-alphanumeric characters.",
        "verify": f"{PY} -c \"from palindrome import is_palindrome as p; assert p('A man, a plan, a canal, Panama') and not p('hello')\"",
    },
    {
        "name": "word_count_cli",
        "prompt": "Create wc.py that reads a file path from sys.argv[1] and prints the number of words in it.",
        "setup": {"sample.txt": "one two three four five"},
        "verify": f"{PY} -c \"import subprocess,sys; o=subprocess.run([sys.executable,'wc.py','sample.txt'],capture_output=True,text=True).stdout; assert '5' in o\"",
    },
    {
        "name": "fix_bug",
        "prompt": "The function in buggy.py should return the sum of a list, but it fails. Fix it.",
        "setup": {"buggy.py": "def total(xs):\n    t = 0\n    for i in range(1, len(xs)):\n        t += xs[i]\n    return t\n"},
        "verify": f"{PY} -c \"from buggy import total; assert total([1,2,3])==6\"",
    },
    {
        "name": "json_to_csv",
        "prompt": "Write convert.py that reads data.json (a list of flat objects) and writes data.csv with a header row.",
        "setup": {"data.json": json.dumps([{"a": 1, "b": 2}, {"a": 3, "b": 4}])},
        "verify": f"{PY} -c \"import subprocess,sys; subprocess.run([sys.executable,'convert.py'],check=True); assert len(open('data.csv').read().strip().splitlines())==3\"",
    },
    {
        "name": "flask_health",
        "prompt": "Create app.py, a Flask app with GET /health returning JSON {\"status\": \"ok\"}. Install Flask if needed.",
        "verify": f"{PY} -c \"from app import app; r=app.test_client().get('/health'); assert r.get_json()=={{'status':'ok'}}\"",
    },
    {
        "name": "write_tests",
        "prompt": "mathx.py has add(a,b). Create test_mathx.py with pytest tests for it and run them.",
        "setup": {"mathx.py": "def add(a, b):\n    return a + b\n"},
        "verify": f"{PY} -m pytest -q test_mathx.py",
    },
    {
        "name": "refactor",
        "prompt": "Refactor messy.py so the duplicated logic lives in one helper function. Behavior must not change.",
        "setup": {"messy.py": "def a(x):\n    return (x*2)+1\n\ndef b(x):\n    return (x*2)+1\n"},
        "verify": f"{PY} -c \"from messy import a,b; assert a(3)==7 and b(3)==7\"",
    },
    {
        "name": "multi_file",
        "prompt": "Create a package 'calc' with calc/__init__.py and calc/ops.py exposing add and mul.",
        "verify": f"{PY} -c \"from calc.ops import add, mul; assert add(2,3)==5 and mul(2,3)==6\"",
    },
    {
        "name": "log_parser",
        "prompt": "Write parse.py that counts lines containing 'ERROR' in app.log and prints the count.",
        "setup": {"app.log": "INFO ok\nERROR bad\nERROR worse\nINFO fine\n"},
        "verify": f"{PY} -c \"import subprocess,sys; o=subprocess.run([sys.executable,'parse.py'],capture_output=True,text=True).stdout; assert '2' in o\"",
    },
]

# --------------------------------------------------------------------------
# 3. HARNESS
# --------------------------------------------------------------------------
def run_task(task: dict) -> dict:
    origin = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        for fname, content in task.get("setup", {}).items():
            Path(tmp, fname).write_text(content)
        os.chdir(tmp)
        start = time.time()
        metrics, error = {}, None
        try:
            metrics = run_agent(task["prompt"]) or {}
        except Exception as e:
            error = repr(e)
        elapsed = time.time() - start
        check = subprocess.run(task["verify"], shell=True, capture_output=True, text=True, timeout=60)
        os.chdir(origin)

    return {
        "name": task["name"],
        "passed": check.returncode == 0 and error is None,
        "seconds": round(elapsed, 1),
        "error": error,
        **metrics,
    }

def avg(rows, key):
    vals = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    return round(sum(vals) / len(vals), 1) if vals else None

def main():
    print("\n" + "="*60)
    print("🚀 STARTING AGENT BENCHMARK SUITE")
    print("="*60 + "\n")
    
    rows = []
    for t in TASKS:
        print(f"▶ Testing {t['name']}...", end=" ", flush=True)
        r = run_task(t)
        rows.append(r)
        print("PASS ✅" if r["passed"] else "FAIL ❌", f"({r['seconds']}s)")
        time.sleep(SLEEP_BETWEEN_TASKS)

    passed = sum(r["passed"] for r in rows)
    total = len(rows)
    failures = sum(r.get("tool_failures", 0) for r in rows)
    recovered = sum(r.get("recovered", 0) for r in rows)

    print("\n" + "="*60)
    print(f"FINAL SUCCESS RATE : {passed}/{total} ({100 * passed // total}%)")
    print(f"Avg time per task  : {avg(rows, 'seconds')}s")
    if avg(rows, "steps") is not None:
        print(f"Avg steps per task : {avg(rows, 'steps')}")
    if avg(rows, "tool_calls") is not None:
        print(f"Avg tool calls    : {avg(rows, 'tool_calls')}")
    if failures:
        print(f"Tool-failure recovery: {recovered}/{failures} ({100 * recovered // failures}%)")
    print("="*60)

    Path("benchmark_results.json").write_text(json.dumps(rows, indent=2))
    print("\nSaved detailed results to benchmark_results.json")

if __name__ == "__main__":
    main()
