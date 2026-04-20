import cv2
import subprocess
import tempfile
import os


def png_to_svg_via_potrace(
    image_bytes: bytes,
    potrace_path: str,
    threshold: int = 200
) -> str:
    """
    Convert PNG bytes → SVG string using OpenCV + Potrace
    """

    with tempfile.TemporaryDirectory() as tmp:

        input_path = os.path.join(tmp, "input.png")
        pbm_path = os.path.join(tmp, "temp.pbm")
        svg_path = os.path.join(tmp, "output.svg")

        # write image
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        # read grayscale
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            raise ValueError("Invalid image input")

        # binarisation (crucial pour barcode)
        _, bw = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

        # save PBM (required by potrace)
        cv2.imwrite(pbm_path, bw)

        # run potrace
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

        # read SVG
        with open(svg_path, "r", encoding="utf-8") as f:
            svg = f.read()

        return svg
