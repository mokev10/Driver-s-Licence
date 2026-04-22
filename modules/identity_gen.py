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
# UI/UX CUSTOM CSS (CONSERVÉ ET AMÉLIORÉ)
# =========================
st.markdown(
    """
    <style>
    @keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0px); opacity: 1; } }
    .step-animated { animation: slideUp 0.6s ease-out; }
    
    .config-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .dpi-badge {
        background: linear-gradient(90deg, #4facfe 0%, #a066ff 100%);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {"title": "AAMVA High-Res Engine", "step3": "⚙️ Rendering & DPI Settings"},
        "FR": {"title": "Moteur AAMVA Haute-Résolution", "step3": "⚙️ Réglages du Rendu & DPI"}
    }
    t = TEXT.get(lang, TEXT["EN"])

    st.title(f"🚀 {t['title']}")
    st.divider()

    # --- SÉLECTION RÉGION ---
    with st.container():
        st.markdown('<div class="step-animated config-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox("Market", ["United States", "Canada"])
        with col2:
            list_data = IIN_US if country == "United States" else IIN_CA
            region = st.selectbox("Jurisdiction", sorted(list_data.keys()))
            mock_iin = list_data[region]
        st.markdown('</div>', unsafe_allow_html=True)

    # --- INPUTS ---
    with st.container():
        st.markdown('<div class="step-animated config-card">', unsafe_allow_html=True)
        cA, cB = st.columns(2)
        with cA:
            dac = st.text_input("DAC (First Name)", "JEAN")
            dcs = st.text_input("DCS (Last Name)", "NICOLAS")
            dbb = st.text_input("DBB (DOB)", "19941208")
        with cB:
            daq = st.text_input("DAQ (DL Number)", "D9823415")
            dba = st.text_input("DBA (Expiry)", "20310509")
            dak = st.text_input("DAK (Zip)", "H2L 4M1")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # ÉTAPE 3: RÉGLAGE DPI PRÉCIS
    # =========================
    with st.container():
        st.markdown(f'<div class="step-animated config-card"><h4>{t["step3"]}</h4>', unsafe_allow_html=True)
        
        cfg_col1, cfg_col2, cfg_col3 = st.columns([2, 2, 2])
        
        with cfg_col1:
            # Sélecteur de DPI réel
            dpi_target = st.select_slider(
                "Target Resolution (DPI)",
                options=[72, 150, 300, 600, 1200],
                value=600,
                help="600 DPI est le standard pour les documents officiels."
            )
            # Calcul du scale : DPI / 40 est une bonne approximation pour pdf417gen
            calculated_scale = max(1, int(dpi_target / 40))
        
        with cfg_col2:
            barcode_padding = st.slider("Padding", 0, 50, 10)
            
        with cfg_col3:
            barcode_columns = st.slider("Columns", 1, 20, 8)
        
        st.markdown(f'Résolution active : <span class="dpi-badge">{dpi_target} DPI</span> (Scale: {calculated_scale})', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # GÉNÉRATION
    # =========================
    if st.button("GÉNÉRER LA MATRICE", use_container_width=True):
        try:
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
            
            raw = f"@\n{aamva_header}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\nDAJ{state_code}\nDAK{dak}\nDBA{dba}"

            st.success("Génération complétée.")
            
            r1, r2 = st.columns(2)
            with r1:
                st.code(raw.replace("\n", "\\n"))

            with r2:
                codes = encode(raw, columns=barcode_columns)
                # Utilisation du scale calculé selon le DPI
                image = render_image(codes, scale=calculated_scale, padding=barcode_padding)

                buf = io.BytesIO()
                image.save(buf, format="PNG", dpi=(dpi_target, dpi_target)) # Injection des métadonnées DPI
                png_bytes = buf.getvalue()

                st.image(png_bytes, caption=f"Rendu à {dpi_target} DPI")
                
                st.download_button(f"📥 PNG ({dpi_target} DPI)", png_bytes, f"{dcs}_{dpi_target}dpi.png", "image/png")

                # SVG
                potrace_path = shutil.which("potrace")
                if potrace_path:
                    svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                    st.download_button("📥 SVG VECTOR", svg, f"{dcs}.svg", "image/svg+xml")

        except Exception:
            st.error(traceback.format_exc())
