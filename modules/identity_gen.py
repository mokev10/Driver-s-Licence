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
# CSS (CENTRAGE GLOBAL ET STYLISATION)
# =========================
st.markdown(
"""
<style>
/* Centrer le titre et la description */
.stApp h1, .stApp p, .stApp div.stMarkdown {
    text-align: center;
}

/* Centrer les colonnes Streamlit */
[data-testid="column"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Forcer le centrage des inputs natifs */
.stTextInput, .stSelectbox, .stCheckbox {
    width: 100% !important;
    max-width: 400px !important;
}

/* ================= ANIMATIONS ================= */
@keyframes slideUp {
    from { transform: translateY(80px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

.step-animated { animation: slideUp 0.8s ease-out; }

.overlay-box {
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
}

/* ================= MENU FLOTTANT CENTRÉ ================= */
#floating-menu-wrapper {
    display: flex;
    justify-content: center;
    width: 100%;
    isolation: isolate;
}

.floating-menu {
    width: 100%;
    max-width: 750px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    font-family: monospace;
}

.menu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    background: #111827;
    color: #ffffff;
}

.menu-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.param-box {
    width: 100%;
    max-width: 500px;
    margin-bottom: 14px;
    padding: 15px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.param-box input, .param-box select {
    width: 100%;
    max-width: 300px;
    margin-top: 10px;
    padding: 8px;
    background: #1f2937;
    color: white;
    text-align: center;
    border-radius: 6px;
    border: none;
}
</style>
""",
unsafe_allow_html=True
)


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
            "success": "HDR generation completed"
        }
    }
    t = TEXT["EN"]

    # --- TITRES CENTRÉS ---
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # --- ÉTAPE 1 : Centrage avec colonnes vides (layout 1:2:1) ---
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        country = st.selectbox(t["country"], ["United States", "Canada"])
    
    icon_url = (
        "https://icons8.com"
        if country == "United States"
        else "https://icons8.com"
    )

    st.markdown(
        f"""
        <div class="step-animated overlay-box">
            <div style="display:flex;align-items:center;gap:10px;justify-content:center;">
                <img src="{icon_url}" width="24">
                <h3 style="margin:0;">{t["step1"]}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    _, center_col_2, _ = st.columns([1, 2, 1])
    with center_col_2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))

    st.divider()

    # --- ÉTAPE 2 : Champs de saisie ---
    st.markdown(f'<div class="overlay-box"><h3>{t["step2"]}</h3></div>', unsafe_allow_html=True)
    
    # Pour centrer les deux colonnes de saisie au milieu de l'écran
    _, colA, colB, _ = st.columns([0.5, 2, 2, 0.5])

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

    # --- ÉTAPE 3 : Menu Barcode Centré ---
    escape = st.checkbox(t["escape"], value=True)

    st.markdown(
        f"""
        <div id="floating-menu-wrapper">
            <div class="floating-menu">
                <div class="menu-header">
                    <span>{t["step3"]}</span>
                    <span style="color:#ff4d4d; cursor:pointer;">✕</span>
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

    # Bouton de génération centré
    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button(t["generate"], use_container_width=True):
            st.success(t["success"])

if __name__ == "__main__":
    show_identity_gen()
