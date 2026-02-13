import os
import subprocess
import json
import re

# NC-TEST-001: Behavioral Validator
# This script executes the defined tests and verifies success criteria.

SCRIPTS_DIR = os.path.expanduser("~/comms")
TESTS_FILE = os.path.expanduser("~/comms/agent_behavior_tests.md")
BLOG_ID = "3560842955308737645"

def run_test(test_id, command):
    print(f"\n>>> [NC-TEST-001] Executing TEST {test_id}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def validate():
    print("--- INITIATING SENTI-001 BEHAVIORAL VALIDATION ---")
    
    results = {}

    # TEST 04: UCP Hardware Discovery (Performed first to satisfy WebMCP requirement)
    stdout, stderr, code = run_test("04", ["python3", os.path.join(SCRIPTS_DIR, "ucp_discovery.py")])
    ucp_path = os.path.expanduser("~/ucp.json")
    if code == 0 and os.path.exists(ucp_path):
        with open(ucp_path, 'r') as f:
            ucp = json.load(f)
            if ucp.get("hardware", {}).get("processor") != "Unknown CPU":
                print("TEST 04 SUCCESS: Hardware Discovery validated.")
                results["04"] = "PASS"
            else:
                print("TEST 04 FAILED: Incomplete hardware data.")
                results["04"] = "FAIL"
    else:
        print(f"TEST 04 FAILED: {stderr}")
        results["04"] = "FAIL"

    # TEST 03: BMM Loopback (Critical Intelligence Gate)
    stdout, stderr, code = run_test("03", ["python3", os.path.join(SCRIPTS_DIR, "blog_summarizer.py")])
    memory_path = os.path.expanduser("~/comms/MEMORY.md")
    if code == 0 and os.path.exists(memory_path):
        mtime = os.path.getmtime(memory_path)
        import time
        if (time.time() - mtime) < 60: # Updated in the last minute
            print("TEST 03 SUCCESS: Memory Loopback synchronized.")
            results["03"] = "PASS"
        else:
            print("TEST 03 FAILED: Memory stale.")
            results["03"] = "FAIL"
    else:
        print(f"TEST 03 FAILED: {stderr}")
        results["03"] = "FAIL"

    # Gating Check
    if results.get("03") == "FAIL":
        print("!!! CRITICAL FAILURE: TEST 03 FAIL. Intelligence 'Amnesia' risk detected. ABORTING 1 AM INGEST.")
        return results

    # TEST 02: Nightly Snapshot
    stdout, stderr, code = run_test("02", ["python3", os.path.join(SCRIPTS_DIR, "intelligence_cycle.py"), "--mode", "snapshot"])
    if code == 0 and "Snapshot Archival SUCCESS" in stdout:
        print("TEST 02 SUCCESS: System Snapshot archived.")
        results["02"] = "PASS"
    else:
        print(f"TEST 02 FAILED: {stdout} {stderr}")
        results["02"] = "FAIL"

    # TEST 01: Intelligence Ingester
    stdout, stderr, code = run_test("01", ["python3", os.path.join(SCRIPTS_DIR, "jotform_api_ingester.py")])
    if code == 0:
        print("TEST 01 SUCCESS: Intelligence Ingester operational.")
        results["01"] = "PASS"
    else:
        print(f"TEST 01 FAILED: {stderr}")
        results["01"] = "FAIL"

    print("\n--- VALIDATION SUMMARY ---")
    for tid, res in results.items():
        print(f"TEST {tid}: {res}")
    
    return results

if __name__ == "__main__":
    validate()
