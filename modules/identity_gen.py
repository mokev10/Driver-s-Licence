import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# PATH FIX
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =========================
# IMPORTS
# =========================
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# CSS CLEAN (NO HTML FLOATING)
# =========================
st.markdown(
"""
<style>

.step-animated { animation: fadeIn 0.8s ease-out; }

.overlay-box {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
}

/* PANEL STYLE (STREAMLIT ONLY) */
.panel {
    padding: 16px;
    border-radius: 16px;
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    color: white;
    margin-top: 10px;
}

.small {
    font-size: 12px;
    color: #9ca3af;
}

</style>
""",
unsafe_allow_html=True
)


# =========================
# MAIN FUNCTION
# =========================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced forensic barcode generator",
            "step1": "Step 1: Country selection",
            "step2": "Step 2: Required fields",
            "step3": "Step 3: Barcode parameters",
            "generate": "GENERATE",

            "escape": "Escape sequences",
            "human": "Human readable text",
            "module": "Module width (mm)",
            "dpi": "Resolution (DPI)",
            "format": "Image format",
            "padding": "Quiet zone",
            "success": "Generation completed"
        }
    }

    t = TEXT["EN"]

    # ================= HEADER =================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # ================= STEP 1 =================
    st.markdown(f"### {t['step1']}")

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("Country", ["United States", "Canada"])

    if country == "United States":
        region = st.selectbox("State", sorted(IIN_US.keys()))
        mock_iin = IIN_US[region]
    else:
        region = st.selectbox("Province", sorted(IIN_CA.keys()))
        mock_iin = IIN_CA[region]

    st.divider()

    # ================= STEP 2 =================
    st.markdown(f"### {t['step2']}")

    colA, colB = st.columns(2)

    with colA:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D9823415")
        dag = st.text_input("DAG", "1560 STREET")

    with colB:
        dai = st.text_input("DAI", "CITY")
        dak = st.text_input("DAK", "POSTAL")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")
        dbc = st.selectbox("DBC", ["1", "2", "3"])
        dcf = st.text_input("DCF", "REF001")

    st.divider()

    # ================= STEP 3 (CLEAN PANEL) =================
    st.markdown(f"### {t['step3']}")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        escape = st.checkbox("Escape sequences (\\n)", value=True)
        human = st.checkbox("Human readable text")

        module = st.text_input("Module width (mm)", "0.254")
        dpi = st.text_input("Resolution (DPI)", "600")

        fmt = st.selectbox("Image format", ["PNG", "SVG"])
        padding = st.text_input("Quiet zone", "3")

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ================= GENERATION =================
    if st.button(t["generate"], use_container_width=True):

        try:
            header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            raw = (
                f"@\n{header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            display_raw = raw.replace("\n", "\\n") if escape else raw

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.code(display_raw)

            codes = encode(raw, columns=10)
            image = render_image(codes, scale=3, padding=int(padding))

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            with col2:
                st.image(png_bytes)
                st.download_button("Download PNG", png_bytes, file_name=f"{dcs}.png")

                potrace_path = shutil.which("potrace")
                svg = None

                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes, potrace_path)
                    except:
                        pass

                if svg:
                    st.download_button("Download SVG", svg, file_name=f"{dcs}.svg")

                    if fmt == "SVG":
                        st.markdown(svg, unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
