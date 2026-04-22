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
# UI/UX CUSTOM CSS (MODERNE & NÉON)
# =========================
st.markdown(
    """
    <style>
    /* Animations existantes */
    @keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0px); opacity: 1; } }
    .step-animated { animation: slideUp 0.6s ease-out; }
    
    /* Style global des conteneurs */
    .config-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    /* Custom Sliders Streamlit */
    div[data-testid="stSlider"] > label {
        color: #4facfe !important;
        font-weight: bold !important;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    /* Custom Checkbox */
    div[data-testid="stCheckbox"] {
        background: rgba(79, 172, 254, 0.1);
        padding: 10px 20px;
        border-radius: 10px;
        border: 1px solid rgba(79, 172, 254, 0.3);
    }

    /* Accentuation de la couleur primaire */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #4facfe;
        box-shadow: 0 0 10px #4facfe;
    }
    
    .stSlider [data-highlight="true"] {
        background: linear-gradient(90deg, #4facfe 0%, #a066ff 100%) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Forensic Generator",
            "step1": "🌍 Jurisdiction Selection",
            "step2": "🪪 Identity Attributes",
            "step3": "⚙️ Barcode Engine Config",
            "generate": "GENERATE PAYLOAD & BARCODE",
            "success": "Matrix generated successfully."
        },
        "FR": {
            "title": "Générateur AAMVA Forensic",
            "step1": "🌍 Sélection de la Juridiction",
            "step2": "🪪 Attributs d'Identité",
            "step3": "⚙️ Configuration du Moteur",
            "generate": "GÉNÉRER LE CODE & LA MATRICE",
            "success": "Matrice générée avec succès."
        }
    }
    t = TEXT.get(lang, TEXT["EN"])

    st.title(f"🚀 {t['title']}")
    st.divider()

    # =========================
    # STEP 1: JURISDICTION
    # =========================
    with st.container():
        st.markdown(f'<div class="step-animated config-card"><h4>{t["step1"]}</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox("Market", ["United States", "Canada"])
        with col2:
            if country == "United States":
                region = st.selectbox("State Territory", sorted(IIN_US.keys()))
                mock_iin = IIN_US[region]
            else:
                region = st.selectbox("Province", sorted(IIN_CA.keys()))
                mock_iin = IIN_CA[region]
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # STEP 2: DATA INPUTS
    # =========================
    with st.container():
        st.markdown(f'<div class="step-animated config-card"><h4>{t["step2"]}</h4>', unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            dac = st.text_input("DAC (First Name)", "JEAN")
            dcs = st.text_input("DCS (Last Name)", "NICOLAS")
            dbb = st.text_input("DBB (DOB)", "19941208")
            daq = st.text_input("DAQ (DL Number)", "D9823415")
        with colB:
            dag = st.text_input("DAG (Address)", "1560 STREET")
            dai = st.text_input("DAI (City)", "CITY")
            dak = st.text_input("DAK (Zip)", "POSTAL")
            dba = st.text_input("DBA (Expiry)", "20310509")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # STEP 3: ADVANCED UI CONFIG (Le nouveau design pour tes sliders)
    # =========================
    with st.container():
        st.markdown(f'<div class="step-animated config-card"><h4>{t["step3"]}</h4>', unsafe_allow_html=True)
        
        # Organisation en grille moderne
        cfg_col1, cfg_col2, cfg_col3 = st.columns([2, 2, 2])
        
        with cfg_col1:
            barcode_scale = st.slider("Scale (Resolution/DPI)", 1, 30, 15, help="Augmenter pour une qualité forensic (600 DPI+)")
        
        with cfg_col2:
            barcode_padding = st.slider("Quiet Zone (Padding)", 0, 50, 5, help="Espace blanc autour du code")
            
        with cfg_col3:
            barcode_columns = st.slider("Module Columns", 1, 30, 8, help="Largeur des colonnes PDF417")
        
        # Checkbox stylisée en bas
        st.markdown("<br>", unsafe_allow_html=True)
        use_escape = st.checkbox("Enable Escape Sequences (\\n) for TEC-IT / Photoshop", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # ACTION
    # =========================
    if st.button(t["generate"], use_container_width=True):
        try:
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
            
            raw = (
                f"@\n{aamva_header}\n"
                f"DCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{state_code}\nDAK{dak}\n"
                f"DBA{dba}\nDCFREF001"
            )

            st.success(t["success"])
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("Final String Payload")
                display_raw = raw.replace("\n", "\\n") if use_escape else raw
                st.code(display_raw, language="text")

            with res_col2:
                st.subheader("Visual Preview")
                codes = encode(raw, columns=barcode_columns)
                image = render_image(codes, scale=barcode_scale, padding=barcode_padding)

                buf = io.BytesIO()
                image.save(buf, format="PNG")
                png_bytes = buf.getvalue()

                st.image(png_bytes, caption=f"PDF417 - Scale {barcode_scale}")
                
                # SVG Export logic
                potrace_path = shutil.which("potrace")
                if potrace_path:
                    svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                    st.download_button("📥 GET VECTOR SVG", svg, f"{dcs}.svg", "image/svg+xml")
                
                st.download_button("📥 GET HIGH-RES PNG", png_bytes, f"{dcs}.png", "image/png")

        except Exception:
            st.error("Engine Fault")
            st.code(traceback.format_exc())
