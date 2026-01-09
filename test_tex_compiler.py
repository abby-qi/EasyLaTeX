"""
Test script for LaTeX compilation
"""

import json
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.compiler.tex_compiler import TeXCompiler


def test_compiler_initialization():
    """Test compiler initialization."""
    print("Testing compiler initialization...")
    compiler = TeXCompiler()
    print(f"✓ Compiler initialized with: {compiler.compiler}")


def test_command_generation():
    """Test compiler command generation."""
    print("\nTesting compiler command generation...")
    compiler = TeXCompiler()

    test_tex_file = "test.tex"
    test_output_dir = "/tmp"

    cmd = compiler._get_compiler_command(test_tex_file, test_output_dir)
    print(f"✓ Generated command: {' '.join(cmd)}")

    expected_parts = ['pdflatex', '-interaction=nonstopmode', '-file-line-error', test_tex_file]
    all_present = all(part in cmd for part in expected_parts)
    if all_present:
        print("✓ Command contains all expected parts")
    else:
        print("✗ Command missing expected parts")


def test_error_parsing():
    """Test error log parsing."""
    print("\nTesting error log parsing...")
    compiler = TeXCompiler()

    test_cases = [
        {
            'name': 'File not found error',
            'log': "! File `test.tex' not found",
            'expected': '找不到文件'
        },
        {
            'name': 'Undefined control sequence',
            'log': "! Undefined control sequence \\test",
            'expected': '使用了未定义的LaTeX命令'
        },
        {
            'name': 'Missing $ error',
            'log': "! Missing $ inserted",
            'expected': '数学公式格式错误'
        },
    ]

    for test in test_cases:
        result = compiler._parse_error_log(test['log'])
        status = "✓" if test['expected'] in result else "✗"
        print(f"{status} {test['name']}")
        if test['expected'] not in result:
            print(f"  Expected: {test['expected']}")
            print(f"  Got: {result}")


def test_simple_latex_compilation():
    """Test simple LaTeX compilation (if pdflatex is available)."""
    print("\nTesting simple LaTeX compilation...")

    simple_latex = r"""
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
        f.write(simple_latex)
        tex_file_path = f.name

    compiler = TeXCompiler()
    success, pdf_path, error_log = compiler.compile(tex_file_path)

    os.unlink(tex_file_path)

    if success:
        print(f"✓ Compilation successful: {pdf_path}")
    else:
        print(f"✗ Compilation failed: {error_log}")
        print("  (This is expected if pdflatex is not installed)")


def test_command_line():
    """Test command line interface."""
    import subprocess

    test_data = {
        'content': r"""
\documentclass{article}
\begin{document}
Test
\end{document}
"""
    }
    print("\nTesting command line interface...")

    result = subprocess.run(
        ['python', 'backend/compiler/tex_compiler.py', json.dumps(test_data)],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        output = json.loads(result.stdout)
        if output.get('success'):
            print(f"✓ CLI test passed")
            print(f"  PDF path: {output.get('pdf_path')}")
        else:
            print(f"✗ CLI test failed: {output.get('error')}")
    else:
        print(f"✗ CLI test failed with error: {result.stderr}")


if __name__ == '__main__':
    test_compiler_initialization()
    test_command_generation()
    test_error_parsing()
    test_simple_latex_compilation()
    test_command_line()
    print("\nAll tests completed!")