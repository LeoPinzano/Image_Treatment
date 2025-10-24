# Image_Treatment

Small image processing utilities using Pillow (PIL).

## Overview
This repository contains `Traitement_Images.py`, a collection of simple image processing functions (grayscale, negative, red filter, brightness, contrast, thresholding, pixelation, sepia, smoothing, sharpening, gradient). The file was translated from French to English; functions operate directly on a PIL Image object and save results to `output.jpg` by default.

## Requirements
- Python 3.7+
- Pillow

Install Pillow:

```powershell
pip install Pillow
```

## Usage
Put an `img.jpg` file in the same directory or modify the script to open a different image.

Basic usage (run from project root):

- Interactive / one-liner examples:

```powershell
python -c "from Traitement_Images import img, grayscale; grayscale(img)"
python -c "from Traitement_Images import img, sepia; sepia(img)"
```

- Open and call functions in a Python REPL:

```powershell
python
>>> from Traitement_Images import img, width, height, pixelate
>>> pixelate(img)  # will ask for block size, saves to output.jpg
```

## Notes & Limitations
- The module opens `img.jpg` at import time. Make sure that file exists or modify the `img = Image.open("img.jpg")` line.
- Color channel arithmetic (brightness, sharpening, etc.) does not currently clamp values to [0, 255]. Out-of-range values may produce incorrect colors or errors on some systems.
- Some filters use simple nested loops and are not optimized for large images. They are intended as educational examples.

## Suggested next steps
- Add input validation and clamp RGB values to [0,255].
- Provide a small CLI or menu to choose and run filters.
- Add unit tests that exercise the core pixel transforms on small generated images.

## Files
- `Traitement_Images.py` — image processing functions (call functions after ensuring `img.jpg` exists)
- `README.md` — this document

If you want, I can add a small CLI (menu) and clamp values automatically — tell me which you'd prefer next.