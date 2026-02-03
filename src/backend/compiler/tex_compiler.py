import sys
import json
import os
import subprocess
import tempfile

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def compile_latex(data, tinytex_path=None):
    """
    编译LaTeX代码为PDF
    :param data: 包含LaTeX内容的数据
    :param tinytex_path: TinyTeX的路径（可选）
    :return: 编译结果
    """
    try:
        content = data.get('content', '')
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 写入LaTeX文件
            tex_file_path = os.path.join(temp_dir, 'document.tex')
            with open(tex_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 构建LaTeX命令
            latex_cmd = ['pdflatex', '-interaction=nonstopmode', 'document.tex']
            
            # 如果指定了TinyTeX路径，使用它
            env = os.environ.copy()
            if tinytex_path and os.path.exists(tinytex_path):
                # 添加TinyTeX的bin目录到PATH
                tinytex_bin = os.path.join(tinytex_path, 'bin', 'win32' if os.name == 'nt' else 'linux')
                if os.path.exists(tinytex_bin):
                    env['PATH'] = tinytex_bin + os.pathsep + env['PATH']
            
            # 执行编译
            process = subprocess.run(
                latex_cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                env=env
            )
            
            # 检查编译结果
            pdf_path = os.path.join(temp_dir, 'document.pdf')
            if not os.path.exists(pdf_path):
                # 编译失败，返回错误信息
                return {
                    "success": False,
                    "error": f"LaTeX编译失败: {process.stderr or process.stdout}"
                }
            
            return {
                "success": True,
                "pdf_path": pdf_path
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "缺少参数"}))
        sys.exit(1)
    
    try:
        data = json.loads(sys.argv[1])
        result = compile_latex(data)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
