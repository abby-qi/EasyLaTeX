"""
Test suite for exporters
"""

import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.exporter.word_exporter import WordExporter
from backend.exporter.tex_exporter import TexExporter


class TestWordExporter:
    """Test cases for WordExporter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.exporter = WordExporter()

    def test_export_simple_text(self):
        """Test simple text export."""
        test_data = {
            'content': 'Hello, World!'
        }

        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
            output_path = f.name

        success, error = self.exporter.export(test_data, output_path)

        assert success is True
        assert error == ''
        assert os.path.exists(output_path)

        os.unlink(output_path)

    def test_export_with_table(self):
        """Test export with table."""
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
"""
        }

        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
            output_path = f.name

        success, error = self.exporter.export(test_data, output_path)

        assert success is True
        assert error == ''

        os.unlink(output_path)


class TestTexExporter:
    """Test cases for TexExporter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.exporter = TexExporter()

    def test_export_simple_text(self):
        """Test simple text export."""
        test_data = {
            'content': r'\documentclass{article}\begin{document}Hello\end{document}'
        }

        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as f:
            output_path = f.name

        success, error = self.exporter.export(test_data, output_path)

        assert success is True
        assert error == ''
        assert os.path.exists(output_path)

        os.unlink(output_path)

    def test_export_empty_content(self):
        """Test export with empty content."""
        test_data = {
            'content': ''
        }

        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as f:
            output_path = f.name

        success, error = self.exporter.export(test_data, output_path)

        assert success is True
        assert error == ''

        os.unlink(output_path)

    def test_export_invalid_path(self):
        """Test export with invalid path."""
        test_data = {
            'content': 'Test'
        }

        success, error = self.exporter.export(test_data, '/invalid/path/test.tex')

        assert success is False
        assert error is not None