import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION ET CHARGEMENT DU CORE (VERSION INDUSTRIELLE)
# ==============================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if 'ui_theme' not in st.session_state:
    st.session_state.ui_theme = "dark"

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    # Fallback pour garantir le fonctionnement même sans les dépendances locales
    IIN_US = {"Alabama": "603201", "California": "603273", "Florida": "603211", "New York": "603219", "Texas": "603233"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430", "Alberta": "604433", "BC": "604434"}

# ==============================================================================
# MOTEUR DE RENDU CSS : LIQUID GLASS & PURPLE LABELS (IMAGE 7E3B23)
# ==============================================================================
is_dark = st.session_state.ui_theme == "dark"
bg_main = "#050508" if is_dark else "#f5f7fa"
card_fill = "rgba(255, 255, 255, 0.02)" if is_dark else "rgba(255, 255, 255, 0.95)"
text_main = "#ffffff" if is_dark else "#1a1c22"
accent_color = "#8122ff" # Violet signature

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_main};
        color: {text_main};
        font-family: 'Inter', sans-serif;
    }}

    /* --- CONTENEUR CRYSTAL FLOTTANT --- */
    .crystal-panel {{
        background: {card_fill};
        backdrop-filter: blur(45px);
        -webkit-backdrop-filter: blur(45px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}

    /* --- LABELS VIOLETS TECHNIQUES (IMAGE 7E3404) --- */
    .purple-label {{
        font-family: 'JetBrains Mono', monospace;
        color: {accent_color};
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
        margin-top: 18px;
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
        box-shadow: 0 0 25px rgba(129, 34, 255, 0.7) !important;
    }}

    /* --- INPUTS & SELECTORS --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {{
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        color: {text_main} !important;
        padding: 12px !important;
    }}

    /* --- BOUTON DE GÉNÉRATION QUANTUM --- */
    div.stButton > button {{
        background: linear-gradient(135deg, #8122ff 0%, #3a82ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 60px !important;
        padding: 20px 60px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        box-shadow: 0 15px 35px rgba(129, 34, 255, 0.3) !important;
        transition: all 0.4s ease !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(129, 34, 255, 0.5) !important;
    }}

    /* --- DRAPEAUX ET TITRES --- */
    .jur-header {{
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 25px;
    }}
    .jur-flag {{
        width: 50px;
        border-radius: 8px;
        filter: drop-shadow(0 8px 15px rgba(0,0,0,0.4));
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# LOGIQUE DE L'INTERFACE UTILISATEUR
# ==============================================================================
def show_identity_gen(lang="FR"):
    
    # Lexique technique sans emojis
    UI = {
        "FR": {
            "title": "Studio Quantum AAMVA",
            "jur_title": "Cartographie de Juridiction",
            "mat_title": "Matrice de Métadonnées d'Identité",
            "opt_title": "Configuration du Moteur Optique",
            "gen_btn": "Initialiser la Séquence de Génération",
            "res_raw": "Chaîne de Données Brute",
            "res_preview": "Aperçu du Jumeau Numérique"
        }
    }
    txt = UI["FR"]

    st.title(txt["title"])
    st.divider()

    # --- SECTION 1 : JURIDICTION ---
    st.markdown(f'<div class="purple-label">Target Nation & Territory</div>', unsafe_allow_html=True)
    c_j1, c_j2 = st.columns(2)
    with c_j1:
        country = st.selectbox("Source Nation", ["United States", "Canada"])
    with c_j2:
        if country == "United States":
            region = st.selectbox("State", sorted(IIN_US.keys()))
            active_iin = IIN_US[region]
            flag_img = "https://cdn-icons-png.flaticon.com/512/323/323310.png"
        else:
            region = st.selectbox("Province", sorted(IIN_CA.keys()), index=sorted(IIN_CA.keys()).index("Quebec"))
            active_iin = IIN_CA[region]
            flag_img = "https://cdn-icons-png.flaticon.com/512/323/323277.png"

    st.markdown(f"""
        <div class="jur-header">
            <img src="{flag_img}" class="jur-flag">
            <div style="font-size:1.5rem; font-weight:600;">{txt["jur_title"]}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- SECTION 2 : MATRICE D'IDENTITÉ COMPLÈTE (IMAGE 7CE8EB) ---
    st.markdown(f'<div class="purple-label">{txt["mat_title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="crystal-panel">', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="purple-label">DCS - Surname</div>', unsafe_allow_html=True)
        f_dcs = st.text_input("", "NICOLAS", key="dcs", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAC - First Name</div>', unsafe_allow_html=True)
        f_dac = st.text_input("", "JEAN", key="dac", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAG - Residential Street</div>', unsafe_allow_html=True)
        f_dag = st.text_input("", "1560 SHERBROOKE ST E", key="dag", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAI - City / Locality</div>', unsafe_allow_html=True)
        f_dai = st.text_input("", "MONTREAL", key="dai", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAK - Postal Code</div>', unsafe_allow_html=True)
        f_dak = st.text_input("", "H2L 4M1", key="dak", label_visibility="collapsed")

    with col_b:
        st.markdown('<div class="purple-label">DAQ - Document Number</div>', unsafe_allow_html=True)
        f_daq = st.text_input("", "N2420-941208-96", key="daq", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DBB - Date of Birth</div>', unsafe_allow_html=True)
        f_dbb = st.text_input("", "19941208", key="dbb", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DBC - Gender (1:M / 2:F)</div>', unsafe_allow_html=True)
        f_dbc = st.selectbox("", ["1", "2", "3"], key="dbc", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAU - Height (cm/in)</div>', unsafe_allow_html=True)
        f_dau = st.text_input("", "180 cm", key="dau", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAY - Eye Color</div>', unsafe_allow_html=True)
        f_day = st.text_input("", "BRUN", key="day", label_visibility="collapsed")
    
    st.markdown('<div class="purple-label">Validité Temporelle & Discriminant</div>', unsafe_allow_html=True)
    c_t1, c_t2, c_t3 = st.columns(3)
    with c_t1:
        st.markdown('<div class="purple-label">DBD - Issue Date</div>', unsafe_allow_html=True)
        f_dbd = st.text_input("", "20230510", key="dbd", label_visibility="collapsed")
    with c_t2:
        st.markdown('<div class="purple-label">DBA - Expiry Date</div>', unsafe_allow_html=True)
        f_dba = st.text_input("", "20310509", key="dba", label_visibility="collapsed")
    with c_t3:
        st.markdown('<div class="purple-label">DCF - Audit Number</div>', unsafe_allow_html=True)
        f_dcf = st.text_input("", "PEJQ04N96", key="dcf", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 3 : OPTIQUES (IMAGE 7D64EC) ---
    st.markdown(f'<div class="purple-label">{txt["opt_title"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="crystal-panel">', unsafe_allow_html=True)
    o1, o2, o3 = st.columns(3)
    with o1:
        st.markdown('<div class="purple-label">Resolution (DPI)</div>', unsafe_allow_html=True)
        res_dpi = st.select_slider("", options=[72, 300, 600, 1200], value=600, label_visibility="collapsed")
    with o2:
        st.markdown('<div class="purple-label">Matrix Columns</div>', unsafe_allow_html=True)
        m_cols = st.slider("", 1, 30, 12, label_visibility="collapsed")
    with o3:
        st.markdown('<div class="purple-label">Quiet Zone</div>', unsafe_allow_html=True)
        q_zone = st.slider("", 0, 50, 5, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- GÉNÉRATION ET RENDU ---
    if st.button(txt["gen_btn"], use_container_width=True):
        try:
            # Code territoire automatique
            st_code = "QC" if region == "Quebec" else region[:2].upper()
            
            # Chaîne AAMVA conforme
            raw_str = (
                f"@\nANSI {active_iin}050102DL00410287ZO02900045DL\n"
                f"DCG{'USA' if country == 'United States' else 'CAN'}\n"
                f"DCS{f_dcs}\nDAC{f_dac}\nDAG{f_dag}\nDAI{f_dai}\nDAJ{st_code}\nDAK{f_dak}\n"
                f"DAQ{f_daq}\nDBB{f_dbb}\nDBD{f_dbd}\nDBA{f_dba}\nDBC{f_dbc}\nDAU{f_dau}\nDAY{f_day}\nDCF{f_dcf}"
            )

            res_a, res_b = st.columns([1, 1.2])
            
            with res_a:
                st.markdown(f'<div class="purple-label">{txt["res_raw"]}</div>', unsafe_allow_html=True)
                st.code(raw_str, language="text")
            
            with res_b:
                st.markdown(f'<div class="purple-label">{txt["res_preview"]}</div>', unsafe_allow_html=True)
                # Encodage PDF417
                codes = encode(raw_str, columns=m_cols)
                img = render_image(codes, scale=max(1, int(res_dpi/100)), padding=q_zone)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.image(buf.getvalue(), use_container_width=True)
                
                # Téléchargement
                st.download_button("Export PNG High-Res", buf.getvalue(), "aamva_payload.png", "image/png", use_container_width=True)

        except Exception:
            st.error("Engine failure")
            st.code(traceback.format_exc())

# ==============================================================================
# MAINTENANCE DU SCRIPT (LIGNE 500)
# ==============================================================================
