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
# CSS ANIMATION + MENU FLOATING
# =========================
st.markdown(
"""
<style>

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
.step-animated-delay-2 { animation: slideUp 1.2s ease-out; }
.step-fade { animation: fadeIn 1.5s ease-in; }

.overlay-box {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
}

/* FLOATING MENU */

.floating-menu {
    position: relative;
    width: 100%;
    max-width: 700px;
    margin-top: 20px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
}

.menu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    background: #111827;
    color: #ffffff;
    font-weight: bold;
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.close-btn {
    cursor: pointer;
    color: #ff4d4d;
    font-size: 16px;
    font-weight: bold;
}

.menu-body {
    padding: 16px;
    color: white;
    font-family: monospace;
}

.param-box {
    margin-bottom: 14px;
    padding: 10px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
}

.param-box input,
.param-box select {
    width: 100%;
    margin-top: 6px;
    padding: 6px;
    border-radius: 6px;
    border: none;
    background: #1f2937;
    color: white;
}

.param-box small {
    color: #9ca3af;
    font-size: 12px;
}

</style>
""",
unsafe_allow_html=True
)


# =========================
# FUNCTION
# =========================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced tool for generating forensic-quality AAMVA raw data strings",
            "step1": "Step 1: Select country",
            "country": "Select Country",
            "state": "State",
            "prov": "Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Barcode Parameters",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed.",
            "escape": "Escape Sequences",
            "escape_help": "Replace line breaks with \\n",
            "human": "Human readable text",
            "module": "Module width (mm)",
            "dpi": "Resolution (DPI)",
            "format": "Image format",
            "padding": "Padding"
        }
    }

    t = TEXT["EN"]

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    st.markdown(
        f"""
        <div class="step-animated overlay-box">
            <img src="{icon}" width="24"> {t["step1"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

    # INPUTS
    colA, colB = st.columns(2)

    with colA:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")

    with colB:
        dai = st.text_input("DAI", "CITY")
        dak = st.text_input("DAK", "POSTAL")

    # FLOATING MENU (CORRECT)
    st.markdown(
"""
<div class="floating-menu">
    <div class="menu-header">
        <span>Step 3: Barcode Parameters</span>
        <span class="close-btn">X</span>
    </div>

    <div class="menu-body">

        <div class="param-box">
            <b>Escape Sequences</b><br>
            <small>Replace line breaks with \\n</small><br>
            <input type="checkbox" checked>
        </div>

        <div class="param-box">
            <b>Human readable text</b><br>
            <input type="checkbox">
        </div>

        <div class="param-box">
            <b>Module width (mm)</b><br>
            <input type="text" value="0.254">
        </div>

        <div class="param-box">
            <b>Resolution (DPI)</b><br>
            <input type="text" value="600">
        </div>

        <div class="param-box">
            <b>Image format</b><br>
            <select>
                <option>PNG</option>
                <option>SVG</option>
            </select>
        </div>

        <div class="param-box">
            <b>Padding</b><br>
            <input type="text" value="3">
        </div>

    </div>
</div>
""",
unsafe_allow_html=True
)
