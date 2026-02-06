#!/usr/bin/env python3
"""
Quick test of citation checker functionality
Run: python test_example.py
"""

import subprocess
import sys

# Test cases
test_cases = [
    {
        "name": "Valid citation format detection",
        "text": "According to Richardson et al. (2023), Earth has crossed 6 of 9 planetary boundaries.",
        "expect_citations": 1
    },
    {
        "name": "Multiple citation formats",
        "text": """
        Smith (2024) found significant results.
        This was confirmed by Jones et al. (2023).
        Earlier work (Wilson & Chen, 2022) suggested similar findings.
        """,
        "expect_citations": 3
    },
    {
        "name": "No citations",
        "text": "This is just regular text without any academic references.",
        "expect_citations": 0
    }
]

def run_test(test_case):
    """Run a single test case"""
    print(f"\n{'='*60}")
    print(f"Test: {test_case['name']}")
    print(f"{'='*60}")

    # Run citation checker
    result = subprocess.run(
        ["python3", "citationChecker.py", "--text", test_case['text'], "--json"],
        capture_output=True,
        text=True
    )

    if result.returncode not in [0, 1]:
        print(f"❌ FAILED: Unexpected return code {result.returncode}")
        print(f"Error: {result.stderr}")
        return False

    # Parse JSON output
    import json
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"❌ FAILED: Invalid JSON output")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        return False

    # Check citation count
    found = output['citations_found']
    expected = test_case['expect_citations']

    if found == expected:
        print(f"✅ PASSED: Found {found} citation(s) as expected")
        if found > 0:
            print(f"\nDetected citations:")
            for i, citation in enumerate(output['results'], 1):
                print(f"  {i}. {citation['original_text']} → {citation['status']}")
        return True
    else:
        print(f"❌ FAILED: Expected {expected} citations, found {found}")
        return False

def main():
    print("Citation Checker Test Suite")
    print("="*60)

    passed = 0
    failed = 0

    for test_case in test_cases:
        if run_test(test_case):
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")

    if failed == 0:
        print(f"\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {failed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
