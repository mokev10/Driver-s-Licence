# Image to SVG Converter – Free Open Source Python Tool

This is a free and open-source **Image to SVG Converter** written in Python.  
It converts raster images such as **PNG, JPG, and JPEG** into **black & white SVG vector files** using **OpenCV** and **Potrace**.

This tool is useful for developers who want to perform **image vectorization**, **bitmap to SVG**, or **raster to vector conversion** locally using Python.

---

## Features

- Convert PNG to SVG
- Convert JPG / JPEG to SVG
- Raster image to vector (SVG) conversion
- Black & white SVG output
- Batch convert images from a folder
- Free and open-source image to svg converter
- Python based image vectorization tool

---

## Prerequisites

Make sure the following are installed on your system:

1. **Python 3.x**
2. **OpenCV for Python**
   ```bash
   pip install opencv-python
   ```
3. **Potrace**

   Download Potrace

   Extract it and note the full path to `potrace.exe`

---

## Setup Instructions

1. Place all images you want to convert (PNG, JPG, JPEG) in the same folder as the Python script (`main.py`).
2. Open `main.py` and update the `potrace_path` variable with the full path to your Potrace executable.

Example:

```python
potrace_path = r"C:\\Users\\YourName\\Downloads\\potrace.exe"
```

---

## How to Run the Image to SVG Converter

Open terminal or command prompt in the project folder and run:

```bash
python main.py
```

Or, if your system uses `python3`:

```bash
python3 main.py
```

---

## Output

Converted SVG files are saved inside the \`svg_vector_output\` folder.

Temporary PBM files are automatically created and removed.

Supported input formats:

- `.png`
- `.jpg`
- `.jpeg`

---

## Notes

- `os` and `subprocess` are built-in Python modules (no installation needed).
- `cv2` (OpenCV) must be installed separately.
- Ensure the Potrace executable path is correct and accessible.

---

## Keywords

- image to svg converter
- png to svg converter
- jpg to svg converter
- bitmap to svg
- raster to vector converter
- image vectorization python
- open source image to svg
- svg converter github
