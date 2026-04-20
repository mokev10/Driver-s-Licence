import cv2
import subprocess
import os
import tempfile


def png_to_svg(png_bytes, potrace_path, threshold=200):
    """
    Convert PNG (bytes) → SVG using OpenCV + Potrace
    """

    # temp folder
    tmp_dir = tempfile.mkdtemp()

    png_path = os.path.join(tmp_dir, "input.png")
    pbm_path = os.path.join(tmp_dir, "output.pbm")
    svg_path = os.path.join(tmp_dir, "output.svg")

    # save PNG
    with open(png_path, "wb") as f:
        f.write(png_bytes)

    # read image
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Invalid image input")

    # binarization
    _, bw = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # save PBM (required by potrace)
    cv2.imwrite(pbm_path, bw)

    # run potrace
    subprocess.run([
        potrace_path,
        pbm_path,
        "-s",
        "-o",
        svg_path
    ], check=True)

    # read SVG result
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_data = f.read()

    # cleanup
    try:
        os.remove(png_path)
        os.remove(pbm_path)
        os.remove(svg_path)
        os.rmdir(tmp_dir)
    except:
        pass

    return svg_data
