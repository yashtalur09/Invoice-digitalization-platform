"""
Handwritten Invoice Text Extractor using EasyOCR with Advanced Preprocessing
This script extracts text from handwritten invoices with improved accuracy
"""

import easyocr
import sys
import os
import io
import cv2
import numpy as np

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class InvoiceOCR:
    def __init__(self, languages=['en']):
        """
        Initialize EasyOCR reader
        
        Args:
            languages: List of languages to detect (default: English)
        """
        print("Initializing EasyOCR (this may take a moment on first run)...")
        try:
            self.reader = easyocr.Reader(languages, gpu=False)
            print("EasyOCR initialized successfully\n")
        except Exception as e:
            print(f"Error initializing EasyOCR: {e}")
            sys.exit(1)
    
    def preprocess_image(self, image_path):
        """
        Advanced image preprocessing to improve OCR accuracy
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            Preprocessed image
        """
        print("Preprocessing image for better accuracy...")
        
        # Read image
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        # Apply binary threshold
        # Try Otsu's thresholding
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Invert if background is dark
        if np.mean(binary) < 127:
            binary = cv2.bitwise_not(binary)
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Resize to optimal size for OCR (not too big to avoid memory issues)
        max_dimension = 1920  # Maximum width or height
        height, width = cleaned.shape
        
        if max(height, width) > max_dimension:
            # Downscale if too large
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            resized = cv2.resize(cleaned, (new_width, new_height), interpolation=cv2.INTER_AREA)
        elif max(height, width) < 800:
            # Upscale only if too small (max 150%)
            scale = min(1.5, 800 / max(height, width))
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = cv2.resize(cleaned, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            # Keep original size if in good range
            resized = cleaned
        
        # Save preprocessed image for debugging
        debug_path = "preprocessed_" + os.path.basename(image_path)
        cv2.imwrite(debug_path, resized)
        print(f"Preprocessed image saved as: {debug_path}")
        print(f"Image size: {resized.shape[1]}x{resized.shape[0]} pixels\n")
        
        return resized
    
    def extract_text(self, image_path, use_preprocessing=True):
        """
        Extract text from handwritten invoice image
        
        Args:
            image_path: Path to the invoice image file
            use_preprocessing: Whether to apply preprocessing (default: True)
            
        Returns:
            dict: Contains full text and detailed annotations
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            print(f"Processing image: {image_path}")
            print("-" * 60)
            
            # Preprocess image if enabled
            if use_preprocessing:
                img = self.preprocess_image(image_path)
            else:
                img = cv2.imread(image_path)
            
            # Perform OCR with detailed output
            print("Running OCR detection...")
            results = self.reader.readtext(
                img,
                detail=1,
                paragraph=False,
                batch_size=1,  # Process one at a time to save memory
                workers=0,  # Disable multiprocessing to save memory
                text_threshold=0.6,
                low_text=0.4
            )
            
            if not results:
                print("No text detected in the image")
                return {'success': True, 'full_text': '', 'words': []}
            
            # Extract full text and word-level information
            full_text_lines = []
            words = []
            
            for detection in results:
                bbox, text, confidence = detection
                words.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
                full_text_lines.append(text)
            
            full_text = ' '.join(full_text_lines)
            
            return {
                'full_text': full_text,
                'words': words,
                'success': True
            }
            
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            print(f"Error processing image: {e}")
            return {'success': False, 'error': str(e)}
    
    def log_results(self, result):
        """
        Log extraction results to terminal in a formatted way
        
        Args:
            result: Dictionary containing extraction results
        """
        if not result['success']:
            print(f"\nExtraction failed: {result.get('error', 'Unknown error')}")
            return
        
        if not result['full_text']:
            print("\nNo text was detected in the image")
            return
        
        # Log full extracted text
        print("\n" + "="*60)
        print("EXTRACTED TEXT FROM INVOICE")
        print("="*60)
        print(result['full_text'])
        print("="*60)
        
        # Log word-level details with confidence scores
        if result['words']:
            print("\n" + "="*60)
            print("WORD-LEVEL DETAILS (with confidence scores)")
            print("="*60)
            
            for i, word in enumerate(result['words'], 1):
                confidence_percent = word['confidence'] * 100
                confidence_bar = "█" * int(confidence_percent / 10)
                
                # Color code based on confidence
                if confidence_percent >= 80:
                    status = "[HIGH]"
                elif confidence_percent >= 50:
                    status = "[MED] "
                else:
                    status = "[LOW] "
                
                print(f"{status} {i:3d}. {word['text']:25s} | Confidence: {confidence_percent:5.1f}% {confidence_bar}")
        
        # Log statistics
        print("\n" + "="*60)
        print("STATISTICS")
        print("="*60)
        total_words = len(result['words'])
        
        if total_words > 0:
            avg_confidence = sum(w['confidence'] for w in result['words']) / total_words * 100
            high_conf = sum(1 for w in result['words'] if w['confidence'] > 0.8)
            med_conf = sum(1 for w in result['words'] if 0.5 <= w['confidence'] <= 0.8)
            low_conf = sum(1 for w in result['words'] if w['confidence'] < 0.5)
            
            print(f"Total words detected: {total_words}")
            print(f"Average confidence: {avg_confidence:.2f}%")
            print(f"High confidence (>80%): {high_conf} words")
            print(f"Medium confidence (50-80%): {med_conf} words")
            print(f"Low confidence (<50%): {low_conf} words")
        
        print(f"Character count: {len(result['full_text'])}")
        print(f"Lines detected: {len(result['words'])}")
        print("="*60 + "\n")
        
        # Tips
        print("TIPS FOR BETTER RESULTS:")
        print("- Check the 'preprocessed_*.jpg' file to see if preprocessing helped")
        print("- Use good lighting and high resolution images (300 DPI or higher)")
        print("- Ensure text is dark on light background")
        print("- Try different preprocessing by modifying the script")
        print()


def main():
    """
    Main function to run the invoice OCR
    """
    print("="*60)
    print("FREE HANDWRITTEN INVOICE OCR - Powered by EasyOCR")
    print("With Advanced Preprocessing for Better Accuracy")
    print("="*60 + "\n")
    
    # Initialize OCR (supports many languages: 'en', 'hi', 'es', 'fr', etc.)
    ocr = InvoiceOCR(languages=['en'])
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Default path - change this to your invoice image
        image_path = "invoice.jpg"
        print(f"No image path provided. Using default: {image_path}")
        print(f"Usage: python {sys.argv[0]} <path_to_invoice_image>\n")
    
    # Extract text from invoice with preprocessing
    result = ocr.extract_text(image_path, use_preprocessing=True)
    
    # Log results to terminal
    ocr.log_results(result)


if __name__ == "__main__":
    main()