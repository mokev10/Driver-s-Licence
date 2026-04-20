"""
Image → SVG Batch Converter (OpenCV + Potrace)
----------------------------------------------
Standalone CLI tool (no Streamlit)
"""

import os
import cv2
import subprocess
import shutil

# =========================
# CONFIGURATION
# =========================

potrace_path = r"PUT_YOUR_POTRACE_EXE_PATH_HERE"

input_extensions = (".png", ".jpg", ".jpeg")

output_folder = "svg_vector_output"
temp_folder = "_temp_pbm"

THRESHOLD = 200

os.makedirs(output_folder, exist_ok=True)
os.makedirs(temp_folder, exist_ok=True)

# =========================
# PROCESS IMAGE
# =========================

def convert_to_svg(file_path):

    name = os.path.splitext(os.path.basename(file_path))[0]

    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"[ERROR] Cannot read {file_path}")
        return

    # Binarisation
    _, bw = cv2.threshold(img, THRESHOLD, 255, cv2.THRESH_BINARY)

    pbm_path = os.path.join(temp_folder, f"{name}.pbm")
    svg_path = os.path.join(output_folder, f"{name}.svg")

    cv2.imwrite(pbm_path, bw)

    try:
        subprocess.run(
            [
                potrace_path,
                pbm_path,
                "-s",
                "-o",
                svg_path
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print(f"[OK] {svg_path}")

    except Exception as e:
        print(f"[FAIL] {file_path} → {e}")

    finally:
        if os.path.exists(pbm_path):
            os.remove(pbm_path)

# =========================
# MAIN LOOP
# =========================

def main():

    files = [
        f for f in os.listdir(".")
        if f.lower().endswith(input_extensions)
    ]

    if not files:
        print("No images found.")
        return

    print(f"{len(files)} images found")

    for f in files:
        convert_to_svg(f)

    print("Done.")


if __name__ == "__main__":
    main()
