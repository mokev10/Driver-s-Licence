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
# CSS (IDENTIQUE - NE PAS TOUCHER)
# =========================
st.markdown(
"""
<style>

@keyframes slideUp {
    from { transform: translateY(80px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

.step-animated { animation: slideUp 0.8s ease-out; }

.step-banner {
    padding: 20px;
    border-radius: 10px;
    background: #111418;
    border: 1px solid #1E2227;
    width: 100%;
    margin: 15px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
}

.overlay-box-step2 {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    width: 100%;
    max-width: 950px;
    margin: 10px auto;
}

.result-card {
    background: #1A1C1E;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #30363D;
    margin-top: 20px;
    width: 100%;
}

.ansi-box {
    background: #000000;
    color: #00FF00;
    font-family: 'Roboto Mono', monospace;
    padding: 15px;
    border-radius: 8px;
    font-size: 13px;
    white-space: pre-wrap;   /* ⭐ FIX IMPORTANT ANTI "BRUIT" */
    text-align: left !important;
    border: 1px solid #333;
}

.barcode-white-bg {
    background: white;
    padding: 20px;
    border-radius: 8px;
    display: inline-block;
    margin-top: 15px;
}

/* FLOATING MENU */
.floating-menu {
    width: 100%;
    max-width: 750px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
}

.menu-header {
    display: flex;
    justify-content: space-between;
    padding: 14px;
    background: #111827;
    color: white;
}

.menu-body {
    padding: 16px;
}

.param-box {
    margin-bottom: 12px;
    padding: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
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
            "desc": "Advanced tool for generating forensic-quality AAMVA raw data strings",
            "step1": "Step 1: Select the country and state or province",
            "country": "Select Country",
            "state": "Select State",
            "prov": "Select Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Barcode Parameters",
            "generate": "GENERATE BARCODE & STRING",
            "escape": "Escape Sequences",
            "escape_help": "Use \\n for line breaks",
            "human": "Human readable text",
            "module": "Module width (mm)",
            "dpi": "Resolution (DPI)",
            "format": "Image format",
            "success": "HDR generation completed"
        }
    }

    t = TEXT["EN"]

    # ================= HEADER =================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    # ⭐ ICON RESTAURÉ EXACTEMENT (NON SIMPLIFIÉ)
    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.markdown(
        f"""
        <div class="step-animated step-banner">
            <img src="{icon}" width="35" style="margin-right:10px;">
            <b style="color:white;">{t["step1"]}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ================= STEP 2 =================
    st.markdown(f'<div class="overlay-box-step2"><h3>{t["step2"]}</h3></div>', unsafe_allow_html=True)

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

    # ================= STEP 3 MENU =================
    st.markdown(
        f"""
        <div class="floating-menu">
            <div class="menu-header">
                <span>{t["step3"]}</span>
                <span>✕</span>
            </div>

            <div class="menu-body">

                <div class="param-box">
                    <b>{t["escape"]}</b><br>
                    <small>{t["escape_help"]}</small><br>
                    <input type="checkbox" checked>
                </div>

                <div class="param-box">
                    <b>{t["human"]}</b><br>
                    <input type="checkbox">
                </div>

                <div class="param-box">
                    <b>{t["module"]}</b><br>
                    <input type="text" value="0.254">
                </div>

                <div class="param-box">
                    <b>{t["dpi"]}</b><br>
                    <input type="text" value="600">
                </div>

                <div class="param-box">
                    <b>{t["format"]}</b><br>
                    <select>
                        <option>PNG</option>
                        <option>SVG</option>
                    </select>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ================= GENERATION =================
    if st.button(t["generate"], use_container_width=True):

        try:
            ansi_data = (
                "@\n"
                f"ANSI {mock_iin}DL{dcf}\n"
                f"DCG{dcg}\nDAC{dac}\nDCS{dcs}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\n"
            )

            st.success(t["success"])

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.write("### PDF417 noise data")

            # ⭐ FIX IMPORTANT: plus de "bruit HTML"
            st.markdown(f'<div class="ansi-box">{ansi_data}</div>', unsafe_allow_html=True)

            st.write("### Barcode")

            codes = encode(ansi_data)
            image = render_image(codes)

            buf = io.BytesIO()
            image.save(buf, format="PNG")

            st.image(buf.getvalue(), use_container_width=True)

            st.download_button("PNG", buf.getvalue(), file_name="barcode.png")

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())


if __name__ == "__main__":
    show_identity_gen()
