import os
import cv2
import subprocess
import tempfile


def png_to_svg_via_potrace(
    image_bytes: bytes,
    potrace_path: str,
    threshold: int = 200
) -> str:
    """
    Convertit une image PNG (bytes) en SVG vectoriel via OpenCV + Potrace.

    Retourne : SVG string
    """

    # 🔥 fichier temporaire image
    with tempfile.TemporaryDirectory() as tmpdir:

        input_path = os.path.join(tmpdir, "input.png")
        pbm_path = os.path.join(tmpdir, "temp.pbm")
        svg_path = os.path.join(tmpdir, "output.svg")

        # write input image
        with open(input_path, "wb") as f:
            f.write(image_bytes)

        # read image
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            raise ValueError("Image invalide")

        # binarisation (IMPORTANT pour PDF417)
        _, bw = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

        # save PBM (format requis par potrace)
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

        # read SVG result
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        return svg_data
