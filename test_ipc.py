"""
Test script for Electron IPC communication
"""

import json
import subprocess


def test_ipc_formula_generation():
    """Test IPC communication for formula generation."""
    print("Testing IPC: Formula Generation...")

    test_data = {'symbol': 'alpha', 'name': 'Alpha'}
    result = subprocess.run(
        ['python', 'backend/latex_generator/formula_gen.py', json.dumps(test_data)],
        capture_output=True,
        text=True,
        timeout=5
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ IPC formula generation passed")
            print(f"  Result: {output.get('latex_code')}")
        else:
            print(f"✗ IPC formula generation failed: {output.get('error')}")
    else:
        print(f"✗ IPC formula generation failed with error: {result.stderr}")


def test_ipc_table_generation():
    """Test IPC communication for table generation."""
    print("\nTesting IPC: Table Generation...")

    test_data = {
        'rows': 2,
        'cols': 2,
        'data': [['a', 'b'], ['c', 'd']]
    }
    result = subprocess.run(
        ['python', 'backend/latex_generator/table_gen.py', json.dumps(test_data)],
        capture_output=True,
        text=True,
        timeout=5
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ IPC table generation passed")
            print(f"  Result: {output.get('latex_code')}")
        else:
            print(f"✗ IPC table generation failed: {output.get('error')}")
    else:
        print(f"✗ IPC table generation failed with error: {result.stderr}")


def test_ipc_latex_compilation():
    """Test IPC communication for LaTeX compilation."""
    print("\nTesting IPC: LaTeX Compilation...")

    test_data = {
        'content': r"""
\documentclass{article}
\begin{document}
Test
\end{document}
"""
    }
    result = subprocess.run(
        ['python', 'backend/compiler/tex_compiler.py', json.dumps(test_data)],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ IPC LaTeX compilation passed")
            print(f"  PDF path: {output.get('pdf_path')}")
        else:
            print(f"✗ IPC LaTeX compilation failed: {output.get('error')}")
    else:
        print(f"✗ IPC LaTeX compilation failed with error: {result.stderr}")


def test_ipc_error_handling():
    """Test IPC error handling."""
    print("\nTesting IPC: Error Handling...")

    test_data = {'symbol': 'unknown_symbol', 'name': 'Unknown'}
    result = subprocess.run(
        ['python', 'backend/latex_generator/formula_gen.py', json.dumps(test_data)],
        capture_output=True,
        text=True,
        timeout=5
    )

    if result.returncode != 0:
        output = json.loads(result.stdout)
        if not output.get('success'):
            print(f"✓ IPC error handling passed")
            print(f"  Error message: {output.get('error')}")
        else:
            print("✗ IPC error handling failed")
    else:
        print("✗ IPC error handling failed")


if __name__ == '__main__':
    test_ipc_formula_generation()
    test_ipc_table_generation()
    test_ipc_latex_compilation()
    test_ipc_error_handling()
    print("\nAll IPC tests completed!")