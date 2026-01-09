"""
Error Handler
Translates LaTeX errors to human-readable messages.
"""


class ErrorHandler:
    """Handles and translates LaTeX errors."""

    def __init__(self):
        self.error_map = {
            'File not found': '找不到文件，请检查图片路径是否正确',
            'Undefined control sequence': '使用了未定义的LaTeX命令',
            'Missing $ inserted': '数学公式格式错误，请检查符号',
            'Extra alignment tab': '表格列数不匹配',
            'Runaway argument': '参数格式错误',
        }

    def translate(self, error_message):
        """
        Translate LaTeX error to human-readable message.

        Args:
            error_message: Original LaTeX error message

        Returns:
            str: Translated error message
        """
        pass

    def add_error_mapping(self, latex_error, human_message):
        """Add custom error mapping."""
        self.error_map[latex_error] = human_message