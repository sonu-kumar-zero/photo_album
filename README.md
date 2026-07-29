# Photo Gallery

Minimal PySide6 desktop editor for laying out a single page on a zoomable, pannable canvas.

## Features

- Qt graphics-view based editor window
- Centered white page on a dark workspace background
- Mouse wheel zoom with min/max zoom limits
- Middle-mouse drag to pan the canvas

## Requirements

- Python 3.11+
- Qt libraries via PySide6

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the application with:

```bash
python main.py
```

## Controls

- Scroll wheel: zoom in and out
- Middle mouse button drag: pan the view

## Project Structure

- `main.py` - application entry point
- `app/` - main window setup
- `canvas/` - graphics scene, view, and page item
- `utils/` - shared constants

## Notes

The current codebase provides the editor shell and canvas interactions only. There are no file import/export, layer, or image placement workflows implemented yet.