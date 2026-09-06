#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX 编译模块 (tex_compiler)

把 LaTeX 源码编译成 PDF，并把天书般的 TeX 错误日志翻译成人话。

历史问题
--------
1. 旧实现把 TinyTeX 的 bin 目录写死成 ``tinytex/bin/win32``，而 TinyTeX 官方
   压缩包解压后的真实结构是按平台命名的：

       Windows -> .TinyTeX/bin/windows/
       Linux   -> .TinyTeX/bin/x86_64-linux/
       macOS   -> .TinyTeX/bin/universal-darwin/

   三端没有一个叫 win32，于是"内置 TinyTeX"永远命中不了。
2. install.bat 在 ``src/scripts/`` 下运行会装出 ``src/scripts/tinytex``，
   而主进程算的是项目根目录下的 ``tinytex``，两处对不上。
3. 编译引擎写死 pdflatex，而项目模板里到处是 ``\\usepackage{ctex}``，
   中文文档用 pdflatex 编译必然失败。
4. 编译失败时把整段 stdout 原样抛给前端，用户看不懂。

本模块改为：多路径探测 + 按内容自动选引擎 + 结构化错误解析 + 中文错误提示。
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------------------
# 引擎与路径探测
# ---------------------------------------------------------------------------

# 各平台下 TinyTeX 实际的 bin 子目录名（按优先级排列）
_TINYTEX_BIN_DIRS = {
    'nt': ['bin/windows', 'bin/win32', 'bin'],
    'posix': [
        'bin/x86_64-linux',
        'bin/aarch64-linux',
        'bin/universal-darwin',
        'bin/x86_64-darwin',
        'bin/arm64-darwin',
        'bin',
    ],
}

# 引擎探测顺序：中文/Unicode 文档优先 XeLaTeX
ENGINE_CANDIDATES = ['xelatex', 'pdflatex', 'lualatex']

# 出现这些标记时优先使用 XeLaTeX
CJK_MARKERS = ('ctex', 'xeCJK', 'CJKutf8', 'zh_CN', '\\begin{CJK')


def _is_cjk_document(content):
    """判断文档是否需要 XeLaTeX（含中文宏包或大量 CJK 字符）。"""
    if any(marker in content for marker in CJK_MARKERS):
        return True
    cjk_count = sum(1 for ch in content if '\u4e00' <= ch <= '\u9fff')
    return cjk_count >= 5


def _iter_tinytex_roots(explicit_path=None):
    """
    产出所有可能的 TinyTeX 根目录。

    顺序：显式指定 -> 项目根 -> 项目根/.TinyTeX -> src/scripts 下 -> 用户目录
    """
    here = os.path.dirname(os.path.abspath(__file__))          # .../src/backend/compiler
    backend_dir = os.path.dirname(here)                         # .../src/backend
    src_dir = os.path.dirname(backend_dir)                      # .../src
    project_root = os.path.dirname(src_dir)                     # 项目根

    candidates = []
    if explicit_path:
        candidates.append(explicit_path)
        # 也允许直接指向 bin 的上一级或 .TinyTeX 目录
        candidates.append(os.path.join(explicit_path, '.TinyTeX'))

    for base in (project_root, src_dir, os.path.join(src_dir, 'scripts'),
                 os.path.expanduser('~'), os.path.expanduser('~/.TinyTeX')):
        candidates.append(os.path.join(base, 'tinytex'))
        candidates.append(os.path.join(base, '.TinyTeX'))

    # 官方 TinyTeX 包解压后会多出一层 .TinyTeX 目录，两种布局都要覆盖
    expanded = []
    for c in candidates:
        expanded.append(c)
        expanded.append(os.path.join(c, '.TinyTeX'))

    seen = set()
    for c in expanded:
        norm = os.path.normpath(c)
        if norm in seen:
            continue
        seen.add(norm)
        yield norm


def find_latex_engine(explicit_path=None, prefer_engine=None):
    """
    探测可用的 LaTeX 引擎。

    :param explicit_path: 用户/调用方显式给出的 TinyTeX 根目录
    :param prefer_engine: 期望的引擎名，如 'xelatex'
    :return: (engine_path, engine_name, tinytex_root) 三元组；找不到引擎时
             返回 (None, None, None)
    """
    bin_dirs = _TINYTEX_BIN_DIRS.get('nt' if os.name == 'nt' else 'posix',
                                     _TINYTEX_BIN_DIRS['posix'])

    names = list(ENGINE_CANDIDATES)
    if prefer_engine and prefer_engine in names:
        names.remove(prefer_engine)
        names.insert(0, prefer_engine)

    exts = ['.exe', ''] if os.name == 'nt' else ['']

    # 1) 先找 TinyTeX（含显式路径）
    for root in _iter_tinytex_roots(explicit_path):
        for sub in bin_dirs:
            bin_dir = os.path.join(root, *sub.split('/'))
            if not os.path.isdir(bin_dir):
                continue
            for name in names:
                for ext in exts:
                    candidate = os.path.join(bin_dir, name + ext)
                    if os.path.isfile(candidate):
                        return candidate, name, root

    # 2) 回退到系统 PATH 里的发行版（TeX Live / MiKTeX / MacTeX）
    for name in names:
        found = shutil.which(name)
        if found:
            return found, name, None

    return None, None, None


# ---------------------------------------------------------------------------
# 错误日志解析
# ---------------------------------------------------------------------------

# ./document.tex:12: Undefined control sequence.
LINE_ERR_RE = re.compile(r'^\s*(?:\./)?([^\s:]+\.tex):(\d+):\s*(.+?)\s*$', re.M)
# ! Undefined control sequence.
BANG_ERR_RE = re.compile(r'^!\s*(.+?)\s*$', re.M)
# l.12 \foo
CONTEXT_LINE_RE = re.compile(r'^l\.(\d+)\s?(.*)$', re.M)
# LaTeX Warning: Reference `xxx' on page 1 undefined
WARNING_RE = re.compile(r'^(?:LaTeX|Package)[^\n]*Warning[^\n]*$', re.M)

# 常见 TeX 错误 -> 中文解释
ERROR_TRANSLATIONS = [
    (r'Undefined control sequence',
     '使用了未定义的命令（可能拼错了命令名，或缺少对应的宏包）'),
    (r'Missing \$ inserted',
     '数学符号写在了公式环境外面，需要用 $ ... $ 包裹'),
    (r'Missing (?:\\|\}) inserted|Missing } inserted|Missing \\\\?endgroup',
     '花括号不配对，请检查 { 和 } 是否一一对应'),
    (r'File .* not found|not found',
     '缺少宏包或文件，需要用 LaTeX 发行版的包管理器安装'),
    (r'Environment .* undefined',
     '环境名不存在（可能拼错，或缺少对应的宏包）'),
    (r'\\begin\{.*\} ended by \\end\{.*\}',
     '环境嵌套不匹配，\\begin 与 \\end 的顺序交叉了'),
    (r'Too many }.?\'?s?|Extra }, or forgotten',
     '多了一个右花括号 }'),
    (r'Unicode character .* not set up for use with LaTeX',
     '当前引擎不支持这个字符，中文文档请改用 XeLaTeX 编译'),
    (r'Dimension too large|Overfull',
     '内容超出页面范围，检查表格或图片是否过宽'),
    (r'Emergency stop|Fatal error',
     '编译被强制中止，通常是前面的错误导致无法继续'),
    (r'Package .* Error',
     '某个宏包报错，请查看该宏包的说明'),
    (r'No room for a new',
     'TeX 资源耗尽，通常是宏包加载过多'),
    (r'Double subscript|Double superscript',
     '同一个符号上重复使用了下标或上标'),
    (r'Illegal unit of measure',
     '长度单位写法有误，例如应写成 5cm 而不是 5'),
    (r'There.s no line here to end',
     '在不能换行的位置使用了 \\\\ 换行'),
]


def translate_error(message):
    """把英文 TeX 错误信息翻译成中文解释；没有匹配时返回空字符串。"""
    for pattern, chinese in ERROR_TRANSLATIONS:
        if re.search(pattern, message, re.I):
            return chinese
    return ''


def parse_log(log_text):
    """
    从编译日志中结构化提取错误与警告。

    :return: {'errors': [{'line': int|None, 'message': str, 'hint': str}],
              'warnings': [str], 'raw': str}
    """
    errors = []
    seen = set()

    for m in LINE_ERR_RE.finditer(log_text or ''):
        line_no = int(m.group(2))
        message = m.group(3)
        key = (line_no, message)
        if key in seen:
            continue
        seen.add(key)
        errors.append({
            'line': line_no,
            'message': message,
            'hint': translate_error(message),
        })

    # ! 开头的错误，行号通常在紧随其后的 l.<n> 行上
    if not errors:
        for m in BANG_ERR_RE.finditer(log_text or ''):
            message = m.group(1)
            tail = log_text[m.end():m.end() + 400]
            lm = CONTEXT_LINE_RE.search(tail)
            errors.append({
                'line': int(lm.group(1)) if lm else None,
                'message': message,
                'hint': translate_error(message),
            })
            if len(errors) >= 10:
                break

    warnings = [w.strip() for w in WARNING_RE.findall(log_text or '')]

    return {
        'errors': errors[:20],
        'warnings': warnings[:10],
        'raw': '',
    }


def _summarize(log_text):
    """从日志里截取最有价值的一段，避免把几千行垃圾全丢给前端。"""
    if not log_text:
        return ''
    lines = log_text.splitlines()
    keep = [ln for ln in lines if ln.strip().startswith(('!', 'l.', './')) or
            re.match(r'^\s*(?:\./)?[^\s:]+\.tex:\d+:', ln)]
    if keep:
        return '\n'.join(keep[:40])
    return '\n'.join(lines[-30:])


# ---------------------------------------------------------------------------
# 编译
# ---------------------------------------------------------------------------

def _build_env(bin_dir):
    env = os.environ.copy()
    if bin_dir and os.path.isdir(bin_dir):
        env['PATH'] = bin_dir + os.pathsep + env.get('PATH', '')
        # TeX Live 需要知道自己的根目录才能找到宏包
        root = os.path.dirname(bin_dir)
        env.setdefault('TEXMFHOME', os.path.join(root, 'texmf-local'))
    return env


def compile_latex(data, tinytex_path=None, output_dir=None):
    """
    编译 LaTeX 源码为 PDF。

    :param data: 至少包含 'content' 的字典，可选 'engine'、'output_dir'
    :param tinytex_path: 显式指定的 TinyTeX 根目录
    :param output_dir: PDF 输出目录；不指定时用系统临时目录下的固定子目录
    :return: 结果字典 {success, pdf_path, engine, log, errors, warnings, message}
    """
    data = data or {}
    content = data.get('content', '') or ''
    if not content.strip():
        return {'success': False, 'error': '内容为空，没有可编译的 LaTeX 源码'}

    tinytex_path = tinytex_path or data.get('tinytex_path')
    output_dir = output_dir or data.get('output_dir')

    # 按内容选引擎：中文文档优先 XeLaTeX
    prefer = data.get('engine')
    if not prefer:
        prefer = 'xelatex' if _is_cjk_document(content) else 'pdflatex'

    engine_path, engine_name, tinytex_root = find_latex_engine(tinytex_path, prefer)
    if not engine_path:
        return {
            'success': False,
            'error': '未找到 LaTeX 引擎。请运行 src/scripts/install.bat 安装内置 TinyTeX，'
                     '或自行安装 TeX Live / MiKTeX 并加入 PATH。',
            'need_setup': True,
        }

    # 工作目录用完即删，但 PDF 必须落到持久目录，否则前端拿到路径时文件已经没了
    if not output_dir:
        output_dir = os.path.join(tempfile.gettempdir(), 'easylatex-build')
    os.makedirs(output_dir, exist_ok=True)

    work_dir = tempfile.mkdtemp(prefix='easylatex-', dir=tempfile.gettempdir())
    tex_file = os.path.join(work_dir, 'document.tex')

    try:
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)

        bin_dir = os.path.dirname(engine_path)
        env = _build_env(bin_dir)

        cmd = [engine_path, '-interaction=nonstopmode',
               '-halt-on-error', '-file-line-error', 'document.tex']

        try:
            proc = subprocess.run(cmd, cwd=work_dir, capture_output=True,
                                  text=True, env=env, timeout=180,
                                  errors='replace')
            log_text = (proc.stdout or '') + '\n' + (proc.stderr or '')
            returncode = proc.returncode
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': '编译超时（超过 180 秒），请检查是否存在死循环或超大内容'}
        except UnicodeDecodeError:
            return {'success': False, 'error': '编译输出编码异常，无法解析日志'}

        pdf_src = os.path.join(work_dir, 'document.pdf')
        parsed = parse_log(log_text)

        if not os.path.exists(pdf_src):
            summary = _summarize(log_text)
            first = parsed['errors'][0] if parsed['errors'] else None
            message = '编译失败'
            if first:
                message += '（第 %s 行）: %s' % (first['line'], first['message'])
                if first['hint']:
                    message += '\n提示: ' + first['hint']
            return {
                'success': False,
                'error': message,
                'errors': parsed['errors'],
                'warnings': parsed['warnings'],
                'log': summary or log_text[-4000:],
                'returncode': returncode,
            }

        # 复制到持久目录，防止临时目录被清理后 PDF 消失
        pdf_dest = os.path.join(output_dir, 'document.pdf')
        shutil.copy2(pdf_src, pdf_dest)

        return {
            'success': True,
            'pdf_path': pdf_dest,
            'engine': engine_name,
            'engine_path': engine_path,
            'tinytex_root': tinytex_root or '',
            'warnings': parsed['warnings'],
            'log': _summarize(log_text),
            'size': os.path.getsize(pdf_dest),
        }
    except Exception as e:
        return {'success': False, 'error': '编译过程异常: %s' % e}
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def check_environment(explicit_path=None):
    """供前端「环境自检」调用，返回引擎探测结果。"""
    engine_path, engine_name, root = find_latex_engine(explicit_path)
    return {
        'success': bool(engine_path),
        'engine': engine_name,
        'engine_path': engine_path or '',
        'tinytex_root': root or '',
        'source': 'tinytex' if root else ('system' if engine_path else 'none'),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '缺少参数'}, ensure_ascii=False))
        sys.exit(1)
    try:
        payload = json.loads(sys.argv[1])
        if payload.get('action') == 'check':
            print(json.dumps(check_environment(payload.get('tinytex_path')),
                             ensure_ascii=False))
            sys.exit(0)
        result = compile_latex(payload, payload.get('tinytex_path'))
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get('success') else 1)
    except Exception as e:  # pragma: no cover
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
