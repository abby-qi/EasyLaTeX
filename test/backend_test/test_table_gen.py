import pytest
from backend.latex_generator.table_gen import TableGenerator


class TestTableGenerator:
    """Test cases for TableGenerator class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.generator = TableGenerator()

    def test_initialization(self):
        """Test that generator is properly initialized."""
        assert self.generator.default_style == 'booktabs'

    def test_generate_simple_table(self):
        """Test generating simple table."""
        table_data = {
            'rows': 3,
            'cols': 3,
            'data': [
                ['a', 'b', 'c'],
                ['d', 'e', 'f'],
                ['g', 'h', 'i']
            ]
        }
        result = self.generator.generate(table_data)
        assert result is not None
        assert r'\begin{tabular}' in result
        assert r'\toprule' in result
        assert r'\midrule' in result
        assert r'\bottomrule' in result

    def test_generate_empty_table(self):
        """Test generating empty table."""
        table_data = {
            'rows': 2,
            'cols': 2,
            'data': [['', ''], ['', '']]
        }
        result = self.generator.generate(table_data)
        assert result is not None