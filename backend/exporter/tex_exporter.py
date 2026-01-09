"""
TeX Exporter
Exports documents to LaTeX source code.
"""

import sys
import json
import os


class TexExporter:
    """Handles LaTeX source code export functionality."""

    def __init__(self):
        pass

    def export(self, data, output_path):
        """
        Export data to LaTeX file.

        Args:
            data: Document data structure
            output_path: Output .tex file path

        Returns:
            tuple: (success: bool, error: str)
        """
        try:
            tex_content = data.get('content', '')

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(tex_content)

            return (True, '')
        except Exception as e:
            return (False, str(e))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        try:
            data = json.loads(sys.argv[1])
            output_path = sys.argv[2]

            exporter = TexExporter()
            success, error = exporter.export(data, output_path)

            if success:
                print(json.dumps({
                    'success': True,
                    'message': 'LaTeX file exported successfully'
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