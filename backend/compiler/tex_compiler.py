"""
TeX Compiler
Compiles LaTeX documents using TinyTeX.
"""

import subprocess
import os


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
        pass

    def _get_compiler_command(self, tex_file_path, output_dir):
        """Generate compiler command."""
        pass

    def _parse_error_log(self, log_content):
        """Parse LaTeX error log and return human-readable messages."""
        pass