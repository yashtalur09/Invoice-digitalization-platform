# Invoice-digitalization-platform

**Project Description:**
- This repository contains a handwritten invoice OCR utility that extracts text from invoice images using EasyOCR with advanced preprocessing steps (CLAHE contrast enhancement, denoising, morphological cleanup and resizing) to improve recognition accuracy for handwritten and noisy documents.

**What's Included:**
- `script.py`: Main Python script implementing preprocessing, EasyOCR integration, and logging of results.
- `invoices/`: Example data and logs (e.g. `invoice_logs.csv`).

**Tech Stack:**
- Python (3.8+ recommended)
- EasyOCR (OCR engine)
- OpenCV (`opencv-python`) (image preprocessing)
- NumPy (array handling)
- (Optional) GPU acceleration if EasyOCR + CUDA are configured

**Installation (Windows - `cmd`)**
1. Install Python 3.8 — 3.11 from https://www.python.org/ if you don't already have it.
2. Open `cmd.exe` and create + activate a virtual environment:

```
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install required packages:

```
pip install --upgrade pip
pip install easyocr opencv-python numpy
```

Notes:
- If you prefer to pin versions, create a `requirements.txt` file and install via `pip install -r requirements.txt`.
- EasyOCR may download model files on first run and can use GPU when configured; the included `script.py` defaults to CPU.

**How to Run**
- Basic usage:

```
python script.py <path_to_invoice_image>
```

- Example (using the default fallback named `invoice.jpg` in repository root):

```
python script.py invoice.jpg
```

What to expect:
- The script will initialize EasyOCR (may take a moment on first run), preprocess the image and save a debug file named `preprocessed_<original_filename>` in the working directory.
- The terminal will show extracted text, word-level confidence scores and basic statistics. If no image path is provided, the script uses `invoice.jpg` by default and prints usage information.

**Script Details**
- `InvoiceOCR` class in `script.py`:
  - `preprocess_image(image_path)`: grayscale conversion, CLAHE contrast enhancement, denoising, Otsu thresholding, morphological open/close, and resizing to appropriate dimensions.
  - `extract_text(image_path, use_preprocessing=True)`: runs `easyocr.Reader.readtext` and returns a dictionary with `full_text`, `words` and `success`.
  - `log_results(result)`: prints formatted output and confidence-based summaries to the console.

**Troubleshooting & Tips**
- If EasyOCR fails to initialize, verify network access (model download) and install dependencies. On Windows, ensure Visual C++ redistributable is installed if you hit binary wheel issues.
- For noisy inputs, inspect the generated `preprocessed_*.jpg` file to see how preprocessing affected the image.
- If you want GPU acceleration, install proper CUDA toolkit and the GPU-compatible dependencies for EasyOCR. Carefully follow EasyOCR docs.

**Next Steps / Improvements**
- Add a `requirements.txt` with pinned versions.
- Add command-line flags (e.g., `--no-preprocess`, `--lang`, `--out-csv`) using `argparse`.
- Add tests for preprocessing and a small sample images folder for CI.

**License & Attribution**
- This repository contains code provided by the author. If you incorporate external models or libraries, follow their licenses (EasyOCR, OpenCV, NumPy).

---
Generated on: 2025-11-16
# Invoice-digitalization-platform