import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# PATH FIX & CORE IMPORTS
# ==============================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg

# ==============================================================================
# LIQUID GLASS PRO UI - ENGINE CONFIGURATION (INTEGRAL CSS)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
    }

    /* --- CRYSTAL CARDS (SECTIONS) --- */
    .crystal-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        animation: slideUp 0.8s ease-out;
    }

    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0px); opacity: 1; }
    }

    /* --- LIQUID GLASS SLIDERS (OPTICAL ENGINE CONFIG) --- */
    /* Cible le rail du slider */
    div[data-testid="stTickBar"] { display: none; } /* Cache les graduations moches */
    
    div[data-baseweb="slider"] > div:first-child {
        height: 12px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* La barre de progression (le remplissage) */
    div[role="presentation"] > div > div:first-child {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        height: 12px !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(106, 17, 203, 0.6) !important;
    }

    /* Le bouton de drag (Thumb) - Style Capsule de l'image 7d64ec */
    div[role="slider"] {
        height: 24px !important;
        width: 24px !important;
        background-color: #fff !important;
        border: 4px solid #6a11cb !important;
        box-shadow: 0 0 20px rgba(106, 17, 203, 0.8), inset 0 0 5px rgba(0,0,0,0.2) !important;
        transition: transform 0.2s ease !important;
    }

    div[role="slider"]:hover {
        transform: scale(1.2) !important;
    }

    /* --- TEXT INPUTS & SELECTS (GLASSMOPHISM) --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f0f0f0 !important;
        padding: 12px 18px !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3) !important;
    }

    .stTextInput input:focus {
        border-color: #2575fc !important;
        box-shadow: 0 0 20px rgba(37, 117, 252, 0.2), inset 0 2px 10px rgba(0,0,0,0.3) !important;
    }

    /* --- ACTION BUTTONS (LIQUID PILL) --- */
    div.stButton > button, div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 50px !important;
        padding: 14px 40px !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3), inset 0 1px 2px rgba(255,255,255,0.2) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(106, 17, 203, 0.2) 0%, rgba(37, 117, 252, 0.2) 100%) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(37, 117, 252, 0.4) !important;
    }

    /* --- SVG CONTAINER --- */
    .svg-container svg {
        max-width: 100% !important;
        height: auto !important;
        max-height: 400px !important;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.8));
        border-radius: 10px;
    }

    .dpi-badge {
        font-family: 'Monaco', monospace;
        background: rgba(37, 117, 252, 0.1);
        color: #4facfe;
        padding: 4px 12px;
        border-radius: 8px;
        border: 1px solid rgba(37, 117, 252, 0.3);
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# CORE GENERATION LOGIC
# ==============================================================================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "Quantum AAMVA Engine",
            "desc": "Next-Gen Liquid Glass Forensic Interface",
            "step1": "Jurisdiction & IIN Mapping",
            "country": "Source Nation",
            "state": "State / Territory",
            "prov": "Province / Region",
            "step2": "Identity Matrix Parameters",
            "step3": "Optical Config (PRO)",
            "generate": "EXECUTE SEQUENCE",
            "success": "Matrix Compiled Successfully.",
            "raw": "AAMVA Raw Payload",
            "use": "Ready for 1:1 Rendering.",
            "preview": "Holographic Preview"
        },
        "FR": {
            "title": "Moteur Quantum AAMVA",
            "desc": "Interface Légiste Liquid Glass Next-Gen",
            "step1": "Cartographie Juridique & IIN",
            "country": "Nation Source",
            "state": "État / Territoire",
            "prov": "Province / Région",
            "step2": "Paramètres de la Matrice d'Identité",
            "step3": "Configuration Optique (PRO)",
            "generate": "EXÉCUTER LA SÉQUENCE",
            "success": "Matrice compilée avec succès.",
            "raw": "Payload Brut AAMVA",
            "use": "Prêt pour le rendu 1:1.",
            "preview": "Aperçu Holographique"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.markdown(f"*{t['desc']}*")
    st.divider()

    # --- ÉTAPE 1 : JURIDICTION ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        country = st.selectbox(t["country"], ["Canada", "United States"])

    icon_url = (
        "https://img.icons8.com/fluency/64/usa-flag.png"
        if country == "United States" else "https://img.icons8.com/fluency/64/canada-flag.png"
    )

    st.markdown(f"""
        <div style="display:flex;align-items:center;gap:15px; margin: 15px 0;">
            <img src="{icon_url}" width="36" style="filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));">
            <h3 style="margin:0; color:white;">{t["step1"]}</h3>
        </div>
    """, unsafe_allow_html=True)

    with c2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            # Quebec par défaut d'après ton permis exemple
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()), index=sorted(IIN_CA.keys()).index("Quebec"))
            mock_iin = IIN_CA[region]
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : MATRICE D'IDENTITÉ ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step2"])
    
    colA, colB = st.columns(2)
    with colA:
        # DCG Dynamique
        def_dcg = "CAN" if country == "Canada" else "USA"
        dcg = st.text_input("DCG (Country Code)", def_dcg)
        dac = st.text_input("DAC (First Name)", "JEAN")
        dcs = st.text_input("DCS (Last Name)", "NICOLAS")
        dbb = st.text_input("DBB (DOB YYYYMMDD)", "19941208") # Date du permis exemple
        daq = st.text_input("DAQ (License Number)", "N2420-941208-96")
        dag = st.text_input("DAG (Address)", "1560 SHERBROOKE ST E")
    with colB:
        dai = st.text_input("DAI (City)", "MONTREAL")
        dak = st.text_input("DAK (Postal Code)", "H2L 4M1")
        dbd = st.text_input("DBD (Issue YYYYMMDD)", "20230510")
        dba = st.text_input("DBA (Expiry YYYYMMDD)", "20310509")
        dbc = st.selectbox("DBC (Sex M=1/F=2)", ["1", "2"], index=0)
        dcf = st.text_input("DCF (Ref Number)", "PEJQ04N96")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : OPTICAL ENGINE (PRO SLIDERS) ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step3"])

    cf1, cf2 = st.columns(2)
    with cf1:
        # Résolution avec design néon
        dpi_val = st.select_slider("RENDER RESOLUTION (DPI)", options=[72, 150, 300, 600, 1200], value=600)
        calc_scale = max(1, int(dpi_val / 40))
        
        # Colonnes de la matrice
        barcode_columns = st.slider("MATRIX COLUMNS DENSITY", 1, 30, 10)
        
    with cf2:
        # Padding de zone calme
        barcode_padding = st.slider("QUIET ZONE PADDING", 0, 50, 3)
        
        # Options binaires
        st.write("")
        use_escape = st.checkbox("ENABLE ESCAPE SEQUENCES (\\n)", value=True)
        st.markdown(f'<span class="dpi-badge">ACTIVE ENGINE: {dpi_val} DPI / SCALE {calc_scale}x</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # ENGINE EXECUTION
    # ==============================================================================
    if st.button(t["generate"], use_container_width=True):

        try:
            # Calcul du code province/état
            s_code = "QC" if region == "Quebec" else region[:2].upper()
            
            # Header AAMVA
            header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # String Building
            raw = (
                f"@\n{header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{s_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])

            # --- RÉSULTATS VISUELS ---
            res_l, res_r = st.columns([1, 1.3])

            with res_l:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(t["raw"])
                final_str = raw.replace("\n", "\\n") if use_escape else raw
                st.code(final_str, language="text")
                st.info(t["use"])
                st.markdown('</div>', unsafe_allow_html=True)

            with res_r:
                st.markdown('<div class="crystal-card" style="text-align:center;">', unsafe_allow_html=True)
                st.subheader(t["preview"])
                
                # PDF417 Logic
                codes = encode(raw, columns=barcode_columns)
                img = render_image(codes, scale=calc_scale, padding=barcode_padding)

                # PNG Export
                b = io.BytesIO()
                img.save(b, format="PNG", dpi=(dpi_val, dpi_val))
                p_bytes = b.getvalue()

                st.image(p_bytes, use_column_width=True)

                # Download Group
                dl1, dl2 = st.columns(2)
                with dl1:
                    st.download_button(f"📥 PNG {dpi_val}", p_bytes, f"{dcs}_AAMVA.png", "image/png", use_container_width=True)
                
                # SVG Logic
                pt_path = shutil.which("potrace")
                svg_data = None
                if pt_path:
                    try:
                        svg_data = png_to_svg(png_bytes=p_bytes, potrace_path=pt_path)
                        with dl2:
                            st.download_button("💎 VECTOR SVG", svg_data, f"{dcs}_AAMVA.svg", "image/svg+xml", use_container_width=True)
                    except: pass
                else:
                    with dl2: st.button("💎 VECTOR N/A", disabled=True, use_container_width=True)

                if svg_data:
                    with st.expander("🔍 VECTOR INSPECTION"):
                        st.markdown(
                            f'<div class="svg-container" style="background:white; padding:20px;">{svg_data}</div>', 
                            unsafe_allow_html=True
                        )
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception:
            st.error("CORE ENGINE ERROR")
            st.code(traceback.format_exc())

# ==============================================================================
# END OF ARCHITECTURE
# ==============================================================================
