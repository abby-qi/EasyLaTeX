import pytest
from backend.latex_generator.formula_gen import FormulaGenerator


class TestFormulaGenerator:
    """Test cases for FormulaGenerator class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = FormulaGenerator()

    def test_symbol_map_initialization(self):
        """Test that symbol map is properly initialized."""
        assert 'integral' in self.generator.symbol_map
        assert 'alpha' in self.generator.symbol_map
        assert 'matrix' in self.generator.symbol_map

    def test_add_symbol(self):
        """Test adding custom symbol mapping."""
        self.generator.add_symbol('custom', r'\custom')
        assert 'custom' in self.generator.symbol_map
        assert self.generator.symbol_map['custom'] == r'\custom'

    def test_generate_basic_formula(self):
        """Test generating basic formula."""
        formula_data = {'symbol': 'alpha', 'name': 'Alpha'}
        result = self.generator.generate(formula_data)
        assert result is not None

    def test_generate_complex_formula(self):
        """Test generating complex formula."""
        formula_data = {'symbol': 'integral', 'name': 'Integral'}
        result = self.generator.generate(formula_data)
        assert result is not None
        assert r'\int' in result