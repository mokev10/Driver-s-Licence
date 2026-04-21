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
# CSS (CENTRAGE GLOBAL + ANIMATIONS + ISOLATION)
# =========================
st.markdown(
"""
<style>
/* --- CENTRAGE GLOBAL --- */
.stApp h1, .stApp p, .stApp div.stMarkdown {
    text-align: center;
}

/* Centrage des colonnes Streamlit */
[data-testid="column"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Centrage et taille des inputs natifs */
.stTextInput, .stSelectbox, .stCheckbox {
    width: 100% !important;
    max-width: 450px !important;
}

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
    width: 100%;
    max-width: 950px;
    margin: 10px auto;
}

/* ================= FIX BRUIT STREAMLIT + CENTRAGE MENU ================= */

#floating-menu-wrapper {
    display: flex;
    justify-content: center;
    position: relative;
    z-index: 9999;
    isolation: isolate;
    contain: layout style paint;
    width: 100%;
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
    display: flex;
    flex-direction: column;
    align-items: center;
    contain: layout style paint;
}

.param-box {
    width: 100%;
    max-width: 550px;
    margin-bottom: 14px;
    padding: 15px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.param-box input,
.param-box select {
    width: 100%;
    max-width: 300px;
    margin-top: 10px;
    padding: 8px;
    border-radius: 6px;
    border: none;
    outline: none;
    background: #1f2937;
    color: white;
    text-align: center;
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
            "padding": "Padding (quiet zone)",
            "success": "HDR generation completed"
        }
    }

    t = TEXT["EN"]

    # ================= HEADER =================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # --- ÉTAPE 1 (SÉLECTEURS EN HAUT COMME SUR L'IMAGE) ---
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    # LOGIQUE ICONE DYNAMIQUE
    icon = (
        "https://icons8.com"
        if country == "United States"
        else "https://icons8.com"
    )

    # BANDEAU D'ÉTAPE EN DESSOUS DES SÉLECTEURS
    st.markdown(
        f"""
        <div class="step-animated overlay-box">
            <div style="display:flex;align-items:center;gap:15px;padding-left:10px;">
                <img src="{icon}" style="width:32px; height:32px;">
                <h3 style="margin:0; font-size:18px; color:white;">{t["step1"]}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ================= STEP 2 =================
    st.markdown(
        f"""
        <div class="step-animated-delay-1 overlay-box">
            <h3>{t["step2"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centrage des colonnes de saisie
    _, colA, colB, _ = st.columns([0.1, 2, 2, 0.1])

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

    # ================= STEP 3 =================
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
    
    # BOUTON GENERATE
    _, col_btn, _ = st.columns([1.5, 1, 1.5])
    with col_btn:
        if st.button(t["generate"], use_container_width=True):
            st.success(t["success"])

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    show_identity_gen()
