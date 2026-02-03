import sys
import json
import os

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def export_word(data, output_path):
    """
    导出Word文件
    :param data: 包含文档内容的数据
    :param output_path: 输出文件路径
    :return: 导出结果
    """
    try:
        # 这里只是一个示例实现
        # 实际项目中应该使用python-docx库生成Word文档
        content = data.get('content', '')
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 写入一个简单的Word文件（实际项目中应该用python-docx）
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Word Export Sample\n{content}")
        
        return {
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "缺少参数"}))
        sys.exit(1)
    
    try:
        data = json.loads(sys.argv[1])
        output_path = sys.argv[2]
        result = export_word(data, output_path)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
