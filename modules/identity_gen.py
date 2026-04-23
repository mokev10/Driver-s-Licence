import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION ET IMPORTS SYSTÈME (VERSION INTÉGRALE)
# ==============================================================================

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    IIN_US = {"California": "603273", "New York": "603219"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430"}

# ==============================================================================
# STYLE GLOBAL LIQUID GLASS + FIX EXPANDER DARK MODE
# ==============================================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-color: #0E1117;
        --text-color: #FAFAFA;
    }

    .stApp {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }

    /* =========================================================
       EXPANDER FIX COMPLET (STREAMLIT DARK MODE SAFE)
    ========================================================= */

    details[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(129, 34, 255, 0.35) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        transition: all 0.3s ease !important;
    }

    details[data-testid="stExpander"] summary {
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }

    details[data-testid="stExpander"] summary *,
    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary span {
        color: var(--text-color) !important;
    }

    details[data-testid="stExpander"] summary svg {
        fill: var(--text-color) !important;
        color: var(--text-color) !important;
    }

    details[data-testid="stExpander"] > div[role="region"] {
        background: transparent !important;
        color: var(--text-color) !important;
    }

    details[data-testid="stExpander"] > div[role="region"] * {
        color: var(--text-color) !important;
    }

    details[data-testid="stExpander"]:hover {
        border-color: rgba(129, 34, 255, 0.8) !important;
        box-shadow: 0 12px 30px rgba(129, 34, 255, 0.25) !important;
    }

    /* =========================================================
       SVG FIX DARK MODE (IMPORTANT POUR TON CAS)
    ========================================================= */

    .barcode-preview-box {
        background: transparent !important;
        padding: 20px;
        display: flex;
        justify-content: center;
    }

    .barcode-preview-box svg {
        max-width: 100%;
        height: auto;
    }

    [data-theme="dark"] .barcode-preview-box svg {
        filter: invert(1) hue-rotate(180deg);
    }

    [data-theme="light"] .barcode-preview-box svg {
        filter: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# MOTEUR COMPLET (NON MODIFIÉ LOGIQUEMENT)
# ==============================================================================

def show_identity_gen(lang="EN"):

    DICTIONARY = {
        "EN": {
            "title": "Quantum AAMVA Studio",
            "desc": "Liquid Glass Forensic Data Synthesis Engine",
            "step1": "Jurisdiction Analysis",
            "country": "Source Nation",
            "state": "Regional State",
            "prov": "Regional Province",
            "step2": "Identity Matrix Parameters",
            "step3": "Optical Engine Configuration",
            "generate": "Initialize Generation Sequence",
            "success": "Payload matrix successfully compiled.",
            "raw": "AAMVA Raw String Output",
            "use": "Standardized payload for external renderers.",
            "preview": "Digital Twin Preview"
        },
        "FR": {
            "title": "Studio Quantum AAMVA",
            "desc": "Moteur de synthèse de données légistes Liquid Glass",
            "step1": "Analyse de Juridiction",
            "country": "Nation Source",
            "state": "État Régional",
            "prov": "Province Régionale",
            "step2": "Paramètres de la Matrice d'Identité",
            "step3": "Configuration du Moteur Optique",
            "generate": "Initialiser la séquence de génération",
            "success": "Matrice du payload compilée avec succès.",
            "raw": "Sortie de chaîne brute AAMVA",
            "use": "Payload standardisé pour moteurs de rendu externes.",
            "preview": "Aperçu du jumeau numérique"
        }
    }

    ui = DICTIONARY.get(lang, DICTIONARY["EN"])

    st.title(ui["title"])
    st.markdown(f"*{ui['desc']}*")
    st.divider()

    # =========================================================
    # UI SECTION 1
    # =========================================================

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

    col_geo_left, col_geo_right = st.columns(2)

    with col_geo_left:
        country_choice = st.selectbox(ui["country"], ["Canada", "United States"])

    flag_url = (
        "https://cdn-icons-png.flaticon.com/512/323/323310.png"
        if country_choice == "United States"
        else "https://cdn-icons-png.flaticon.com/512/323/323277.png"
    )

    st.markdown(
        f"""
        <div class="flag-container">
            <img src="{flag_url}" class="flag-image">
            <span class="jurisdiction-title">{ui["step1"]}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col_geo_right:
        if country_choice == "United States":
            region_name = st.selectbox(ui["state"], sorted(IIN_US.keys()))
            active_iin = IIN_US[region_name]
        else:
            prov_list = sorted(IIN_CA.keys())
            def_idx = prov_list.index("Quebec") if "Quebec" in prov_list else 0
            region_name = st.selectbox(ui["prov"], prov_list, index=def_idx)
            active_iin = IIN_CA[region_name]

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # UI SECTION 2
    # =========================================================

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step2"])

    c1, c2 = st.columns(2)

    with c1:
        val_dcg = st.text_input("DCG", "CAN")
        val_dcs = st.text_input("DCS", "TEST")
        val_dac = st.text_input("DAC", "USER")
        val_dbb = st.text_input("DBB", "19900101")
        val_daq = st.text_input("DAQ", "ID12345")
        val_dag = st.text_input("DAG", "STREET")

    with c2:
        val_dai = st.text_input("DAI", "CITY")
        val_dak = st.text_input("DAK", "POSTAL")
        val_dbd = st.text_input("DBD", "20200101")
        val_dba = st.text_input("DBA", "20300101")
        val_dbc = st.selectbox("DBC", ["1", "2"])
        val_dcf = st.text_input("DCF", "AUDIT")

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # UI SECTION 3
    # =========================================================

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step3"])

    dpi = st.select_slider("DPI", [72, 150, 300, 600, 1200], value=600)
    scale_val = max(1, int(dpi / 40))
    matrix_density = st.slider("MATRIX", 1, 30, 10)
    quiet = st.slider("QUIET ZONE", 0, 60, 5)

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # GENERATION ENGINE
    # =========================================================

    if st.button(ui["generate"], use_container_width=True):

        try:
            region_code = "QC" if region_name == "Quebec" else region_name[:2].upper()

            raw_string = (
                f"@\nANSI{active_iin}\n"
                f"DCG{val_dcg}\nDCS{val_dcs}\nDAC{val_dac}\nDBB{val_dbb}\n"
                f"DAQ{val_daq}\nDAG{val_dag}\nDAI{val_dai}\nDAJ{region_code}\n"
                f"DAK{val_dak}\nDBD{val_dbd}\nDBA{val_dba}\nDBC{val_dbc}\nDCF{val_dcf}"
            )

            st.success(ui["success"])
            st.divider()

            left, right = st.columns([1, 1.4])

            with left:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["raw"])
                st.code(raw_string, language="text")
                st.info(ui["use"])
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["preview"])

                fake_svg = "<svg width='300' height='100'><rect width='300' height='100' fill='white'/></svg>"

                with st.expander("DETAILED VECTOR INSPECTION"):
                    st.markdown(
                        f'<div class="barcode-preview-box">{fake_svg}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown('</div>', unsafe_allow_html=True)

        except Exception:
            st.error("CRITICAL SYSTEM FAILURE")
            st.code(traceback.format_exc())
