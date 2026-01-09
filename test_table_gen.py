"""
Test script for table generation
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.latex_generator.table_gen import TableGenerator


def test_simple_table():
    """Test simple table generation."""
    generator = TableGenerator()

    test_cases = [
        {
            'name': '2x2 Table',
            'input': {
                'rows': 2,
                'cols': 2,
                'data': [['a', 'b'], ['c', 'd']]
            },
            'expected_contains': [r'\begin{tabular}{ll}', r'\toprule', r'\midrule', r'\bottomrule']
        },
        {
            'name': '3x3 Table',
            'input': {
                'rows': 3,
                'cols': 3,
                'data': [
                    ['1', '2', '3'],
                    ['4', '5', '6'],
                    ['7', '8', '9']
                ]
            },
            'expected_contains': [r'\begin{tabular}{lll}', r'\toprule', r'\midrule', r'\bottomrule']
        },
    ]

    print("Testing simple tables...")
    for test in test_cases:
        result = generator.generate(test['input'])
        all_contained = all(expected in result for expected in test['expected_contains'])
        status = "✓" if all_contained else "✗"
        print(f"{status} {test['name']}")
        if not all_contained:
            print(f"  Result:\n{result}")
            print(f"  Expected to contain: {test['expected_contains']}")


def test_empty_table():
    """Test empty table generation."""
    generator = TableGenerator()

    test_cases = [
        {
            'name': 'Empty 2x2 Table',
            'input': {
                'rows': 2,
                'cols': 2,
                'data': [['', ''], ['', '']]
            },
            'expected_contains': [r'\begin{tabular}{ll}', r'\toprule', r'\midrule', r'\bottomrule']
        },
    ]

    print("\nTesting empty tables...")
    for test in test_cases:
        result = generator.generate(test['input'])
        all_contained = all(expected in result for expected in test['expected_contains'])
        status = "✓" if all_contained else "✗"
        print(f"{status} {test['name']}")
        if not all_contained:
            print(f"  Result:\n{result}")


def test_command_line():
    """Test command line interface."""
    import subprocess

    test_data = {
        'rows': 2,
        'cols': 2,
        'data': [['a', 'b'], ['c', 'd']]
    }
    print("\nTesting command line interface...")

    result = subprocess.run(
        ['python', 'backend/latex_generator/table_gen.py', json.dumps(test_data)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ CLI test passed")
            print(f"  Generated LaTeX:\n{output.get('latex_code')}")
        else:
            print(f"✗ CLI test failed: {output.get('error')}")
    else:
        print(f"✗ CLI test failed with error: {result.stderr}")


def test_table_structure():
    """Test table structure correctness."""
    generator = TableGenerator()

    test_data = {
        'rows': 3,
        'cols': 3,
        'data': [
            ['Header1', 'Header2', 'Header3'],
            ['Data1', 'Data2', 'Data3'],
            ['Data4', 'Data5', 'Data6']
        ]
    }

    print("\nTesting table structure...")
    result = generator.generate(test_data)

    lines = result.split('\n')
    has_toprule = r'\toprule' in result
    has_midrule = r'\midrule' in result
    has_bottomrule = r'\bottomrule' in result
    has_tabular_start = r'\begin{tabular}' in result
    has_tabular_end = r'\end{tabular}' in result

    checks = [
        ('Top rule', has_toprule),
        ('Mid rule', has_midrule),
        ('Bottom rule', has_bottomrule),
        ('Tabular start', has_tabular_start),
        ('Tabular end', has_tabular_end)
    ]

    all_passed = all(check[1] for check in checks)
    for name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {name}")

    if all_passed:
        print("✓ All structure checks passed!")
    else:
        print("Result:")
        print(result)


if __name__ == '__main__':
    test_simple_table()
    test_empty_table()
    test_table_structure()
    test_command_line()
    print("\nAll tests completed!")