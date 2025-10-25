# Image_Treatment

Small image-processing utilities using Pillow (PIL). This project provides a small set of educational, pixel-based filters implemented in [functions.py](functions.py) and two ways to run them: an interactive terminal menu in [interface.py](interface.py) and a lightweight CLI in [main.py](main.py).

## Contents
- [functions.py](functions.py) — image processing functions (e.g. [`functions.grayscale`](functions.py), [`functions.sepia`](functions.py), [`functions.pixelate`](functions.py))
- [interface.py](interface.py) — interactive menu and helpers (e.g. [`interface.main`](interface.py), [`interface.apply_sequence`](interface.py))
- [main.py](main.py) — small runner / CLI entry (`python main.py ...`)

## Requirements
- Python 3.7+
- Pillow

Install Pillow:

```powershell
pip install Pillow
```


## Usage

### 1. Interactive CLI (recommended)

Run the terminal interface to select and apply filters interactively:

```powershell
python main.py
```

You'll see a menu listing all available filters. Enter the number of the filter you want to apply. The result is saved as `output.jpg`.

### 2. One-liner examples

You can still call functions directly:

```powershell
python -c "from functions import img, grayscale; grayscale(img)"
python -c "from functions import img, sepia; sepia(img)"
```

### 3. Python REPL

```powershell
python
>>> from functions import img, width, height, pixelate
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
- `functions.py` — image processing functions (call functions after ensuring `img.jpg` exists)
- `main.py` — terminal menu interface to select and apply filters interactively
- `README.md` — this document