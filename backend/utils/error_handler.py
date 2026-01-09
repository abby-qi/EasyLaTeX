"""
Error Handler
Translates LaTeX errors to human-readable messages.
"""

import logging


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

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def translate(self, error_message):
        """
        Translate LaTeX error to human-readable message.

        Args:
            error_message: Original LaTeX error message

        Returns:
            str: Translated error message
        """
        for latex_error, human_message in self.error_map.items():
            if latex_error in error_message:
                return human_message

        if '!' in error_message:
            return f'LaTeX编译错误: {error_message[:100]}'

        return error_message

    def log_error(self, error_type, error_message, context=None):
        """
        Log error with context.

        Args:
            error_type: Type of error
            error_message: Error message
            context: Additional context information
        """
        translated_message = self.translate(error_message)
        log_msg = f"[{error_type}] {translated_message}"
        if context:
            log_msg += f" | Context: {context}"

        self.logger.error(log_msg)

    def log_warning(self, warning_message, context=None):
        """
        Log warning with context.

        Args:
            warning_message: Warning message
            context: Additional context information
        """
        log_msg = warning_message
        if context:
            log_msg += f" | Context: {context}"

        self.logger.warning(log_msg)

    def log_info(self, info_message, context=None):
        """
        Log info message with context.

        Args:
            info_message: Info message
            context: Additional context information
        """
        log_msg = info_message
        if context:
            log_msg += f" | Context: {context}"

        self.logger.info(log_msg)

    def add_error_mapping(self, latex_error, human_message):
        """Add custom error mapping."""
        self.error_map[latex_error] = human_message
        self.logger.info(f"Added error mapping: {latex_error} -> {human_message}")