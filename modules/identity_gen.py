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
# CSS (CENTRAGE + ANIMATIONS + BANDEAU STEP 1)
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

/* Taille des inputs natifs */
.stTextInput, .stSelectbox, .stCheckbox {
    width: 100% !important;
    max-width: 450px !important;
}

/* ================= ANIMATIONS ================= */
@keyframes slideUp {
    from { transform: translateY(80px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

.step-animated { animation: slideUp 0.8s ease-out; }

/* BANDEAU STYLE IMAGE (SOMBRE ET LARGE) */
.step-banner {
    padding: 20px;
    border-radius: 10px;
    background: #111418;
    border: 1px solid #1E2227;
    width: 100%;
    margin: 15px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start; /* Aligné à gauche comme l'image */
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

/* ================= MENU PARAMÈTRES STEP 3 ================= */
#floating-menu-wrapper {
    display: flex;
    justify-content: center;
    width: 100%;
    position: relative;
    z-index: 9999;
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
    color: white;
}

.menu-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.param-box {
    width: 100%;
    max-width: 550px;
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

    # --- TITRES ---
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # --- ÉTAPE 1 : SÉLECTEURS EN HAUT ---
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    # LOGIQUE ICONE (TES LIENS)
    icon = (
        "https://icons8.com"
        if country == "United States"
        else "https://icons8.com"
    )

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    # BANDEAU D'ÉTAPE EN DESSOUS (COMME TON IMAGE)
    st.markdown(
        f"""
        <div class="step-animated step-banner">
            <img src="{icon}" width="35" height="35" style="margin-right: 15px; vertical-align: middle;">
            <span style="font-size: 20px; font-weight: bold; color: #FFFFFF; font-family: sans-serif;">
                {t["step1"]}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --- ÉTAPE 2 ---
    st.markdown(f'<div class="overlay-box-step2"><h3>{t["step2"]}</h3></div>', unsafe_allow_html=True)
    
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

    # --- ÉTAPE 3 ---
    escape = st.checkbox(t["escape"], value=True)
    st.markdown(
        f"""
        <div id="floating-menu-wrapper">
            <div class="floating-menu">
                <div class="menu-header">
                    <span>{t["step3"]}</span>
                    <span style="color:#ff4d4d; cursor:pointer; font-weight:bold;">✕</span>
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
                        <select><option>PNG</option><option>SVG</option></select>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button(t["generate"], use_container_width=True):
            st.success(t["success"])

if __name__ == "__main__":
    show_identity_gen()
