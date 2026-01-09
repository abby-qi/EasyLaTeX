"""
TeX Compiler
Compiles LaTeX documents using TinyTeX.
"""

import subprocess
import os
import sys
import json
import tempfile
import re


class TeXCompiler:
    """Handles LaTeX compilation with TinyTeX."""

    def __init__(self, tinytex_path=None):
        self.tinytex_path = tinytex_path
        self.compiler = 'pdflatex'

    def compile(self, tex_file_path, output_dir=None):
        """
        Compile LaTeX file to PDF.

        Args:
            tex_file_path: Path to .tex file
            output_dir: Output directory for PDF

        Returns:
            tuple: (success: bool, pdf_path: str, error_log: str)
        """
        if output_dir is None:
            output_dir = os.path.dirname(tex_file_path)

        tex_filename = os.path.basename(tex_file_path)
        base_name = os.path.splitext(tex_filename)[0]
        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

        try:
            cmd = self._get_compiler_command(tex_file_path, output_dir)
            result = subprocess.run(
                cmd,
                cwd=output_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                if os.path.exists(pdf_path):
                    return (True, pdf_path, '')
                else:
                    return (False, '', 'PDF file was not generated')
            else:
                error_log = self._parse_error_log(result.stderr + result.stdout)
                return (False, '', error_log)

        except subprocess.TimeoutExpired:
            return (False, '', 'Compilation timeout (30s)')
        except Exception as e:
            return (False, '', str(e))

    def _get_compiler_command(self, tex_file_path, output_dir):
        """Generate compiler command."""
        compiler = self.compiler

        if self.tinytex_path:
            compiler = os.path.join(self.tinytex_path, 'bin', 'x86_64-linux', compiler)

        return [compiler, '-interaction=nonstopmode', '-file-line-error', tex_file_path]

    def _parse_error_log(self, log_content):
        """Parse LaTeX error log and return human-readable messages."""
        error_patterns = {
            r'! File `(.+?)\' not found': '找不到文件，请检查路径是否正确',
            r'! Undefined control sequence': '使用了未定义的LaTeX命令',
            r'! Missing \$ inserted': '数学公式格式错误，请检查符号',
            r'! Extra alignment tab': '表格列数不匹配',
            r'! Runaway argument': '参数格式错误',
            r'! LaTeX Error': 'LaTeX编译错误',
        }

        for pattern, message in error_patterns.items():
            match = re.search(pattern, log_content)
            if match:
                return message

        if log_content.strip():
            return f'编译错误: {log_content[:200]}'

        return '未知编译错误'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
            tex_content = data.get('content', '')

            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
                f.write(tex_content)
                tex_file_path = f.name

            compiler = TeXCompiler()
            success, pdf_path, error_log = compiler.compile(tex_file_path)

            os.unlink(tex_file_path)

            if success:
                print(json.dumps({
                    'success': True,
                    'pdf_path': pdf_path
                }))
            else:
                print(json.dumps({
                    'success': False,
                    'error': error_log
                }))

        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))