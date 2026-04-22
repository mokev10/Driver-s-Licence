import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# PATH FIX & CORE IMPORTS (STRICTEMENT CONSERVÉS)
# ==============================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg

# ==============================================================================
# LIQUID GLASS UI KIT - CUSTOM CSS ENGINE (PLUS DE 150 LIGNES DE STYLE)
# ==============================================================================
st.markdown(
    """
    <style>
    /* Global Background & Font Tuning */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }

    /* Keyframes pour les effets de lumière Liquid Glass */
    @keyframes glassShine {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes slideUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0px); opacity: 1; }
    }

    /* Conteneur de section style 'Crystal Slab' */
    .crystal-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2), inset 0 0 15px rgba(255,255,255,0.05);
        animation: slideUp 0.8s ease-out;
    }

    /* --- BOUTONS LIQUID GLASS (STYLE IMAGE) --- */
    div.stButton > button, div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 50px !important; /* Pill shape comme sur l'image */
        padding: 12px 35px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 2px 5px rgba(255,255,255,0.2) !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(106, 17, 203, 0.4), inset 0 2px 10px rgba(255,255,255,0.3) !important;
    }

    /* Effet spécifique 'Secondary' ou 'Action' avec gradient interne léger */
    div.stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* --- CHAMPS DE TEXTE LIQUID GLASS --- */
    /* On cible les inputs Streamlit pour leur donner l'aspect de l'image (Text field) */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e0e0e0 !important;
        padding: 10px 15px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5), 0 1px 1px rgba(255,255,255,0.05) !important;
        transition: border 0.3s ease, box-shadow 0.3s ease !important;
    }

    .stTextInput input:focus {
        border-color: #6a11cb !important;
        box-shadow: 0 0 15px rgba(106, 17, 203, 0.3), inset 0 2px 4px rgba(0,0,0,0.5) !important;
    }

    /* --- CHECKBOX / SWITCH STYLE --- */
    /* Simulation du style Switch visible sur l'image kit */
    div[data-testid="stCheckbox"] label span {
        color: #bbb !important;
        font-weight: 400 !important;
    }

    /* --- TITRES ET SUBHEADERS --- */
    h1, h2, h3 {
        background: linear-gradient(135deg, #ffffff 0%, #aab7c4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600 !important;
    }

    /* --- ELEMENTS SPECIFIQUES --- */
    .dpi-info {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 5px 15px;
        border-left: 3px solid #6a11cb;
        font-family: monospace;
        color: #4facfe;
    }

    .svg-container svg {
        max-width: 100% !important;
        height: auto !important;
        max-height: 380px !important;
        display: block;
        margin: 0 auto;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
    }

    /* Scrollbar stylisée pour le verre */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# MAIN FUNCTION
# ==============================================================================
def show_identity_gen(lang="EN"):

    # Dictionnaire de traduction (Intégral)
    TEXT = {
        "EN": {
            "title": "Crystal AAMVA Generator",
            "desc": "Liquid Glass UI Kit Edition - Forensic Payload Engine",
            "step1": "Jurisdiction Mapping",
            "country": "Nation Source",
            "state": "State Territory",
            "prov": "Province Region",
            "step2": "Identity Matrix Data (AAMVA)",
            "step3": "Optical Engine Configuration",
            "generate": "INITIALIZE GENERATION",
            "success": "Matrix sequence established.",
            "raw": "Payload String Output",
            "use": "Copy the sequence below for rendering.",
            "preview": "Digital Twin Preview"
        },
        "FR": {
            "title": "Générateur Crystal AAMVA",
            "desc": "Édition Liquid Glass UI - Moteur de Payload Légiste",
            "step1": "Cartographie de Juridiction",
            "country": "Source de la Nation",
            "state": "Territoire de l'État",
            "prov": "Région de la Province",
            "step2": "Matrice de Données d'Identité",
            "step3": "Configuration du Moteur Optique",
            "generate": "INITIALISER LA GÉNÉRATION",
            "success": "Séquence matricielle établie.",
            "raw": "Sortie de la chaîne Payload",
            "use": "Copiez la séquence ci-dessous pour le rendu.",
            "preview": "Aperçu du Jumeau Numérique"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.markdown(f"*{t['desc']}*")
    st.divider()

    # --- ÉTAPE 1 : JURIDICTION (CRYSTAL CARD 1) ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        # Valeur par défaut Canada selon tes instructions précédentes
        country = st.selectbox(t["country"], ["Canada", "United States"])

    # Logique d'icône Liquid Glass
    icon = (
        "https://img.icons8.com/fluency/64/usa-flag.png"
        if country == "United States" else "https://img.icons8.com/fluency/64/canada-flag.png"
    )

    st.markdown(f"""
        <div style="display:flex;align-items:center;gap:15px; margin-top:10px; margin-bottom:15px;">
            <img src="{icon}" width="32" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
            <h3 style="margin:0;">{t["step1"]}</h3>
        </div>
    """, unsafe_allow_html=True)

    with c2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()), index=sorted(IIN_CA.keys()).index("Quebec"))
            mock_iin = IIN_CA[region]
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : DONNÉES (CRYSTAL CARD 2) ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step2"])
    
    colA, colB = st.columns(2)
    with colA:
        # Logique dynamique du pays (CAN/USA) conservée
        default_dcg = "CAN" if country == "Canada" else "USA"
        dcg = st.text_input("DCG (ISO Country)", default_dcg)
        
        dac = st.text_input("DAC (Given Names)", "JEAN")
        dcs = st.text_input("DCS (Surname)", "NICOLAS")
        dbb = st.text_input("DBB (Date of Birth - YYYYMMDD)", "19941208")
        daq = st.text_input("DAQ (License Identifier)", "N2420-941208-96")
        dag = st.text_input("DAG (Residential Address)", "1560 SHERBROOKE ST E")
    with colB:
        dai = st.text_input("DAI (Locality / City)", "MONTREAL")
        dak = st.text_input("DAK (Postal / Zip Code)", "H2L 4M1")
        dbd = st.text_input("DBD (Document Issue Date)", "20230510")
        dba = st.text_input("DBA (Document Expiration)", "20310509")
        dbc = st.selectbox("DBC (Gender / Sex)", ["1", "2"], index=0, help="1: Male, 2: Female")
        dcf = st.text_input("DCF (Document Discriminator)", "PEJQ04N96")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : ENGINE (CRYSTAL CARD 3) ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step3"])

    cf1, cf2, cf3, cf4 = st.columns(4)
    with cf1:
        dpi_val = st.select_slider("Resolution Density (DPI)", options=[72, 150, 300, 600, 1200], value=600)
        calc_scale = max(1, int(dpi_val / 40))
    with cf2:
        barcode_padding = st.slider("Zone Padding", 0, 50, 3)
    with cf3:
        barcode_columns = st.slider("Matrix Columns", 1, 30, 10)
    with cf4:
        use_escape = st.checkbox("Format with Escape (\\n)", value=True)

    st.markdown(f'<p class="dpi-info">ENGINE STATUS: {dpi_val} DPI | TARGET SCALE: {calc_scale}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # GENERATION LOGIC - THE CORE ENGINE
    # ==============================================================================
    if st.button(t["generate"], use_container_width=True):

        try:
            # Traitement des codes régionaux (DAJ)
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            
            # Reconstruction du Header AAMVA (Standard 2005)
            # Format: @ + LF + ANSI + IIN + Version + DL + Offsets...
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # Assemblage de la chaîne brute (Payload)
            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{state_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])
            st.divider()

            # --- DISPLAY RESULTS (LIQUID GLASS LAYOUT) ---
            res_left, res_right = st.columns([1, 1.3])

            with res_left:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(t["raw"])
                # Option d'affichage pour les outils de design type Photoshop/AI
                display_raw = raw.replace("\n", "\\n") if use_escape else raw
                st.code(display_raw, language="text")
                st.info(t["use"])
                st.markdown('</div>', unsafe_allow_html=True)

            with res_right:
                st.markdown('<div class="crystal-card" style="text-align:center;">', unsafe_allow_html=True)
                st.subheader(t["preview"])
                
                # Encodage PDF417
                codes = encode(raw, columns=barcode_columns)
                image = render_image(codes, scale=calc_scale, padding=barcode_padding)

                # Conversion Buffer PNG
                buf = io.BytesIO()
                image.save(buf, format="PNG", dpi=(dpi_val, dpi_val))
                png_bytes = buf.getvalue()

                # Affichage de l'image PNG (Rendu High DPI)
                st.image(png_bytes, use_column_width=True)

                # Groupe de boutons de téléchargement Liquid Glass
                btn_1, btn_2 = st.columns(2)
                with btn_1:
                    st.download_button(
                        label=f"💾 EXPORT PNG ({dpi_val})",
                        data=png_bytes,
                        file_name=f"AAMVA_{dcs}_{region}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                # Gestion du moteur vectoriel Potrace
                potrace_path = shutil.which("potrace")
                svg = None
                
                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                        with btn_2:
                            st.download_button(
                                label="💎 EXPORT SVG (VECTOR)",
                                data=svg,
                                file_name=f"AAMVA_{dcs}_{region}.svg",
                                mime="image/svg+xml",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Vector engine error: {e}")
                else:
                    with btn_2:
                        st.button("🚫 VECTOR DISABLED", disabled=True, use_container_width=True)

                # Expander pour l'aperçu vectoriel (Correctif de taille intégré)
                if svg:
                    with st.expander("🔍 Inspect Vector Layer"):
                        st.markdown(
                            f'<div class="step-fade svg-container" style="background:white; padding:15px; border-radius:15px;">{svg}</div>', 
                            unsafe_allow_html=True
                        )
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            # Gestion d'erreur brute pour debug forensic
            st.error("Engine Fault Detected")
            st.code(traceback.format_exc())

# ==============================================================================
# END OF FILE (IDENTITY_GEN.PY)
# ==============================================================================
# Ce code contient la structure complète, le moteur CSS Liquid Glass,
# la logique bilingue, et le traitement des données AAMVA sans aucune simplification.
