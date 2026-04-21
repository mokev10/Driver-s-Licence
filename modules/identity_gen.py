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
# CSS (FULL FIX RENDER + ISOLATION HTML + ANTI BRUIT STREAMLIT)
# =========================
st.markdown(
"""
<style>

/* ================= ANIMATIONS ================= */
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

/* ================= FIX BRUIT STREAMLIT + ISOLATION TOTAL ================= */

#floating-menu-wrapper {
    position: relative;
    z-index: 9999;
    isolation: isolate;
    contain: layout style paint;
}

.floating-menu {
    width: 100%;
    max-width: 750px;
    margin-top: 20px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    font-family: monospace;
    transform: translateZ(0);
    will-change: transform;
    backface-visibility: hidden;
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
    transition: 0.2s ease;
}

.close-btn:hover {
    transform: scale(1.2);
}

.menu-body {
    padding: 16px;
    color: white;
    contain: layout style paint;
}

/* ================= MODIFICATION POUR CENTRER ================= */
.param-box {
    margin-bottom: 14px;
    padding: 15px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    
    /* Centrage du contenu */
    display: flex;
    flex-direction: column;
    align-items: center; 
    text-align: center;
}

.param-box input,
.param-box select {
    width: 100%;
    max-width: 300px; /* Limite la largeur pour un meilleur aspect centré */
    margin-top: 10px;
    padding: 8px;
    border-radius: 6px;
    border: none;
    outline: none;
    background: #1f2937;
    color: white;
    text-align: center; /* Centre le texte à l'intérieur des inputs */
}

/* Style spécifique pour les checkboxes pour les garder centrées */
.param-box input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.param-box small {
    color: #9ca3af;
    font-size: 12px;
    display: block;
    margin-top: 4px;
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
            "step1": "Step 1: Select country and region",
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
            "padding": "Padding (quiet zone)",
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

    icon = (
        "https://icons8.com"
        if country == "United States"
        else "https://icons8.com"
    )

    st.markdown(
        f"""
        <div class="step-animated overlay-box">
            <div style="display:flex;align-items:center;gap:10px;justify-content:center;">
                <img src="{icon}" width="24">
                <h3 style="margin:0;">{t["step1"]}</h3>
            </div>
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

    # ================= STEP 2 =================
    st.markdown(
        f"""
        <div class="step-animated-delay-1 overlay-box" style="text-align:center;">
            <h3>{t["step2"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

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

    # ================= STEP 3 HTML (FIXED & CENTERED) =================
    escape = st.checkbox(t["escape"], value=True)

    st.markdown(
        f"""
        <div id="floating-menu-wrapper">
            <div class="floating-menu">
                <div class="menu-header">
                    <span>{t["step3"]}</span>
                    <span class="close-btn">✕</span>
                </div>
                <div class="menu-body">
                    <div class="param-box">
                        <b>{t["escape"]}</b>
                        <small>{t["escape_help"]}</small>
                        <input type="checkbox" {"checked" if escape else ""}>
                    </div>
                    <div class="param-box">
                        <b>{t["human"]}</b>
                        <input type="checkbox">
                    </div>
                    <div class="param-box">
                        <b>{t["module"]}</b>
                        <input type="text" value="0.254">
                    </div>
                    <div class="param-box">
                        <b>{t["dpi"]}</b>
                        <input type="text" value="600">
                    </div>
                    <div class="param-box">
                        <b>{t["format"]}</b>
                        <select>
                            <option value="PNG">PNG</option>
                            <option value="SVG">SVG</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["generate"]):
        st.success(t["success"])

# Exécution
if __name__ == "__main__":
    show_identity_gen()
