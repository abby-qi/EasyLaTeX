#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式生成模块 (formula_gen)

将用户在可视化界面上的点击动作翻译成合法的 LaTeX 代码。
由 Electron 主进程以 ``python formula_gen.py '<json>'`` 方式调用，
标准输出一个 JSON 对象 ``{"success": bool, "latex_code": str, ...}``。
"""

import json
import sys

# ---------------------------------------------------------------------------
# 符号映射表：界面按钮 -> LaTeX 命令
# 键采用「语义名」，界面上可以显示成任意 Unicode 字形。
# ---------------------------------------------------------------------------
SYMBOL_MAP = {
    # 基本运算
    'plus': r'+',
    'minus': r'-',
    'times': r'\times',
    'div': r'\div',
    'equal': r'=',
    'neq': r'\neq',
    'less': r'<',
    'greater': r'>',
    'leq': r'\leq',
    'geq': r'\geq',
    'approx': r'\approx',
    'equiv': r'\equiv',
    'pm': r'\pm',
    'cdot': r'\cdot',
    # 希腊字母
    'alpha': r'\alpha',
    'beta': r'\beta',
    'gamma': r'\gamma',
    'delta': r'\delta',
    'epsilon': r'\epsilon',
    'varepsilon': r'\varepsilon',
    'zeta': r'\zeta',
    'eta': r'\eta',
    'theta': r'\theta',
    'vartheta': r'\vartheta',
    'iota': r'\iota',
    'kappa': r'\kappa',
    'lambda': r'\lambda',
    'mu': r'\mu',
    'nu': r'\nu',
    'xi': r'\xi',
    'pi': r'\pi',
    'rho': r'\rho',
    'sigma': r'\sigma',
    'tau': r'\tau',
    'upsilon': r'\upsilon',
    'phi': r'\phi',
    'varphi': r'\varphi',
    'chi': r'\chi',
    'psi': r'\psi',
    'omega': r'\omega',
    # 大写希腊字母
    'Gamma': r'\Gamma',
    'Delta': r'\Delta',
    'Theta': r'\Theta',
    'Lambda': r'\Lambda',
    'Xi': r'\Xi',
    'Pi': r'\Pi',
    'Sigma': r'\Sigma',
    'Phi': r'\Phi',
    'Psi': r'\Psi',
    'Omega': r'\Omega',
    # 关系与逻辑
    'in': r'\in',
    'notin': r'\notin',
    'subset': r'\subset',
    'subseteq': r'\subseteq',
    'cup': r'\cup',
    'cap': r'\cap',
    'forall': r'\forall',
    'exists': r'\exists',
    'neg': r'\neg',
    'land': r'\land',
    'lor': r'\lor',
    'to': r'\to',
    'mapsto': r'\mapsto',
    'implies': r'\implies',
    # 大运算符
    'sum': r'\sum',
    'prod': r'\prod',
    'int': r'\int',
    'iint': r'\iint',
    'oint': r'\oint',
    'lim': r'\lim',
    'infty': r'\infty',
    'partial': r'\partial',
    'nabla': r'\nabla',
    # 函数
    'sin': r'\sin',
    'cos': r'\cos',
    'tan': r'\tan',
    'cot': r'\cot',
    'sec': r'\sec',
    'csc': r'\csc',
    'ln': r'\ln',
    'log': r'\log',
    'exp': r'\exp',
    'max': r'\max',
    'min': r'\min',
    'sup': r'\sup',
    'inf': r'\inf',
    # 其他常用
    'degree': r'^\circ',
    'angle': r'\angle',
    'triangle': r'\triangle',
    'perp': r'\perp',
    'parallel': r'\parallel',
    'vec': r'\vec{}',
    'hat': r'\hat{}',
    'bar': r'\bar{}',
    'dot': r'\dot{}',
    'overrightarrow': r'\overrightarrow{}',
    'ellipsis': r'\ldots',
    'dots': r'\cdots',
    'quad': r'\quad',
}

# 需要花括号参数的一元装饰器，生成时自动补一对空花括号
_DECORATORS = {'vec', 'hat', 'bar', 'dot', 'overrightarrow', 'tilde', 'overline', 'underline'}


def generate_symbol(name, custom_symbols=None):
    """
    根据语义名生成符号的 LaTeX 代码。

    :param name: 符号语义名，如 'alpha'；也允许直接传入已带反斜杠的命令，如 '\\alpha'
    :param custom_symbols: 用户自定义符号表，优先级高于内置表
    :return: LaTeX 代码片段
    :raises KeyError: 符号既不在内置表也不在自定义表时抛出
    """
    if custom_symbols and name in custom_symbols:
        return custom_symbols[name]

    # 允许直接传命令形式，去掉前导反斜杠再查表
    key = name[1:] if isinstance(name, str) and name.startswith('\\') else name

    if key in SYMBOL_MAP:
        return SYMBOL_MAP[key]

    raise KeyError("未知符号: {}".format(name))


def _wrap_group(body):
    """给非空内容加上花括号，空内容原样返回，避免出现 {} 这种无意义占位。"""
    return '' if not body else '{%s}' % body


def generate_formula(formula_type, params=None):
    """
    生成结构化公式（分数、根号、积分、求和、矩阵等）的 LaTeX 代码。

    所有结构都生成「待填写」的占位花括号，方便用户在编辑器里直接补内容：
        fraction -> \\frac{}{}
        integral(带上下限) -> \\int_{}^{}{}

    :param formula_type: 结构类型
    :param params: 结构参数字典
    :return: LaTeX 代码片段
    :raises ValueError: 未知的结构类型
    """
    params = params or {}
    t = (formula_type or '').lower()

    if t in ('fraction', 'frac'):
        return r'\frac{%s}{%s}' % (params.get('numerator', ''), params.get('denominator', ''))

    if t in ('sqrt', 'root'):
        # \sqrt[n]{x}：只有 n 非空时才带可选参数
        index = params.get('index', '')
        return r'\sqrt%s{%s}' % ('[%s]' % index if index else '', params.get('radicand', ''))

    if t in ('subscript', 'sub'):
        return '_{%s}' % params.get('base', '')

    if t in ('superscript', 'sup', 'power'):
        return '^{%s}' % params.get('exponent', '')

    if t in ('subsup',):
        return '_%s^%s' % (_wrap_group(params.get('sub', '')), _wrap_group(params.get('sup', '')))

    if t in ('integral', 'int'):
        lower = params.get('lower', '')
        upper = params.get('upper', '')
        body = params.get('body', '')
        if lower or upper:
            return r'\int_%s^%s %s' % (_wrap_group(lower), _wrap_group(upper), body)
        # 不带上下限 —— 与 README 里承诺的 \int_{}^{} 保持一致
        return r'\int_{%s}^{%s}{%s}' % (lower, upper, body)

    if t in ('sum', 'summation'):
        lower = params.get('lower', '')
        upper = params.get('upper', '')
        body = params.get('body', '')
        if lower or upper:
            return r'\sum_%s^%s %s' % (_wrap_group(lower), _wrap_group(upper), body)
        return r'\sum_{%s}^{%s}{%s}' % (lower, upper, body)

    if t in ('prod', 'product'):
        lower = params.get('lower', '')
        upper = params.get('upper', '')
        return r'\prod_%s^%s %s' % (
            _wrap_group(lower), _wrap_group(upper), params.get('body', ''))

    if t in ('limit', 'lim'):
        return r'\lim_{%s \to %s} %s' % (
            params.get('variable', 'x'),
            params.get('target', ''),
            params.get('body', ''))

    if t in ('matrix',):
        rows = int(params.get('rows', 2) or 2)
        cols = int(params.get('cols', 2) or 2)
        bracket = (params.get('bracket') or '').lower()
        envs = {
            '': 'matrix', 'p': 'pmatrix', 'b': 'bmatrix',
            'B': 'Bmatrix', 'v': 'vmatrix', 'V': 'Vmatrix',
        }
        env = envs.get(bracket, 'matrix')
        lines = []
        for _ in range(rows):
            lines.append('  ' + ' & '.join([''] * cols))
        return '\\begin{%s}\n%s\n\\end{%s}' % (env, r' \\' + '\n'.join(lines), env)

    if t in ('cases',):
        count = int(params.get('rows', 2) or 2)
        lines = '\n'.join(['  %s & %s' % ('', '') for _ in range(count)])
        return '\\begin{cases}\n%s\n\\end{cases}' % lines

    if t in ('abs',):
        return r'\left| %s \right|' % params.get('body', '')

    if t in ('norm',):
        return r'\left\| %s \right\|' % params.get('body', '')

    if t in ('binomial',):
        return r'\binom{%s}{%s}' % (params.get('n', ''), params.get('k', ''))

    # 兜底：当成符号处理，这样前端新增按钮时后端不用同步改
    try:
        return generate_symbol(formula_type, params.get('custom_symbols'))
    except KeyError:
        raise ValueError("未知公式类型: {}".format(formula_type))


def handle(data):
    """
    统一的 CLI / IPC 入口。

    支持的输入形态：
        {"action": "symbol", "name": "alpha"}
        {"action": "formula", "type": "fraction", "params": {...}}
        {"name": "alpha"}                      # 缺省 action=symbol
        {"type": "fraction", "params": {...}}  # 缺省 action=formula
        {"symbols": ["alpha", "beta"]}         # 批量符号
    """
    action = data.get('action')
    custom = data.get('custom_symbols')

    if 'symbols' in data:
        codes = [generate_symbol(s, custom) for s in data['symbols']]
        return {'success': True, 'latex_code': ''.join(codes)}

    if action == 'symbol' or (not action and 'name' in data):
        return {'success': True, 'latex_code': generate_symbol(data.get('name'), custom)}

    params = data.get('params') or {}
    if custom:
        params.setdefault('custom_symbols', custom)
    return {'success': True, 'latex_code': generate_formula(data.get('type'), params)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '缺少参数'}, ensure_ascii=False))
        sys.exit(1)
    try:
        result = handle(json.loads(sys.argv[1]))
        print(json.dumps(result, ensure_ascii=False))
    except (KeyError, ValueError) as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:  # pragma: no cover - 防御性兜底
        print(json.dumps({'success': False, 'error': '生成失败: %s' % e}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
