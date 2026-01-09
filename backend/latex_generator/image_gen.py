"""
Image Generator
Handles image inclusion in LaTeX documents.
"""


class ImageGenerator:
    """Generates LaTeX code for image inclusion."""

    def __init__(self):
        self.default_options = 'width=0.8\\textwidth'

    def generate(self, image_data):
        """
        Generate LaTeX code for image.

        Args:
            image_data: Dictionary containing image path, caption, etc.

        Returns:
            str: LaTeX image code
        """
        pass

    def set_default_options(self, options):
        """Set default figure options."""
        self.default_options = options