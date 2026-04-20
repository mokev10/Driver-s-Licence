"""
Tool: Image to SVG Vector Converter
----------------------------------
This script converts raster images (PNG, JPG, JPEG) into
black & white SVG vector files using OpenCV and Potrace.

Workflow:
1. Read image
2. Convert to grayscale
3. Convert to pure black & white
4. Save as PBM (temporary)
5. Convert PBM to SVG using Potrace
6. Clean up temporary files

Author: Farrukh Ali Khan
"""


import os
import cv2
import subprocess

# -------------------------------------------------
# IMPORTANT:
# Replace the path below with the FULL path
# to potrace.exe on your own system
# Example (Windows):
# r"C:\path\to\potrace\potrace.exe"
# -------------------------------------------------
potrace_path = r"PUT_YOUR_POTRACE_EXE_PATH_HERE"

# Supported image formats to process
input_extensions = (".png", ".jpg", ".jpeg")

# Folder where generated SVG files will be saved
output_folder = "svg_vector_output"

# Create output folder if it does not already exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the current directory
for file in os.listdir("."):

    # Process only supported image files
    if file.lower().endswith(input_extensions):

        # Extract file name without extension
        name = os.path.splitext(file)[0]

        # Read the image in grayscale mode
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

        # Convert grayscale image to pure black & white
        # Pixels above threshold become white, below become black
        _, bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

        # Temporary PBM file name (required by Potrace)
        pbm_file = f"{name}.pbm"

        # Save black & white image as PBM
        cv2.imwrite(pbm_file, bw)

        # Output SVG file path
        svg_path = os.path.join(output_folder, f"{name}.svg")

        # Run Potrace to convert PBM file into SVG vector
        subprocess.run([
            potrace_path,   # Path to potrace executable
            pbm_file,       # Input PBM file
            "-s",           # Output format: SVG
            "-o",
            svg_path        # Output SVG file
        ], check=True)

        # Delete temporary PBM file after conversion
        os.remove(pbm_file)

        # Print success message
        print(f"Vector SVG created: {svg_path}")
