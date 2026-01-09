"""
Test script for formula generation
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.latex_generator.formula_gen import FormulaGenerator


def test_basic_symbols():
    """Test basic symbol generation."""
    generator = FormulaGenerator()

    test_cases = [
        {
            'name': 'Alpha symbol',
            'input': {'symbol': 'alpha', 'name': 'Alpha'},
            'expected': r'\alpha'
        },
        {
            'name': 'Pi symbol',
            'input': {'symbol': 'pi', 'name': 'Pi'},
            'expected': r'\pi'
        },
        {
            'name': 'Infinity symbol',
            'input': {'symbol': 'infinity', 'name': 'Infinity'},
            'expected': r'\infty'
        },
    ]

    print("Testing basic symbols...")
    for test in test_cases:
        result = generator.generate(test['input'])
        status = "✓" if result == test['expected'] else "✗"
        print(f"{status} {test['name']}: {result}")
        if result != test['expected']:
            print(f"  Expected: {test['expected']}")
            print(f"  Got: {result}")


def test_complex_formulas():
    """Test complex formula generation."""
    generator = FormulaGenerator()

    test_cases = [
        {
            'name': 'Integral with limits',
            'input': {
                'symbol': 'integral',
                'name': 'Integral',
                'params': {'lower': '0', 'upper': '\\infty'}
            },
            'expected': r'\int_{0}^{\infty}'
        },
        {
            'name': 'Square root',
            'input': {
                'symbol': 'sqrt',
                'name': 'Square Root',
                'params': {'content': 'x^2 + 1'}
            },
            'expected': r'\sqrt{x^2 + 1}'
        },
        {
            'name': 'Fraction',
            'input': {
                'symbol': 'fraction',
                'name': 'Fraction',
                'params': {'numerator': 'a', 'denominator': 'b'}
            },
            'expected': r'\frac{a}{b}'
        },
    ]

    print("\nTesting complex formulas...")
    for test in test_cases:
        result = generator.generate(test['input'])
        status = "✓" if result == test['expected'] else "✗"
        print(f"{status} {test['name']}: {result}")
        if result != test['expected']:
            print(f"  Expected: {test['expected']}")
            print(f"  Got: {result}")


def test_matrix():
    """Test matrix generation."""
    generator = FormulaGenerator()

    test_cases = [
        {
            'name': '2x2 Matrix',
            'input': {
                'symbol': 'matrix',
                'name': 'Matrix',
                'params': {
                    'rows': 2,
                    'cols': 2,
                    'data': [['a', 'b'], ['c', 'd']]
                }
            },
            'expected_contains': r'\begin{matrix}'
        },
    ]

    print("\nTesting matrix...")
    for test in test_cases:
        result = generator.generate(test['input'])
        status = "✓" if test['expected_contains'] in result else "✗"
        print(f"{status} {test['name']}")
        print(f"  Result: {result}")


def test_command_line():
    """Test command line interface."""
    import subprocess

    test_data = {'symbol': 'alpha', 'name': 'Alpha'}
    print("\nTesting command line interface...")

    result = subprocess.run(
        ['python', 'backend/latex_generator/formula_gen.py', json.dumps(test_data)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ CLI test passed: {output.get('latex_code')}")
        else:
            print(f"✗ CLI test failed: {output.get('error')}")
    else:
        print(f"✗ CLI test failed with error: {result.stderr}")


if __name__ == '__main__':
    test_basic_symbols()
    test_complex_formulas()
    test_matrix()
    test_command_line()
    print("\nAll tests completed!")