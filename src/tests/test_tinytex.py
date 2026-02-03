#!/usr/bin/env python3
"""
测试 TinyTeX 集成
"""

import json
import subprocess
import os

# 测试简单的 LaTeX 内容
test_tex_content = r'''
\documentclass{article}
\begin{document}
Hello, EasyLaTeX!
\end{document}
'''

# 计算 TinyTeX 路径
tinytex_path = os.path.join(os.getcwd(), 'tinytex')

# 构建测试数据
test_data = {
    'content': test_tex_content,
    'tinytex_path': tinytex_path
}

# 运行编译脚本
print("Testing TinyTeX integration...")
print(f"TinyTeX path: {tinytex_path}")

result = subprocess.run(
    ['python', 'backend/compiler/tex_compiler.py', json.dumps(test_data)],
    capture_output=True,
    text=True
)

print("\nOutput:")
print(result.stdout)

if result.stderr:
    print("\nError:")
    print(result.stderr)

print(f"\nReturn code: {result.returncode}")
