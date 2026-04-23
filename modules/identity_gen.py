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
# STYLE GLOBAL LIQUID GLASS + FIX DARK MODE EXPANDER
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

    /* =========================
       EXPANDER FIX COMPLET
    ========================== */

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
    details[data-testid="stExpander"] summary p {
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

    /* =========================
       SVG FIX DARK MODE
    ========================== */

    .barcode-preview-box {
        padding: 15px;
        display: flex;
        justify-content: center;
        background: transparent !important;
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

    /* =========================
       BOUTONS HOVER CLEAN
    ========================== */

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 45px rgba(129,34,255,0.4) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# LOGIQUE MÉTIER
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

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

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

    if st.button(ui["generate"], use_container_width=True):

        try:
            raw_string = "@\nSAMPLE DATA\nDCGTEST\nDCSUSER"

            st.success(ui["success"])
            st.divider()

            st.subheader(ui["preview"])

            svg_fake = "<svg width='200' height='80'><rect width='200' height='80' fill='white'/></svg>"

            with st.expander("DETAILED VECTOR INSPECTION"):
                st.markdown(
                    f'<div class="barcode-preview-box">{svg_fake}</div>',
                    unsafe_allow_html=True
                )

        except Exception:
            st.error("CRITICAL SYSTEM FAILURE")
            st.code(traceback.format_exc())
