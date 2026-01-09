"""
PDF Exporter
Exports documents to PDF format.
"""

import sys
import json
import os
import tempfile


class PDFExporter:
    """Handles PDF export functionality."""

    def __init__(self, compiler=None):
        if compiler is None:
            from backend.compiler.tex_compiler import TeXCompiler
            compiler = TeXCompiler()
        self.compiler = compiler

    def export(self, tex_content, output_path):
        """
        Export LaTeX content to PDF.

        Args:
            tex_content: LaTeX source code
            output_path: Output PDF file path

        Returns:
            tuple: (success: bool, pdf_path: str, error: str)
        """
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
                f.write(tex_content)
                tex_file_path = f.name

            success, pdf_path, error_log = self.compiler.compile(tex_file_path)

            os.unlink(tex_file_path)

            if success and pdf_path:
                import shutil
                shutil.move(pdf_path, output_path)
                return (True, output_path, '')
            else:
                return (False, '', error_log)

        except Exception as e:
            return (False, '', str(e))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            data = json.loads(sys.argv[1])
            output_path = sys.argv[2]

            tex_content = data.get('content', '')

            exporter = PDFExporter()
            success, pdf_path, error = exporter.export(tex_content, output_path)

            if success:
                print(json.dumps({
                    'success': True,
                    'pdf_path': pdf_path,
                    'message': 'PDF exported successfully'
                }))
            else:
                print(json.dumps({
                    'success': False,
                    'error': error
                }))

        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }))