# 📄 Invoice Digitalization Platform

> Transform handwritten invoices into digital text with advanced OCR technology

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![EasyOCR](https://img.shields.io/badge/OCR-EasyOCR-orange.svg)](https://github.com/JaidedAI/EasyOCR)

---

## 🎯 Overview

The Invoice Digitalization Platform is a powerful, free, and open-source solution for extracting text from handwritten invoices. Built with **EasyOCR** and advanced image preprocessing techniques, it converts paper invoices into structured digital data with high accuracy.

### ✨ Key Features

- 🖼️ **Advanced Image Preprocessing** - CLAHE contrast enhancement, denoising, and morphological operations
- 🎯 **High Accuracy OCR** - Powered by EasyOCR with optimized settings for handwriting
- 📊 **Detailed Analytics** - Word-level confidence scores and comprehensive statistics
- 💾 **Debug Mode** - Saves preprocessed images for quality inspection
- 🔧 **Memory Optimized** - Handles images of any size without memory overflow
- 🆓 **100% Free** - No API keys, no billing, runs completely offline

### 🚀 Use Cases

- Digitizing handwritten business invoices
- Converting paper records to searchable text
- Automating invoice data entry
- Building document management systems
- Creating searchable invoice archives

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Usage Examples](#-usage-examples)
- [Output Format](#-output-format)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Performance Tips](#-performance-tips)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux
- 4GB RAM minimum (8GB recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/invoice-digitalization-platform.git
cd invoice-digitalization-platform
```

### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install easyocr opencv-python numpy
```

**Note:** On first run, EasyOCR will download recognition models (~100MB). Ensure you have a stable internet connection.

---

##  Quick Start

### Basic Usage

```bash
python script.py invoice.jpg
```

### With Output Redirection

```bash
python script.py invoice.jpg > output.txt
```

### Processing Multiple Files

```bash
# Windows
for %f in (invoices\*.jpg) do python script.py "%f" > "output_%~nf.txt"

# Linux/macOS
for f in invoices/*.jpg; do python script.py "$f" > "output_$(basename "$f" .jpg).txt"; done
```

---

##  How It Works

### Processing Pipeline

```
Input Image → Preprocessing → OCR Detection → Text Extraction → Results Output
```

### 1. **Preprocessing Stage**

The script applies multiple enhancement techniques:

- **Grayscale Conversion** - Simplifies image to single channel
- **CLAHE Enhancement** - Adaptive contrast improvement for uneven lighting
- **Denoising** - Removes background noise and artifacts
- **Otsu's Thresholding** - Automatic binary conversion
- **Morphological Operations** - Cleans up small imperfections
- **Smart Resizing** - Optimizes image dimensions for OCR

### 2. **OCR Detection**

Uses EasyOCR with optimized parameters:
- Memory-efficient batch processing
- Adjusted confidence thresholds
- Single-worker mode for stability

### 3. **Output Generation**

Produces:
- Full extracted text
- Word-by-word confidence scores
- Visual confidence indicators
- Comprehensive statistics

---

##  Usage Examples

### Example 1: Basic Invoice Processing

```bash
python script.py my_invoice.jpg
```

**Output:**
```
============================================================
EXTRACTED TEXT FROM INVOICE
============================================================
TALUR YASHWANTH
============================================================

WORD-LEVEL DETAILS (with confidence scores)
============================================================
[HIGH]   1. TALUR                     | Confidence:  92.3% █████████
[HIGH]   2. YASHWANTH                 | Confidence:  88.7% ████████
```

### Example 2: Batch Processing

Create a batch script (`process_all.bat`):

```batch
@echo off
for %%f in (invoices\*.jpg) do (
    echo Processing %%f...
    python script.py "%%f" > "output\%%~nf.txt"
)
echo Done!
```

### Example 3: Custom Language

Modify `script.py` to support multiple languages:

```python
# For Hindi + English
ocr = InvoiceOCR(languages=['en', 'hi'])

# For Spanish + English
ocr = InvoiceOCR(languages=['en', 'es'])
```

**Supported languages:** English, Hindi, Spanish, French, German, Chinese, Japanese, Korean, and 70+ more!

---

##  Output Format

### Console Output Structure

```
============================================================
FREE HANDWRITTEN INVOICE OCR - Powered by EasyOCR
============================================================

Preprocessing image for better accuracy...
Preprocessed image saved as: preprocessed_invoice.jpg
Image size: 1280x960 pixels

Running OCR detection...

============================================================
EXTRACTED TEXT FROM INVOICE
============================================================
[Extracted text here]
============================================================

WORD-LEVEL DETAILS (with confidence scores)
============================================================
[HIGH]   1. WORD1          | Confidence:  95.2% █████████
[MED]    2. WORD2          | Confidence:  67.8% ██████
[LOW]    3. WORD3          | Confidence:  45.1% ████

============================================================
STATISTICS
============================================================
Total words detected: 15
Average confidence: 78.45%
High confidence (>80%): 10 words
Medium confidence (50-80%): 3 words
Low confidence (<50%): 2 words
Character count: 125
Lines detected: 15
============================================================
```

### Understanding Confidence Levels

| Level | Confidence | Meaning |
|-------|------------|---------|
| `[HIGH]` | >80% | Very reliable, likely accurate |
| `[MED]` | 50-80% | Moderately reliable, may need review |
| `[LOW]` | <50% | Low reliability, manual verification recommended |

---

##  Configuration

### Adjusting Preprocessing

Edit the `preprocess_image()` method in `script.py`:

```python
# Increase contrast enhancement
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Default: 2.0

# Adjust denoising strength
denoised = cv2.fastNlMeansDenoising(enhanced, None, 15, 7, 21)  # Default: 10

# Change max image dimension
max_dimension = 1280  # Default: 1920
```

### Adjusting OCR Parameters

Edit the `extract_text()` method:

```python
results = self.reader.readtext(
    img,
    text_threshold=0.7,  # Increase for stricter detection (default: 0.6)
    low_text=0.5,        # Increase to reduce false positives (default: 0.4)
)
```

---

##  Troubleshooting

### Issue: "Not enough memory" error

**Solution:**
1. Reduce `max_dimension` in the script (try 1280 or 800)
2. Close other applications
3. Process smaller images
4. Use a machine with more RAM

### Issue: Poor accuracy on handwriting

**Solutions:**
1. Ensure good lighting when capturing images
2. Use higher resolution images (300 DPI or higher)
3. Make sure text is dark on light background
4. Check the `preprocessed_*.jpg` file - if it looks unclear, adjust preprocessing
5. Consider using Google Vision API for better accuracy (requires billing)

### Issue: No text detected

**Possible causes:**
1. Image is too blurry or low resolution
2. Text is too faint or light
3. Preprocessing made text worse

**Solutions:**
1. Try running with `use_preprocessing=False`
2. Manually enhance the image in photo editor first
3. Retake the photo with better lighting

### Issue: Wrong language detected

**Solution:**
Change the language parameter:
```python
ocr = InvoiceOCR(languages=['hi'])  # For Hindi only
```

---

## 🎯 Performance Tips

### For Best Results

1. **Image Quality**
   - Use 300 DPI or higher resolution
   - Ensure even, bright lighting
   - Avoid shadows and glare
   - Keep text dark on light background

2. **Camera Settings**
   - Hold camera steady or use tripod
   - Ensure text is in focus
   - Capture straight-on (not at angle)
   - Fill frame with document

3. **Preprocessing**
   - Check `preprocessed_*.jpg` output
   - Adjust CLAHE settings if needed
   - Experiment with threshold values

4. **Hardware**
   - Use GPU for faster processing (requires CUDA setup)
   - More RAM = can process larger images
   - SSD speeds up model loading

---

## 🗺️ Roadmap

### Planned Features

- [ ] Batch processing GUI
- [ ] CSV/Excel export of extracted data
- [ ] Web-based interface
- [ ] Invoice field detection (date, amount, invoice number)
- [ ] Multi-language support in UI
- [ ] Database integration
- [ ] REST API for integration
- [ ] Docker containerization
- [ ] PDF support
- [ ] Template-based extraction

### Alternative OCR Engines (Future)

- TrOCR (Microsoft's transformer model)
- Tesseract OCR integration
- Google Vision API support
- Azure Form Recognizer integration

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- Improving preprocessing algorithms
- Adding support for more languages
- Creating a GUI interface
- Writing tests
- Documentation improvements
- Performance optimizations

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - The OCR engine powering this project
- [OpenCV](https://opencv.org/) - Image processing library
- [NumPy](https://numpy.org/) - Numerical computing tools

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/invoice-digitalization-platform/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/invoice-digitalization-platform/discussions)
- **Email:** taluryash4@gmail.com

---

## 📊 Project Stats

- **Language:** Python 3.8+
- **Dependencies:** 3 core libraries
- **Lines of Code:** ~250
- **Processing Time:** 2-5 seconds per invoice
- **Accuracy:** 70-95% (depends on handwriting quality)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for the open-source community

</div>