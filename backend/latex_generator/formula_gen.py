"""
Formula Generator
Converts mathematical formulas to LaTeX code.
"""

import sys
import json


class FormulaGenerator:
    """Generates LaTeX code from formula symbols and structures."""

    def __init__(self):
        self.symbol_map = {
            'integral': r'\int_{}^{}',
            'summation': r'\sum_{}^{}',
            'product': r'\prod_{}^{}',
            'matrix': r'\begin{matrix} \end{matrix}',
            'alpha': r'\alpha',
            'beta': r'\beta',
            'gamma': r'\gamma',
            'delta': r'\delta',
            'epsilon': r'\epsilon',
            'pi': r'\pi',
            'theta': r'\theta',
            'lambda': r'\lambda',
            'mu': r'\mu',
            'sigma': r'\sigma',
            'phi': r'\phi',
            'omega': r'\omega',
            'infinity': r'\infty',
            'partial': r'\partial',
            'nabla': r'\nabla',
            'sqrt': r'\sqrt{}',
            'fraction': r'\frac{}{}',
        }

    def generate(self, formula_data):
        """
        Generate LaTeX code from formula data.

        Args:
            formula_data: Dictionary containing formula structure

        Returns:
            str: LaTeX code
        """
        symbol = formula_data.get('symbol', '')
        params = formula_data.get('params', {})

        if symbol not in self.symbol_map:
            raise ValueError(f"Unknown symbol: {symbol}")

        latex_code = self.symbol_map[symbol]

        if symbol in ['integral', 'summation', 'product']:
            lower = params.get('lower', '')
            upper = params.get('upper', '')
            latex_code = latex_code.replace('{}', '', 1).replace('{}', '')
            if lower:
                latex_code = latex_code.replace('_', f'_{{{lower}}}', 1)
            if upper:
                latex_code = latex_code.replace('^', f'^{{{upper}}}', 1)

        elif symbol in ['sqrt', 'fraction']:
            if symbol == 'fraction':
                numerator = params.get('numerator', '')
                denominator = params.get('denominator', '')
                latex_code = r'\frac{' + numerator + '}{' + denominator + '}'
            else:
                content = params.get('content', '')
                latex_code = r'\sqrt{' + content + '}'

        elif symbol == 'matrix':
            rows = params.get('rows', 2)
            cols = params.get('cols', 2)
            data = params.get('data', [[''] * cols for _ in range(rows)])
            matrix_content = ' \\\\\n'.join([' & '.join(row) for row in data])
            latex_code = r'\begin{matrix}' + matrix_content + r'\end{matrix}'

        return latex_code

    def add_symbol(self, symbol, latex_code):
        """Add custom symbol mapping."""
        self.symbol_map[symbol] = latex_code


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            formula_data = json.loads(sys.argv[1])
            generator = FormulaGenerator()
            latex_code = generator.generate(formula_data)
            print(json.dumps({
                'success': True,
                'latex_code': latex_code
            }))
        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))