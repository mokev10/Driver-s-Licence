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
# CSS GLOBAL
# =========================
st.markdown(
    """
    <style>

    .overlay-box {
        padding: 14px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* =========================
       FLOATING MENU PANEL
       ========================= */
    .floating-menu {
        position: relative;
        background: rgba(20,20,20,0.85);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 15px;
    }

    .menu-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .close-btn {
        cursor: pointer;
        padding: 4px 10px;
        border-radius: 8px;
        background: rgba(255,0,0,0.15);
        color: white;
        font-weight: bold;
    }

    .close-btn:hover {
        background: rgba(255,0,0,0.35);
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

            "step1": "Step 1: Select country / region",
            "country": "Country",
            "state": "State",
            "prov": "Province",

            "step2": "Step 2: Identity fields",

            "step3": "Step 3: PDF417 Config Panel",

            "generate": "GENERATE BARCODE & STRING",
            "success": "Generation completed",

            "settings": "PDF417 Settings",
            "escape": "Escape sequences",
            "eval": "Evaluate escape sequences (\\n \\t \\F)",
            "human": "Human readable text",
            "dpi": "Resolution (DPI)",
            "module": "Module width: 0.254 mm",
            "format": "Image format",

            "preview": "Preview",
            "png": "Download PNG",
            "svg": "Download SVG",

            "close": "Close"
        },
        "FR": {
            "title": "Générateur AAMVA",
            "desc": "Générateur forensic PDF417",

            "step1": "Étape 1 : Pays / région",
            "country": "Pays",
            "state": "État",
            "prov": "Province",

            "step2": "Étape 2 : Données identité",

            "step3": "Étape 3 : Panneau PDF417",

            "generate": "GÉNÉRER CODE-BARRES & CHAÎNE",
            "success": "Génération terminée",

            "settings": "Paramètres PDF417",
            "escape": "Séquences d'échappement",
            "eval": "Évaluer les séquences (\\n \\t \\F)",
            "human": "Texte lisible humain",
            "dpi": "Résolution (DPI)",
            "module": "Largeur module : 0.254 mm",
            "format": "Format image",

            "preview": "Aperçu",
            "png": "Télécharger PNG",
            "svg": "Télécharger SVG",

            "close": "Fermer"
        }
    }

    t = TEXT[lang]

    # =========================
    # HEADER
    # =========================
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

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.markdown(f"<div class='overlay-box'><h3>{t['step1']}</h3></div>", unsafe_allow_html=True)

    st.divider()

    # =========================
    # IDENTITY FIELDS
    # =========================
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

    # =========================
    # FLOATING PDF417 MENU
    # =========================
    if "menu_open" not in st.session_state:
        st.session_state.menu_open = True

    if st.session_state.menu_open:

        st.markdown(f"""
        <div class="floating-menu">

            <div class="menu-header">
                <strong>{t['settings']}</strong>
                <div class="close-btn">{t['close']}</div>
            </div>

        </div>
        """, unsafe_allow_html=True)

        colS1, colS2 = st.columns(2)

        with colS1:
            escape_sequences = st.checkbox(t["escape"], value=True)
            eval_escape = st.checkbox(t["eval"], value=True)
            human = st.checkbox(t["human"], value=False)

        with colS2:
            dpi = st.number_input(t["dpi"], 72, 1200, 600, 50)
            format_img = st.selectbox(t["format"], ["PNG", "SVG"])

        st.markdown(f"- {t['module']}")

    st.divider()

    # =========================
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            display = raw.replace("\n", "\\n") if escape_sequences else raw

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.code(display)

            codes = encode(raw, columns=10)
            image = render_image(codes, scale=3, padding=3)

            buf = io.BytesIO()
            image.save(buf, format="PNG", dpi=(dpi, dpi))
            png_bytes = buf.getvalue()

            with col2:
                st.image(png_bytes)

                st.download_button(t["png"], png_bytes, file_name=f"{dcs}.png")

                if format_img == "SVG":
                    svg = png_to_svg(png_bytes, shutil.which("potrace"))
                    st.download_button(t["svg"], svg, file_name=f"{dcs}.svg")

        except Exception:
            st.error(traceback.format_exc())
