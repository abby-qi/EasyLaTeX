"""
Test suite for data conversion module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.utils.data_converter import DataConverter


class TestDataConverter:
    """Test cases for DataConverter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.converter = DataConverter()

    def test_json_to_latex_simple(self):
        """Test simple JSON to LaTeX conversion."""
        json_data = {
            'title': 'Test Document',
            'author': 'Test Author',
            'content': [
                {'type': 'text', 'content': 'Hello, World!'},
                {'type': 'section', 'content': 'Introduction'},
                {'type': 'text', 'content': 'This is a test.'}
            ]
        }

        result = self.converter.json_to_latex(json_data)
        assert r'\documentclass' in result
        assert r'\title{Test Document}' in result
        assert r'\author{Test Author}' in result
        assert 'Hello, World!' in result
        assert r'\section{Introduction}' in result

    def test_json_to_latex_with_formula(self):
        """Test JSON with formula to LaTeX conversion."""
        json_data = {
            'title': 'Math Test',
            'content': [
                {'type': 'text', 'content': 'The formula is:'},
                {'type': 'formula', 'content': r'\int_{0}^{\infty} e^{-x^2} dx'}
            ]
        }

        result = self.converter.json_to_latex(json_data)
        assert r'\int_{0}^{\infty}' in result

    def test_json_to_latex_with_table(self):
        """Test JSON with table to LaTeX conversion."""
        json_data = {
            'title': 'Table Test',
            'content': [
                {'type': 'text', 'content': 'Here is a table:'},
                {'type': 'table', 'content': r'\begin{tabular}{ll}\toprule a & b \\ \midrule c & d \\ \bottomrule\end{tabular}'}
            ]
        }

        result = self.converter.json_to_latex(json_data)
        assert r'\begin{tabular}' in result

    def test_json_to_latex_empty_content(self):
        """Test JSON with empty content to LaTeX conversion."""
        json_data = {
            'title': 'Empty Test',
            'content': []
        }

        result = self.converter.json_to_latex(json_data)
        assert r'\begin{document}' in result
        assert r'\end{document}' in result

    def test_latex_to_json_simple(self):
        """Test simple LaTeX to JSON conversion."""
        latex_code = r"""
\documentclass{article}
\title{Test}
\author{Author}
\begin{document}
Hello, World!
\section{Introduction}
This is a test.
\end{document}
"""

        result = self.converter.latex_to_json(latex_code)
        assert result['title'] == 'Test'
        assert result['author'] == 'Author'
        assert len(result['content']) > 0

    def test_validate_json_valid(self):
        """Test validation of valid JSON."""
        json_data = {
            'title': 'Valid Document',
            'content': []
        }

        valid, error = self.converter.validate_json(json_data)
        assert valid is True
        assert error == ''

    def test_validate_json_invalid_content_type(self):
        """Test validation of invalid JSON content type."""
        json_data = {
            'title': 'Test',
            'content': 'invalid'
        }

        valid, error = self.converter.validate_json(json_data)
        assert valid is False

    def test_validate_json_missing_title(self):
        """Test validation of JSON missing title."""
        json_data = {
            'content': []
        }

        valid, error = self.converter.validate_json(json_data)
        assert valid is False

    def test_round_trip_conversion(self):
        """Test round-trip conversion (JSON -> LaTeX -> JSON)."""
        original_json = {
            'title': 'Round Trip Test',
            'author': 'Test Author',
            'content': [
                {'type': 'text', 'content': 'Test content'},
                {'type': 'section', 'content': 'Test Section'}
            ]
        }

        latex_code = self.converter.json_to_latex(original_json)
        reconstructed_json = self.converter.latex_to_json(latex_code)

        assert original_json['title'] == reconstructed_json['title']
        assert original_json['author'] == reconstructed_json['author']

    def test_json_string_input(self):
        """Test JSON string input."""
        json_string = '{"title": "Test", "content": []}'

        result = self.converter.json_to_latex(json_string)
        assert r'\documentclass' in result

    def test_invalid_json_string(self):
        """Test invalid JSON string input."""
        json_string = '{invalid json}'

        with pytest.raises(ValueError):
            self.converter.json_to_latex(json_string)