import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION ET CHARGEMENT DES MODULES
# ==============================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if 'ui_theme' not in st.session_state:
    st.session_state.ui_theme = "dark"

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    IIN_US = {"Alabama": "603201", "California": "603273", "Florida": "603211", "New York": "603219", "Texas": "603233"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430", "Alberta": "604433"}

# ==============================================================================
# MOTEUR DE STYLE LIQUID GLASS ULTRA-COMPLET (IMAGE 7D5952 / 7D64EC)
# ==============================================================================
is_dark = st.session_state.ui_theme == "dark"
bg_main = "#030305" if is_dark else "#fcfdfe"
card_fill = "rgba(255, 255, 255, 0.02)" if is_dark else "rgba(255, 255, 255, 0.9)"
txt_main = "#ffffff" if is_dark else "#101114"
brd_ref = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.08)"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_main};
        color: {txt_main};
        font-family: 'Inter', sans-serif;
    }}

    /* --- CARTE FLOTTANTE STYLE GLASS --- */
    .floating-card {{
        background: {card_fill};
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid {brd_ref};
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 35px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}

    /* --- LABELS VIOLETS (IMAGE 7E3404) --- */
    .meta-label {{
        font-family: 'JetBrains Mono', monospace;
        color: #8122ff;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 6px;
        margin-top: 15px;
    }}

    /* --- TITRE DE SECTION (IMAGE 7DBF85) --- */
    .section-header {{
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 25px;
        color: {txt_main};
    }}

    /* --- SLIDERS LIQUID (IMAGE 7D64EC) --- */
    div[data-testid="stTickBar"] {{ display: none !important; }}
    div[data-baseweb="slider"] > div:first-child {{
        height: 14px !important;
        background: rgba(129, 34, 255, 0.1) !important;
        border-radius: 20px !important;
    }}
    div[role="presentation"] > div > div:first-child {{
        background: linear-gradient(90deg, #8122ff, #3a82ff) !important;
        height: 14px !important;
        border-radius: 20px !important;
    }}
    div[role="slider"] {{
        height: 28px !important;
        width: 28px !important;
        background-color: #ffffff !important;
        border: 5px solid #8122ff !important;
        box-shadow: 0 0 20px rgba(129, 34, 255, 0.5) !important;
    }}

    /* --- BOUTONS ET INPUTS --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {brd_ref} !important;
        border-radius: 14px !important;
        color: {txt_main} !important;
        height: 45px !important;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #8122ff, #3a82ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 18px 45px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
    }}
    
    /* --- BARCODE PREVIEW AREA --- */
    .barcode-container {{
        background: #fff;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# LOGIQUE DE GESTION DU THÈME
# ==============================================================================
def toggle_theme():
    st.session_state.ui_theme = "light" if st.session_state.ui_theme == "dark" else "dark"

# ==============================================================================
# INTERFACE PRINCIPALE EXHAUSTIVE
# ==============================================================================
def show_identity_gen(lang="FR"):
    
    # Lexique technique
    UI = {
        "FR": {
            "title": "Studio Quantum AAMVA",
            "theme": "Changer le Mode Visuel",
            "jur_title": "Cartographie de Juridiction",
            "mat_title": "Matrice de Métadonnées d'Identité",
            "opt_title": "Configuration du Moteur Optique",
            "gen_btn": "Initialiser la Séquence de Génération"
        },
        "EN": {
            "title": "Quantum AAMVA Studio",
            "theme": "Switch Visual Mode",
            "jur_title": "Jurisdiction Mapping",
            "mat_title": "Identity Metadata Matrix",
            "opt_title": "Optical Engine Config",
            "gen_btn": "Initialize Generation Sequence"
        }
    }
    
    txt = UI.get(lang, UI["FR"])

    # Header de l'application
    h_col1, h_col2 = st.columns([5, 2])
    with h_col1:
        st.title(txt["title"])
    with h_col2:
        st.button(txt["theme"], on_click=toggle_theme, use_container_width=True)

    st.divider()

    # --- ÉTAPE 1 : JURIDICTION (IMAGE 7DBF85) ---
    st.markdown(f'<div class="section-header">{txt["jur_title"]}</div>', unsafe_allow_html=True)
    
    c_j1, c_j2 = st.columns(2)
    with c_j1:
        st.markdown('<div class="meta-label">Source Nation</div>', unsafe_allow_html=True)
        nation = st.selectbox("", ["United States", "Canada"], label_visibility="collapsed")
    with c_j2:
        st.markdown('<div class="meta-label">Regional State / Province</div>', unsafe_allow_html=True)
        if nation == "United States":
            region = st.selectbox("", sorted(IIN_US.keys()), label_visibility="collapsed")
            iin = IIN_US[region]
        else:
            provinces = sorted(IIN_CA.keys())
            q_idx = provinces.index("Quebec") if "Quebec" in provinces else 0
            region = st.selectbox("", provinces, index=q_idx, label_visibility="collapsed")
            iin = IIN_CA[region]

    # --- ÉTAPE 2 : MATRICE D'IDENTITÉ (IMAGE 7E3404) ---
    st.markdown(f'<div class="section-header">{txt["mat_title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown('<div class="meta-label">DCG - ISO Country Code</div>', unsafe_allow_html=True)
        f_dcg = st.text_input("", "USA" if nation == "United States" else "CAN", key="dcg", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DAC - First Name</div>', unsafe_allow_html=True)
        f_dac = st.text_input("", "JEAN", key="dac", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DCS - Family Name</div>', unsafe_allow_html=True)
        f_dcs = st.text_input("", "NICOLAS", key="dcs", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DBB - Date of Birth</div>', unsafe_allow_html=True)
        f_dbb = st.text_input("", "19941208", key="dbb", label_visibility="collapsed")
    
    with m_col2:
        st.markdown('<div class="meta-label">DAQ - Document Number</div>', unsafe_allow_html=True)
        f_daq = st.text_input("", "N2420-941208-96", key="daq", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DBD - Issue Date</div>', unsafe_allow_html=True)
        f_dbd = st.text_input("", "20230510", key="dbd", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DBA - Expiry Date</div>', unsafe_allow_html=True)
        f_dba = st.text_input("", "20310509", key="dba", label_visibility="collapsed")
        
        st.markdown('<div class="meta-label">DCF - Discriminator</div>', unsafe_allow_html=True)
        f_dcf = st.text_input("", "PEJQ04N96", key="dcf", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : CONFIGURATION OPTIQUE (IMAGE 7D64EC) ---
    st.markdown(f'<div class="section-header">{txt["opt_title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="floating-card">', unsafe_allow_html=True)
    
    o_col1, o_col2, o_col3 = st.columns(3)
    with o_col1:
        st.markdown('<div class="meta-label">Render Resolution (DPI)</div>', unsafe_allow_html=True)
        dpi = st.select_slider("", options=[72, 300, 600, 1200], value=600, label_visibility="collapsed")
    with o_col2:
        st.markdown('<div class="meta-label">Barcode Density (Cols)</div>', unsafe_allow_html=True)
        cols = st.slider("", 1, 30, 10, label_visibility="collapsed")
    with o_col3:
        st.markdown('<div class="meta-label">Quiet Zone Padding</div>', unsafe_allow_html=True)
        pad = st.slider("", 0, 60, 5, label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- GÉNÉRATION ET PRÉVISUALISATION (IMAGE 7CDAA2) ---
    if st.button(txt["gen_btn"], use_container_width=True):
        try:
            # Construction de la chaîne AAMVA brute
            raw_str = f"@\nANSI {iin}050102DL00410287ZO02900045DL\nDCG{f_dcg}\nDCS{f_dcs}\nDAC{f_dac}\nDBB{f_dbb}\nDAQ{f_daq}"
            
            p_col1, p_col2 = st.columns([2, 3])
            
            with p_col1:
                st.markdown('<div class="meta-label">Raw Data String</div>', unsafe_allow_html=True)
                st.code(raw_str, language="text")
            
            with p_col2:
                st.markdown('<div class="meta-label">Holographic Preview</div>', unsafe_allow_html=True)
                # Encodage PDF417
                codes = encode(raw_str, columns=cols)
                img = render_image(codes, scale=max(1, int(dpi/60)), padding=pad)
                
                # Affichage de l'image
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.image(buf.getvalue(), use_container_width=True)
                
                # Boutons de téléchargement style Liquid
                st.download_button("PNG (High DPI)", buf.getvalue(), "barcode.png", "image/png", use_container_width=True)
                
        except Exception:
            st.error("Défaut de compilation du moteur")
            st.code(traceback.format_exc())

# ==============================================================================
# MAINTENANCE DU SCRIPT (LIGNE 500)
# ==============================================================================
