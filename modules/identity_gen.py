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
# ANIMATION CSS (STRICTEMENT CONSERVÉE)
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
        margin-bottom: 10px;
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
            "step1": "Step 1: Region Selection",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Barcode Configuration",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed.",
            "raw": "Raw Data String",
            "preview": "Barcode Preview"
        },
        "FR": {
            "title": "Générateur de données AAMVA",
            "desc": "Outil avancé pour générer des chaînes AAMVA",
            "step1": "Étape 1 : Sélection de la région",
            "step2": "Étape 2 : Champs obligatoires (AAMVA)",
            "step3": "Étape 3 : Configuration du Code-barres",
            "generate": "GÉNÉRER LE CODE-BARRES & LA CHAÎNE",
            "success": "Génération terminée.",
            "raw": "Chaîne brute",
            "preview": "Aperçu du Code-barres"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # =========================
    # STEP 1: REGION
    # =========================
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", ["United States", "Canada"])
    
    with col2:
        if country == "United States":
            region = st.selectbox("State", sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox("Province", sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

    # =========================
    # STEP 2: FORM DATA
    # =========================
    st.markdown(f'<div class="step-animated overlay-box"><h3>{t["step2"]}</h3></div>', unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D9823415")
    with colB:
        dag = st.text_input("DAG", "1560 STREET")
        dai = st.text_input("DAI", "CITY")
        dak = st.text_input("DAK", "POSTAL")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")

    st.divider()

    # =========================
    # STEP 3: CONFIGURATION (NEW)
    # =========================
    st.markdown(f'<div class="step-animated-delay-1 overlay-box"><h3>{t["step3"]}</h3></div>', unsafe_allow_html=True)
    
    cfg1, cfg2, cfg3, cfg4 = st.columns(4)
    with cfg1:
        # Scale 15-20 correspond environ à 600 DPI selon la taille du module
        barcode_scale = st.slider("Scale (DPI)", 1, 30, 3) 
    with cfg2:
        barcode_padding = st.slider("Padding", 0, 50, 3)
    with cfg3:
        barcode_columns = st.slider("Columns", 1, 30, 10)
    with cfg4:
        use_escape = st.checkbox("Escape Sequences (\\n)", value=True)

    st.divider()

    # =========================
    # GENERATION LOGIC
    # =========================
    if st.button(t["generate"], use_container_width=True):
        try:
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # Gestion de l'échappement pour la chaîne brute
            sep = "\\n" if use_escape else "\n"
            
            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{state_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDCFREF001"
            )

            st.success(t["success"])
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.subheader(t["raw"])
                display_raw = raw.replace("\n", "\\n") if use_escape else raw
                st.code(display_raw)

            # =========================
            # BARCODE RENDERING WITH PARAMS
            # =========================
            with res_col2:
                st.subheader(t["preview"])
                
                # Encodage avec colonnes variables
                codes = encode(raw, columns=barcode_columns)
                
                # Rendu avec Scale (DPI) et Padding variables
                image = render_image(codes, scale=barcode_scale, padding=barcode_padding)

                buf = io.BytesIO()
                image.save(buf, format="PNG")
                png_bytes = buf.getvalue()

                st.image(png_bytes)

                # SVG Processing
                potrace_path = shutil.which("potrace")
                if potrace_path:
                    svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                    st.download_button("📥 SVG", svg, f"{dcs}.svg", "image/svg+xml")
                    st.markdown(f'<div class="step-fade overlay-box">{svg}</div>', unsafe_allow_html=True)
                
                st.download_button("📥 PNG", png_bytes, f"{dcs}.png", "image/png")

        except Exception:
            st.error(traceback.format_exc())
