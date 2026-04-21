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
# CSS COMPLET (NE PAS SIMPLIFIER)
# =========================
st.markdown(
"""
<style>

/* ANIMATIONS */
@keyframes slideUp {
    from { transform: translateY(80px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.step-animated { animation: slideUp 0.8s ease-out; }
.step-animated-delay-1 { animation: slideUp 1.0s ease-out; }
.step-fade { animation: fadeIn 1.5s ease-in; }

.overlay-box {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
}

/* BUTTON STYLE GLOBAL */
.stButton > button {
    background: linear-gradient(135deg, #4facfe 0%, #a066ff 100%) !important;
    color: white !important;
    border: none !important;
    padding: 10px 25px !important;
    border-radius: 50px !important;
    font-weight: bold !important;
    box-shadow: 0 0 15px rgba(160, 102, 255, 0.5) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(160, 102, 255, 0.8) !important;
}

/* FLOATING MENU */
.floating-menu {
    margin-top: 20px;
    background: #111827;
    border-radius: 16px;
    border: 1px solid #2a2f3a;
    box-shadow: 0 15px 40px rgba(0,0,0,0.5);
    overflow: hidden;
}

.menu-header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding: 12px 16px;
    background:#0b1220;
    color:white;
    font-weight:600;
}

.menu-body {
    padding: 18px;
    color: white;
}

.close-btn {
    background:red;
    padding:2px 10px;
    border-radius:8px;
    cursor:pointer;
}

/* ANSI BOX */
.ansi-box {
    background:#1a1a1a;
    color:#00ff88;
    padding:12px;
    border-radius:8px;
    font-family: monospace;
    white-space: pre-wrap;
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
            "desc": "Advanced forensic PDF417 generator",
            "step1": "Step 1: Select country and region",
            "country": "Country",
            "state": "State",
            "prov": "Province",
            "step2": "Step 2: Required fields",
            "step3": "Step 3: PDF417 Parameters",
            "generate": "GENERATE BARCODE & STRING",
            "success": "Generation completed",
            "raw": "PDF417 noise data",
            "escape": "Escape Sequences",
            "escape_desc": "Convert line breaks to \\n",
            "hr": "Human readable text",
            "module": "Module width (mm)",
            "dpi": "Resolution (DPI)",
            "format": "Image format",
            "padding": "Padding (quiet zone)"
        }
    }

    t = TEXT[lang]

    # =========================
    # HEADER
    # =========================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # =========================
    # COUNTRY
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], ["AL", "CA", "NY"])
            mock_iin = "636033"
        else:
            region = st.selectbox(t["prov"], ["QC", "ON"])
            mock_iin = "636038"

    st.divider()

    # =========================
    # INPUTS (NE PAS MODIFIER STRUCTURE)
    # =========================
    colA, colB = st.columns(2)

    with colA:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D982094120896")
        dag = st.text_input("DAG", "1560 SHERBROOKE ST E")

    with colB:
        dai = st.text_input("DAI", "MONTREAL")
        dak = st.text_input("DAK", "H2L4M1")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")
        dbc = st.selectbox("DBC", ["1", "2", "3"])
        dcf = st.text_input("DCF", "REF001")

    st.divider()

    # =========================
    # FLOATING MENU (FULL STRUCTURE FIXED)
    # =========================
    st.markdown(f"""
    <div class="floating-menu">

        <div class="menu-header">
            <span>{t["step3"]}</span>
            <span class="close-btn">X</span>
        </div>

        <div class="menu-body">

            <b>{t["escape"]}</b><br>
            <small>{t["escape_desc"]}</small><br>
            <input type="checkbox" checked> ON/OFF<br><br>

            <b>{t["hr"]}</b><br>
            <input type="checkbox"><br><br>

            <b>{t["module"]}</b><br>
            <input type="text" value="0.254 mm"><br><br>

            <b>{t["dpi"]}</b><br>
            <input type="text" value="600 DPI"><br><br>

            <b>{t["format"]}</b><br>
            <select>
                <option>PNG</option>
                <option>SVG</option>
            </select><br><br>

            <b>{t["padding"]}</b><br>
            <small>Quiet zone around barcode for scan reliability</small><br>
            <input type="text" value="3">

        </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # GENERATE (RAW STRICT IDENTICAL)
    # =========================
    if st.button(t["generate"], use_container_width=True):

        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

        raw = (
            f"@\n{aamva_header}\n"
            f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
            f"DAG{dag}\nDAI{dai}\nDAJ{region}\nDAK{dak}\n"
            f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        )

        st.success(t["success"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="ansi-box">
{raw}
            </div>
            """, unsafe_allow_html=True)

        codes = encode(raw, columns=10)
        image = render_image(codes, scale=3, padding=3)

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        with col2:
            st.image(png_bytes)
            st.download_button("PNG", png_bytes, file_name=f"{dcs}.png", mime="image/png")

            try:
                potrace_path = shutil.which("potrace")
                if potrace_path:
                    svg = png_to_svg(png_bytes, potrace_path)
                    st.download_button("SVG", svg, file_name=f"{dcs}.svg", mime="image/svg+xml")
            except:
                pass
