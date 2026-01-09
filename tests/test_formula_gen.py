"""
Test suite for formula generation module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.latex_generator.formula_gen import FormulaGenerator


class TestFormulaGenerator:
    """Test cases for FormulaGenerator class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = FormulaGenerator()

    def test_basic_symbols(self):
        """Test basic symbol generation."""
        test_cases = [
            {'symbol': 'alpha', 'name': 'Alpha', 'params': {}},
            {'symbol': 'beta', 'name': 'Beta', 'params': {}},
            {'symbol': 'pi', 'name': 'Pi', 'params': {}},
            {'symbol': 'infinity', 'name': 'Infinity', 'params': {}},
        ]

        for test in test_cases:
            result = self.generator.generate(test)
            assert result is not None
            assert len(result) > 0

    def test_integral_with_limits(self):
        """Test integral with lower and upper limits."""
        test_data = {
            'symbol': 'integral',
            'name': 'Integral',
            'params': {'lower': '0', 'upper': '\\infty'}
        }

        result = self.generator.generate(test_data)
        assert '\\int_' in result
        assert '{0}' in result
        assert '{\\infty}' in result

    def test_fraction(self):
        """Test fraction generation."""
        test_data = {
            'symbol': 'fraction',
            'name': 'Fraction',
            'params': {'numerator': 'a', 'denominator': 'b'}
        }

        result = self.generator.generate(test_data)
        assert result == r'\frac{a}{b}'

    def test_sqrt(self):
        """Test square root generation."""
        test_data = {
            'symbol': 'sqrt',
            'name': 'Square Root',
            'params': {'content': 'x^2 + 1'}
        }

        result = self.generator.generate(test_data)
        assert result == r'\sqrt{x^2 + 1}'

    def test_matrix(self):
        """Test matrix generation."""
        test_data = {
            'symbol': 'matrix',
            'name': 'Matrix',
            'params': {
                'rows': 2,
                'cols': 2,
                'data': [['a', 'b'], ['c', 'd']]
            }
        }

        result = self.generator.generate(test_data)
        assert r'\begin{matrix}' in result
        assert r'\end{matrix}' in result
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result
        assert 'd' in result

    def test_unknown_symbol(self):
        """Test unknown symbol raises error."""
        test_data = {
            'symbol': 'unknown_symbol',
            'name': 'Unknown',
            'params': {}
        }

        with pytest.raises(ValueError):
            self.generator.generate(test_data)

    def test_add_custom_symbol(self):
        """Test adding custom symbol mapping."""
        self.generator.add_symbol('custom', r'\custom{}')
        test_data = {
            'symbol': 'custom',
            'name': 'Custom',
            'params': {}
        }

        result = self.generator.generate(test_data)
        assert result == r'\custom{}'

    def test_integral_without_limits(self):
        """Test integral without limits."""
        test_data = {
            'symbol': 'integral',
            'name': 'Integral',
            'params': {}
        }

        result = self.generator.generate(test_data)
        assert '\\int' in result

    def test_summation(self):
        """Test summation generation."""
        test_data = {
            'symbol': 'summation',
            'name': 'Summation',
            'params': {'lower': 'i=0', 'upper': 'n'}
        }

        result = self.generator.generate(test_data)
        assert '\\sum_' in result
        assert '{i=0}' in result
        assert '{n}' in result