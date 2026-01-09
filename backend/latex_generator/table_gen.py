"""
Table Generator
Converts table data to LaTeX three-line table (booktabs) code.
"""

import sys
import json


class TableGenerator:
    """Generates LaTeX booktabs table code from table data."""

    def __init__(self):
        self.default_style = 'booktabs'

    def generate(self, table_data):
        """
        Generate LaTeX code from table data.

        Args:
            table_data: Dictionary containing rows, columns, and content

        Returns:
            str: LaTeX table code
        """
        rows = table_data.get('rows', 3)
        cols = table_data.get('cols', 3)
        data = table_data.get('data', [[''] * cols for _ in range(rows)])

        column_spec = 'l' * cols
        table_lines = []

        table_lines.append(r'\begin{tabular}{' + column_spec + '}')
        table_lines.append(r'\toprule')

        for i, row in enumerate(data):
            table_lines.append(' & '.join(row) + r' \\')
            if i == 0:
                table_lines.append(r'\midrule')

        table_lines.append(r'\bottomrule')
        table_lines.append(r'\end{tabular}')

        return '\n'.join(table_lines)

    def _generate_header(self, num_columns):
        """Generate table header line."""
        return 'l' * num_columns

    def _generate_midrule(self):
        """Generate midrule for booktabs style."""
        return r'\midrule'

    def _generate_bottomrule(self):
        """Generate bottom rule for booktabs style."""
        return r'\bottomrule'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            table_data = json.loads(sys.argv[1])
            generator = TableGenerator()
            latex_code = generator.generate(table_data)
            print(json.dumps({
                'success': True,
                'latex_code': latex_code
            }))
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))