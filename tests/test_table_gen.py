"""
Test suite for table generation module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.latex_generator.table_gen import TableGenerator


class TestTableGenerator:
    """Test cases for TableGenerator class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = TableGenerator()

    def test_simple_table(self):
        """Test simple table generation."""
        test_data = {
            'rows': 2,
            'cols': 2,
            'data': [['a', 'b'], ['c', 'd']]
        }

        result = self.generator.generate(test_data)
        assert r'\begin{tabular}' in result
        assert r'\toprule' in result
        assert r'\midrule' in result
        assert r'\bottomrule' in result
        assert r'\end{tabular}' in result

    def test_empty_table(self):
        """Test empty table generation."""
        test_data = {
            'rows': 2,
            'cols': 2,
            'data': [['', ''], ['', '']]
        }

        result = self.generator.generate(test_data)
        assert r'\begin{tabular}' in result
        assert r'\end{tabular}' in result

    def test_large_table(self):
        """Test large table generation."""
        test_data = {
            'rows': 5,
            'cols': 5,
            'data': [[f'{i}{j}' for j in range(5)] for i in range(5)]
        }

        result = self.generator.generate(test_data)
        assert result.count('&') == 25
        assert result.count(r'\\') == 5

    def test_default_dimensions(self):
        """Test table with default dimensions."""
        test_data = {
            'rows': 3,
            'cols': 3,
            'data': []
        }

        result = self.generator.generate(test_data)
        assert r'\begin{tabular}{lll}' in result

    def test_single_row(self):
        """Test table with single row."""
        test_data = {
            'rows': 1,
            'cols': 3,
            'data': [['a', 'b', 'c']]
        }

        result = self.generator.generate(test_data)
        assert r'\toprule' in result
        assert r'\bottomrule' in result
        assert r'\midrule' not in result

    def test_single_column(self):
        """Test table with single column."""
        test_data = {
            'rows': 3,
            'cols': 1,
            'data': [['a'], ['b'], ['c']]
        }

        result = self.generator.generate(test_data)
        assert r'\begin{tabular}{l}' in result

    def test_generate_header(self):
        """Test header generation."""
        generator = TableGenerator()
        result = generator._generate_header(3)
        assert result == 'lll'

    def test_generate_midrule(self):
        """Test midrule generation."""
        generator = TableGenerator()
        result = generator._generate_midrule()
        assert result == r'\midrule'

    def test_generate_bottomrule(self):
        """Test bottomrule generation."""
        generator = TableGenerator()
        result = generator._generate_bottomrule()
        assert result == r'\bottomrule'