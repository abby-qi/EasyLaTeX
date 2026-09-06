#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三线表生成模块 (table_gen)

生成 booktabs 风格的学术三线表。由 Electron 主进程以
``python table_gen.py '<json>'`` 方式调用，标准输出 JSON。

输入示例：:

    {
      "rows": 3, "cols": 3,
      "data": [["姓名", "年龄", "成绩"], ["张三", "20", "95"], ["李四", "21", "88"]],
      "caption": "学生成绩表",
      "label": "tab:scores",
      "align": "c",          // 单字符统一对齐，或数组 ["l","c","r"]
      "header": true,        // 首行作为表头，下方加 \\midrule
      "position": "htbp",    // 浮动体位置，空字符串则不套 table 环境
      "escape": true         // 是否转义单元格中的 LaTeX 特殊字符
    }

历史 bug 修复记录：
  * 单行表格不再生成多余的 ``\\midrule``（三线表的中线只在「表头 -> 数据」之间出现）。
  * 列数由 ``data`` 实际行长推导，不再依赖用户传入的 ``cols``，避免行列不一致
    导致 ``&`` 分隔符数量错误。
"""

import json
import re
import sys

# 对齐方式白名单，非法值一律回退为居中
_VALID_ALIGN = {'l', 'c', 'r', 'p'}

# 需要转义的 LaTeX 特殊字符（按顺序：& % $ # _ 单独处理，{} 与 \\ 用分组处理）
_ESCAPE_MAP = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
}


def escape_latex(text):
    """转义字符串中的 LaTeX 特殊字符，避免用户输入的 & % $ 等破坏表格结构。"""
    if text is None:
        return ''
    return ''.join(_ESCAPE_MAP.get(ch, ch) for ch in str(text))


def _normalize_data(data, rows, cols):
    """
    把输入数据规整成 rows x cols 的二维列表。

    - 缺失的行补空行，缺失的单元格补空字符串；
    - 多出来的列截断到 cols（以 cols 为准，保证列格式与内容一致）；
    - 未显式指定 cols 时，以最长行的长度为准。
    """
    if not data:
        data = []
    # 过滤掉非列表项，避免前端异常传入字符串导致崩溃
    data = [list(row) if isinstance(row, (list, tuple)) else [row] for row in data]

    if not cols:
        # 未显式给出列数时，以最长行的长度为准；完全没有数据时退化成单列
        cols = max((len(row) for row in data), default=0) or 1
    cols = max(int(cols), 0)

    if rows is not None:
        rows = int(rows)
        if len(data) < rows:
            data = data + [[''] * cols for _ in range(rows - len(data))]
        else:
            data = data[:rows]

    normalized = []
    for row in data:
        row = [('' if c is None else str(c)) for c in row]
        if len(row) < cols:
            row = row + [''] * (cols - len(row))
        elif len(row) > cols:
            row = row[:cols]
        normalized.append(row)
    return normalized, cols


def _build_colspec(cols, align):
    """生成 tabular 的列格式串，如 'lccr'。"""
    if isinstance(align, (list, tuple)):
        spec = ''
        for i in range(cols):
            a = align[i] if i < len(align) else 'c'
            # 支持 'p{3cm}' 这类带参数的列格式
            a = str(a).strip()
            if a and a[0] in _VALID_ALIGN:
                spec += a
            else:
                spec += 'c'
        return spec or 'c'

    a = str(align or 'c').strip()
    if a and a[0] in _VALID_ALIGN:
        return a[0] * cols
    return 'c' * cols


def generate_table(data):
    """
    生成三线表 LaTeX 代码。

    :param data: 描述表格的字典，字段见模块文档
    :return: LaTeX 代码片段
    """
    data = data or {}
    rows = data.get('rows')
    cols = data.get('cols')
    cells, cols = _normalize_data(data.get('data'), rows, cols)

    if cols <= 0 or not cells:
        raise ValueError('表格为空：请至少提供一行一列')

    float_env = str(data.get('position', 'htbp') or '').strip()
    header = bool(data.get('header', True))
    escape = bool(data.get('escape', True))
    colspec = _build_colspec(cols, data.get('align', 'c'))

    body_lines = []
    for row_index, row in enumerate(cells):
        rendered = [escape_latex(c) if escape else ('' if c is None else str(c)) for c in row]
        line = ' & '.join(rendered) + r' \\'
        # 中线只出现在「表头与数据之间」，且表格必须不止一行
        if header and row_index == 0 and len(cells) > 1:
            line += '\n' + r'\midrule'
        body_lines.append(line)

    table_body = '\n'.join(body_lines)

    inner = '\n'.join([
        r'\centering',
        r'\begin{tabular}{%s}' % colspec,
        r'\toprule',
        table_body,
        r'\bottomrule',
        r'\end{tabular}',
    ])

    if not float_env:
        return inner

    caption = data.get('caption')
    label = data.get('label')

    # caption 必须在 label 之前，否则 \ref 会指向章节而不是表格
    caption_line = r'\caption{%s}' % (escape_latex(caption) if escape else caption) if caption else ''
    label_line = r'\label{%s}' % label if label else ''

    parts = [r'\begin{table}[%s]' % float_env, inner]
    if caption_line:
        parts.append(caption_line)
    if label_line:
        parts.append(label_line)
    parts.append(r'\end{table}')

    return '\n'.join(parts)


def handle(data):
    """统一的 CLI / IPC 入口。"""
    return {'success': True, 'latex_code': generate_table(data)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '缺少参数'}, ensure_ascii=False))
        sys.exit(1)
    try:
        result = handle(json.loads(sys.argv[1]))
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, TypeError) as e:
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:  # pragma: no cover - 防御性兜底
        print(json.dumps({'success': False, 'error': '生成失败: %s' % e}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
