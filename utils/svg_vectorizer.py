import cv2
import subprocess
import os
import tempfile


def png_to_svg(png_bytes, potrace_path, threshold=180):
    """
    Convertit une image PNG (PDF417) en SVG vectoriel via OpenCV + Potrace
    """

    if not png_bytes:
        raise ValueError("PNG data is empty")

    # 📁 dossier temporaire isolé
    tmp_dir = tempfile.mkdtemp()

    png_path = os.path.join(tmp_dir, "input.png")
    pbm_path = os.path.join(tmp_dir, "input.pbm")
    svg_path = os.path.join(tmp_dir, "output.svg")

    try:
        # 💾 sauvegarde PNG
        with open(png_path, "wb") as f:
            f.write(png_bytes)

        # 🖼️ lecture image
        img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            raise ValueError("Impossible de lire l'image PNG")

        # ⚫⚪ binarisation stricte (IMPORTANT pour PDF417)
        _, bw = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

        # 💾 PBM (format obligatoire Potrace)
        cv2.imwrite(pbm_path, bw)

        # ⚙️ vectorisation Potrace
        subprocess.run([
            potrace_path,
            pbm_path,
            "-s",
            "-o",
            svg_path
        ], check=True)

        # 📄 lecture SVG final
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        return svg_data

    finally:
        # 🧹 nettoyage total
        for path in [png_path, pbm_path, svg_path]:
            if os.path.exists(path):
                os.remove(path)

        if os.path.exists(tmp_dir):
            try:
                os.rmdir(tmp_dir)
            except:
                pass
