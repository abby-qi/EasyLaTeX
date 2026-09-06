"""
latex_generator - LaTeX 代码生成模块

提供公式生成 (formula_gen) 与三线表生成 (table_gen) 两个子模块，
由 Electron 主进程通过 IPC 以子进程方式调用。
"""

from .formula_gen import generate_formula, generate_symbol, SYMBOL_MAP
from .table_gen import generate_table

__all__ = ['generate_formula', 'generate_symbol', 'generate_table', 'SYMBOL_MAP']
