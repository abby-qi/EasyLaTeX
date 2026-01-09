"""
Data Converter
Converts between JSON intermediate data and various formats.
"""

import json

try:
    from jsonschema import validate, ValidationError
except ImportError:
    validate = None
    ValidationError = None


class DataConverter:
    """Handles data conversion between formats."""

    def __init__(self):
        self.document_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "author": {"type": "string"},
                "content": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "data": {"type": "object"}
                        }
                    }
                }
            }
        }

    def json_to_latex(self, json_data):
        """
        Convert JSON data to LaTeX code.

        Args:
            json_data: JSON string or dict

        Returns:
            str: LaTeX code
        """
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")

        if not isinstance(json_data, dict):
            raise ValueError("Input must be a JSON object")

        title = json_data.get('title', 'Document')
        author = json_data.get('author', '')
        content = json_data.get('content', [])

        latex_lines = []

        latex_lines.append(r'\documentclass[12pt,a4paper]{article}')
        latex_lines.append(r'\usepackage{ctex}')
        latex_lines.append(r'\usepackage{amsmath,amssymb,amsfonts}')
        latex_lines.append(r'\usepackage{graphicx}')
        latex_lines.append(r'\usepackage{booktabs}')
        latex_lines.append(r'\usepackage{geometry}')
        latex_lines.append(r'\geometry{a4paper,left=3.17cm,right=3.17cm,top=2.54cm,bottom=2.54cm}')

        if title:
            latex_lines.append(r'\title{' + title + '}')
        if author:
            latex_lines.append(r'\author{' + author + '}')
        latex_lines.append(r'\date{\today}')

        latex_lines.append(r'\begin{document}')
        latex_lines.append(r'\maketitle')

        for item in content:
            if isinstance(item, dict):
                item_type = item.get('type', 'text')
                item_content = item.get('content', '')

                if item_type == 'text':
                    latex_lines.append(item_content)
                elif item_type == 'formula':
                    latex_lines.append(item_content)
                elif item_type == 'table':
                    latex_lines.append(item_content)
                elif item_type == 'section':
                    latex_lines.append(r'\section{' + item_content + '}')
                elif item_type == 'subsection':
                    latex_lines.append(r'\subsection{' + item_content + '}')
            elif isinstance(item, str):
                latex_lines.append(item)

        latex_lines.append(r'\end{document}')

        return '\n'.join(latex_lines)

    def latex_to_json(self, latex_code):
        """
        Convert LaTeX code to JSON data.

        Args:
            latex_code: LaTeX source code

        Returns:
            dict: JSON data
        """
        lines = latex_code.split('\n')
        content = []
        title = ''
        author = ''

        for line in lines:
            line = line.strip()

            if line.startswith(r'\title{'):
                title = line[7:-1]
            elif line.startswith(r'\author{'):
                author = line[8:-1]
            elif line.startswith(r'\section{'):
                section_title = line[9:-1]
                content.append({'type': 'section', 'content': section_title})
            elif line.startswith(r'\subsection{'):
                subsection_title = line[12:-1]
                content.append({'type': 'subsection', 'content': subsection_title})
            elif line and not line.startswith('\\') and not line.startswith('%'):
                content.append({'type': 'text', 'content': line})

        return {
            'title': title,
            'author': author,
            'content': content
        }

    def validate_json(self, json_data):
        """
        Validate JSON data against schema.

        Args:
            json_data: JSON data to validate

        Returns:
            tuple: (valid: bool, error: str)
        """
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                return (False, f"Invalid JSON: {e}")

        if validate is None:
            return (True, 'Schema validation not available (jsonschema not installed)')

        try:
            validate(instance=json_data, schema=self.document_schema)
            return (True, '')
        except ValidationError as e:
            return (False, f"Validation error: {e.message}")