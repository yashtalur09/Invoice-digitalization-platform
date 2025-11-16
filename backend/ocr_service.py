"""
OCR Service - Integration with script.py for text extraction
"""
import sys
import os
import subprocess
import json
from pathlib import Path

# Add parent directory to path to import script.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from script import InvoiceOCR


class OCRService:
    """
    Service class to handle OCR operations using script.py
    """
    def __init__(self):
        # Initialize OCR reader once (reuse for better performance)
        self.ocr = None
    
    def _get_ocr_instance(self):
        """
        Get or create OCR instance (singleton pattern for efficiency)
        """
        if self.ocr is None:
            self.ocr = InvoiceOCR(languages=['en'])
        return self.ocr
    
    def extract_text_from_image(self, image_path: str) -> dict:
        """
        Extract text from an image using script.py
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            ocr = self._get_ocr_instance()
            result = ocr.extract_text(image_path, use_preprocessing=True)
            
            if result['success']:
                return {
                    'success': True,
                    'text': result['full_text'],
                    'word_count': len(result['words']),
                    'words': result['words']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error'),
                    'text': ''
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }


# Global OCR service instance
ocr_service = OCRService()

