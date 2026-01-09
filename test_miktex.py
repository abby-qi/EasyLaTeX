import os
import subprocess
import tempfile

# Test MiKTeX compilation
tex_content = r"""\documentclass{article}
\begin{document}
Hello from MiKTeX!
\end{document}
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
    f.write(tex_content)
    tex_file = f.name

try:
    cmd = [r'D:\Application\MiKTeX\miktex\bin\x64\pdflatex.exe',
           '-interaction=nonstopmode',
           '-file-line-error',
           tex_file]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    print(f"Exit code: {result.returncode}")
    if result.returncode == 0:
        pdf_file = tex_file.replace('.tex', '.pdf')
        if os.path.exists(pdf_file):
            print(f"✓ PDF generated: {pdf_file}")
        else:
            print("✗ PDF file not found")
    else:
        print("✗ Compilation failed")
        print(f"Error output: {result.stderr[:500]}")

finally:
    if os.path.exists(tex_file):
        os.unlink(tex_file)
    pdf_file = tex_file.replace('.tex', '.pdf')
    if os.path.exists(pdf_file):
        os.unlink(pdf_file)
