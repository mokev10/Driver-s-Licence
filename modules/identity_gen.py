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
# CSS (CENTRAGE + ANIMATIONS + BANDEAU STEP 1 + RÉSULTAT)
# =========================
st.markdown(
"""
<style>
/* --- CENTRAGE GLOBAL --- */
.stApp h1, .stApp p, .stApp div.stMarkdown {
    text-align: center;
}

[data-testid="column"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.stTextInput, .stSelectbox, .stCheckbox {
    width: 100% !important;
    max-width: 450px !important;
}

/* --- ANIMATIONS --- */
@keyframes slideUp {
    from { transform: translateY(80px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}
.step-animated { animation: slideUp 0.8s ease-out; }

/* BANDEAU STYLE IMAGE */
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

/* ZONE RÉSULTAT STYLISÉE */
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
    word-break: break-all;
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

/* --- MENU PARAMÈTRES STEP 3 --- */
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

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # --- ÉTAPE 1 ---
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

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

    st.markdown(
        f"""
        <div class="step-animated step-banner">
            <img src="{icon}" width="35" height="35" style="margin-right: 15px;">
            <span style="font-size: 20px; font-weight: bold; color: #FFFFFF;">{t["step1"]}</span>
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
                <div class="menu-header"><span>{t["step3"]}</span><span style="color:#ff4d4d; font-weight:bold; cursor:pointer;">✕</span></div>
                <div class="menu-body">
                    <div class="param-box"><b>{t["escape"]}</b><small>{t["escape_help"]}</small><input type="checkbox" {"checked" if escape else ""}></div>
                    <div class="param-box"><b>{t["human"]}</b><input type="checkbox"></div>
                    <div class="param-box"><b>{t["module"]}</b><input type="text" value="0.254"></div>
                    <div class="param-box"><b>{t["dpi"]}</b><input type="text" value="600"></div>
                    <div class="param-box"><b>{t["format"]}</b><select><option>PNG</option><option>SVG</option></select></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # BOUTON ET LOGIQUE DE GÉNÉRATION
    _, col_btn, _ = st.columns([1, 1.5, 1])
    with col_btn:
        generate_clicked = st.button(t["generate"], use_container_width=True)

    if generate_clicked:
        # 1. Construction de la chaîne ANSI (Exemple)
        ansi_data = f"@\n\nANSI {mock_iin}DL{dcf}\nDCG{dcg}\nDAC{dac}\nDCS{dcs}\nDBB{dbb}\nDAQ{daq}\nDAG{dag}\nDAI{dai}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\n"
        
        st.success(t["success"])
        
        # 2. ZONE DE RÉSULTAT (CONTENU RÉTABLI)
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        st.write("### Generated ANSI String")
        st.markdown(f'<div class="ansi-box">{ansi_data.replace("\\n", "<br>")}</div>', unsafe_allow_html=True)
        
        st.write("### PDF417 Barcode")
        try:
            # Génération réelle du code-barres
            codes = encode(ansi_data)
            image = render_image(codes)
            
            # Affichage dans un conteneur blanc
            st.markdown('<div class="barcode-white-bg">', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Boutons de téléchargement
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            st.download_button("Download PNG", buf.getvalue(), "barcode.png", "image/png")
            
        except Exception as e:
            st.error(f"Error generating barcode: {e}")
            st.code(traceback.format_exc())
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_identity_gen()
