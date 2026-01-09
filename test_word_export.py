"""
Test script for Word export
"""

import json
import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.exporter.word_exporter import WordExporter


def test_simple_text_export():
    """Test simple text export."""
    print("Testing simple text export...")
    exporter = WordExporter()

    test_data = {
        'content': 'Hello, World!\nThis is a test document.'
    }

    success, error = exporter.export(test_data, 'test_output.docx')

    if success:
        print("✓ Simple text export passed")
        print(f"  Created: test_output.docx")
    else:
        print(f"✗ Simple text export failed: {error}")


def test_table_export():
    """Test table export."""
    print("\nTesting table export...")
    exporter = WordExporter()

    test_data = {
        'content': r"""
Here is a table:

\begin{tabular}{ll}
\toprule
a & b \\
\midrule
c & d \\
\bottomrule
\end{tabular}

End of table.
"""
    }

    success, error = exporter.export(test_data, 'test_table.docx')

    if success:
        print("✓ Table export passed")
        print(f"  Created: test_table.docx")
    else:
        print(f"✗ Table export failed: {error}")


def test_mixed_content_export():
    """Test mixed content export."""
    print("\nTesting mixed content export...")
    exporter = WordExporter()

    test_data = {
        'content': r"""
Title: Test Document

Section 1: Introduction

This is the first section.

Section 2: Data

\begin{tabular}{lc}
\toprule
Item & Value \\
\midrule
A & 100 \\
B & 200 \\
\bottomrule
\end{tabular}

Conclusion: Test completed.
"""
    }

    success, error = exporter.export(test_data, 'test_mixed.docx')

    if success:
        print("✓ Mixed content export passed")
        print(f"  Created: test_mixed.docx")
    else:
        print(f"✗ Mixed content export failed: {error}")


def test_command_line():
    """Test command line interface."""
    print("\nTesting command line interface...")

    test_data = {
        'content': 'Test content for CLI.'
    }

    result = subprocess.run(
        ['python', 'backend/exporter/word_exporter.py', json.dumps(test_data), 'test_cli.docx'],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ CLI test passed")
            print(f"  Message: {output.get('message')}")
        else:
            print(f"✗ CLI test failed: {output.get('error')}")
    else:
        print(f"✗ CLI test failed with error: {result.stderr}")


if __name__ == '__main__':
    test_simple_text_export()
    test_table_export()
    test_mixed_content_export()
    test_command_line()
    print("\nAll tests completed!")