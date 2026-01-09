"""
Test script for data conversion
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.utils.data_converter import DataConverter


def test_json_to_latex():
    """Test JSON to LaTeX conversion."""
    print("Testing JSON to LaTeX conversion...")
    converter = DataConverter()

    test_cases = [
        {
            'name': 'Simple document',
            'input': {
                'title': 'Test Document',
                'author': 'Test Author',
                'content': [
                    {'type': 'text', 'content': 'Hello, World!'},
                    {'type': 'section', 'content': 'Introduction'},
                    {'type': 'text', 'content': 'This is a test.'}
                ]
            },
            'expected_contains': ['\\documentclass', '\\begin{document}', 'Hello, World!', '\\section{Introduction}']
        },
        {
            'name': 'Document with formula',
            'input': {
                'title': 'Math Test',
                'content': [
                    {'type': 'text', 'content': 'The formula is:'},
                    {'type': 'formula', 'content': r'\int_{0}^{\infty} e^{-x^2} dx'}
                ]
            },
            'expected_contains': [r'\int_{0}^{\infty}']
        },
        {
            'name': 'Document with table',
            'input': {
                'title': 'Table Test',
                'content': [
                    {'type': 'text', 'content': 'Here is a table:'},
                    {'type': 'table', 'content': r'\begin{tabular}{ll}\toprule a & b \\ \midrule c & d \\ \bottomrule\end{tabular}'}
                ]
            },
            'expected_contains': [r'\begin{tabular}', r'\toprule', r'\midrule', r'\bottomrule']
        },
    ]

    for test in test_cases:
        try:
            result = converter.json_to_latex(test['input'])
            all_contained = all(expected in result for expected in test['expected_contains'])
            status = "✓" if all_contained else "✗"
            print(f"{status} {test['name']}")
            if not all_contained:
                print(f"  Missing: {[e for e in test['expected_contains'] if e not in result]}")
        except Exception as e:
            print(f"✗ {test['name']}: {e}")


def test_latex_to_json():
    """Test LaTeX to JSON conversion."""
    print("\nTesting LaTeX to JSON conversion...")
    converter = DataConverter()

    test_cases = [
        {
            'name': 'Simple LaTeX',
            'input': r"""
\documentclass{article}
\title{Test}
\author{Author}
\begin{document}
Hello, World!
\section{Introduction}
This is a test.
\end{document}
""",
            'expected_title': 'Test',
            'expected_author': 'Author'
        },
    ]

    for test in test_cases:
        try:
            result = converter.latex_to_json(test['input'])
            title_match = result.get('title') == test['expected_title']
            author_match = result.get('author') == test['expected_author']
            status = "✓" if title_match and author_match else "✗"
            print(f"{status} {test['name']}")
            if not title_match:
                print(f"  Expected title: {test['expected_title']}, Got: {result.get('title')}")
            if not author_match:
                print(f"  Expected author: {test['expected_author']}, Got: {result.get('author')}")
        except Exception as e:
            print(f"✗ {test['name']}: {e}")


def test_validate_json():
    """Test JSON validation."""
    print("\nTesting JSON validation...")
    converter = DataConverter()

    test_cases = [
        {
            'name': 'Valid JSON',
            'input': {
                'title': 'Valid Document',
                'content': []
            },
            'expected_valid': True
        },
        {
            'name': 'Invalid JSON (missing title)',
            'input': {
                'content': []
            },
            'expected_valid': False
        },
        {
            'name': 'Invalid JSON (invalid content type)',
            'input': {
                'title': 'Test',
                'content': 'invalid'
            },
            'expected_valid': False
        },
    ]

    for test in test_cases:
        try:
            valid, error = converter.validate_json(test['input'])
            status = "✓" if valid == test['expected_valid'] else "✗"
            print(f"{status} {test['name']}")
            if valid != test['expected_valid']:
                print(f"  Expected valid: {test['expected_valid']}, Got: {valid}")
                if error:
                    print(f"  Error: {error}")
        except Exception as e:
            print(f"✗ {test['name']}: {e}")


def test_round_trip():
    """Test round-trip conversion (JSON -> LaTeX -> JSON)."""
    print("\nTesting round-trip conversion...")
    converter = DataConverter()

    original_json = {
        'title': 'Round Trip Test',
        'author': 'Test Author',
        'content': [
            {'type': 'text', 'content': 'Test content'},
            {'type': 'section', 'content': 'Test Section'}
        ]
    }

    try:
        latex_code = converter.json_to_latex(original_json)
        reconstructed_json = converter.latex_to_json(latex_code)

        title_match = original_json.get('title') == reconstructed_json.get('title')
        author_match = original_json.get('author') == reconstructed_json.get('author')

        status = "✓" if title_match and author_match else "✗"
        print(f"{status} Round-trip conversion")
        if not title_match:
            print(f"  Title mismatch: {original_json.get('title')} != {reconstructed_json.get('title')}")
        if not author_match:
            print(f"  Author mismatch: {original_json.get('author')} != {reconstructed_json.get('author')}")
    except Exception as e:
        print(f"✗ Round-trip conversion: {e}")


if __name__ == '__main__':
    test_json_to_latex()
    test_latex_to_json()
    test_validate_json()
    test_round_trip()
    print("\nAll data conversion tests completed!")