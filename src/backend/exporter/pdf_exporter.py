import sys
import json
import os
import shutil

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入LaTeX编译器
from compiler.tex_compiler import compile_latex

def export_pdf(data, output_path):
    """
    导出PDF文件
    :param data: 包含文档内容的数据
    :param output_path: 输出文件路径
    :return: 导出结果
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 获取TinyTeX路径
        tinytex_path = data.get('tinytex_path')
        
        # 编译LaTeX为PDF
        compile_result = compile_latex(data, tinytex_path)
        
        if not compile_result.get('success', False):
            return {
                "success": False,
                "error": compile_result.get('error', '编译失败')
            }
        
        # 复制生成的PDF到指定输出路径
        temp_pdf_path = compile_result.get('pdf_path')
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            # 确保输出文件路径是绝对路径
            output_path = os.path.abspath(output_path)
            
            # 再次确保输出目录存在（绝对路径可能不同）
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 复制文件
            shutil.copy2(temp_pdf_path, output_path)
            
            # 验证文件是否成功复制
            if not os.path.exists(output_path):
                return {
                    "success": False,
                    "error": f"PDF文件复制失败，目标路径不存在: {output_path}"
                }
                
            # 验证文件大小
            if os.path.getsize(output_path) == 0:
                return {
                    "success": False,
                    "error": f"PDF文件复制失败，目标文件为空: {output_path}"
                }
        else:
            return {
                "success": False,
                "error": "PDF文件生成失败"
            }
        
        return {
            "success": True,
            "pdf_path": output_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"导出失败: {str(e)}"
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "缺少参数"}))
        sys.exit(1)
    
    try:
        data = json.loads(sys.argv[1])
        output_path = sys.argv[2]
        result = export_pdf(data, output_path)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
