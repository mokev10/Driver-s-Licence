import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION ET IMPORTS SYSTÈME
# ==============================================================================
# Extension du path pour garantir l'accès aux utilitaires (ajuster selon structure)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    # Fallback pour environnement de développement ou standalone
    IIN_US = {
        "California": "603273", "New York": "603219", "Florida": "603290",
        "Texas": "603285", "Illinois": "603277", "Nevada": "603261"
    }
    IIN_CA = {
        "Quebec": "604428", "Ontario": "604430", "Alberta": "604432", 
        "British Columbia": "604434"
    }

# Configuration de la page Streamlit
st.set_page_config(page_title="Quantum AAMVA Studio", layout="wide")

# ==============================================================================
# MOTEUR DE STYLE LIQUID GLASS - VERSION PRO 500
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #020203;
        color: #ffffff;
    }

    /* Animation de déploiement des cartes Crystal */
    @keyframes cardGlowFade {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0px); opacity: 1; }
    }

    .crystal-card {
        background: rgba(255, 255, 255, 0.015);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        animation: cardGlowFade 0.9s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* --- SLIDERS PROFESSIONNELS --- */
    div[data-testid="stTickBar"] { display: none !important; }
    div[data-baseweb="slider"] > div:first-child {
        height: 14px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 20px !important;
    }

    div[role="presentation"] > div > div:first-child {
        background: linear-gradient(90deg, #8122ff 0%, #3a82ff 100%) !important;
        height: 14px !important;
        border-radius: 20px !important;
    }

    div[role="slider"] {
        height: 28px !important;
        width: 28px !important;
        background-color: #ffffff !important;
        border: 5px solid #8122ff !important;
        box-shadow: 0 0 20px rgba(129, 34, 255, 0.9) !important;
    }

    /* --- INPUTS TEXTE ET CHAMPS DE SELECTION --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(10, 10, 12, 0.6) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f2f2f2 !important;
        padding: 14px 22px !important;
    }

    /* --- BOUTONS D'ACTION PILL --- */
    div.stButton > button, div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 80px !important;
        padding: 18px 50px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2.5px !important;
        transition: all 0.4s ease !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(129, 34, 255, 0.2), rgba(58, 130, 255, 0.2)) !important;
        border-color: #ffffff !important;
        transform: translateY(-3px);
    }

    .flag-container {
        display: flex; align-items: center; gap: 20px;
        margin-bottom: 25px; padding: 15px 25px;
        background: rgba(255, 255, 255, 0.03); border-radius: 20px;
    }

    .flag-image { width: 48px; height: auto; border-radius: 6px; }

    .jurisdiction-title {
        font-size: 1.4rem; font-weight: 600;
        background: linear-gradient(to right, #fff, #999);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .engine-status-tag {
        font-family: 'JetBrains Mono', monospace; color: #00e5ff;
        background: rgba(0, 229, 255, 0.08); padding: 8px 18px;
        border-radius: 12px; border: 1px solid rgba(0, 229, 255, 0.3);
        font-size: 0.85rem; display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# LOGIQUE MÉTIER ET INTERFACE
# ==============================================================================
def show_identity_gen():
    # Gestion du sélecteur de langue en haut de page
    lang = st.sidebar.selectbox("SYSTEM LANGUAGE", ["FR", "EN"])

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

    ui = DICTIONARY[lang]

    st.title(ui["title"])
    st.markdown(f"*{ui['desc']}*")
    st.divider()

    # --- ÉTAPE 1 : JURIDICTION ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    col_geo_left, col_geo_right = st.columns(2)
    
    with col_geo_left:
        country_choice = st.selectbox(ui["country"], ["Canada", "United States"])
        flag_url = (
            "https://cdn-icons-png.flaticon.com/512/323/323310.png" if country_choice == "United States" 
            else "https://cdn-icons-png.flaticon.com/512/323/323277.png"
        )
        st.markdown(
            f'<div class="flag-container"><img src="{flag_url}" class="flag-image">'
            f'<span class="jurisdiction-title">{ui["step1"]}</span></div>', 
            unsafe_allow_html=True
        )

    with col_geo_right:
        if country_choice == "United States":
            region_name = st.selectbox(ui["state"], sorted(IIN_US.keys()))
            active_iin = IIN_US[region_name]
        else:
            prov_list = sorted(IIN_CA.keys())
            def_prov_idx = prov_list.index("Quebec") if "Quebec" in prov_list else 0
            region_name = st.selectbox(ui["prov"], prov_list, index=def_prov_idx)
            active_iin = IIN_CA[region_name]
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : MATRICE DE DONNÉES ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step2"])
    
    f_a, f_b = st.columns(2)
    with f_a:
        iso_country = "CAN" if country_choice == "Canada" else "USA"
        val_dcg = st.text_input("DCG - ISO Country", iso_country)
        val_dac = st.text_input("DAC - Given Names", "JEAN")
        val_dcs = st.text_input("DCS - Surname", "NICOLAS")
        val_dbb = st.text_input("DBB - Date of Birth (YYYYMMDD)", "19941208")
        val_daq = st.text_input("DAQ - License Identifier", "N2420-941208-96")
        
    with f_b:
        val_dag = st.text_input("DAG - Residential Street", "1560 SHERBROOKE ST E")
        val_dai = st.text_input("DAI - City", "MONTREAL")
        val_dak = st.text_input("DAK - Postal Code", "H2L 4M1")
        val_dbd = st.text_input("DBD - Issue Date", "20230510")
        val_dbc = st.selectbox("DBC - Gender (1:M / 2:F)", ["1", "2"])
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : CONFIGURATION OPTIQUE ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step3"])
    o_1, o_2 = st.columns(2)
    with o_1:
        res_dpi = st.select_slider("RENDER RESOLUTION (DPI)", options=[72, 150, 300, 600], value=300)
        matrix_density = st.slider("MATRIX COLUMN COUNT", 1, 30, 12)
    with o_2:
        quiet_padding = st.slider("QUIET ZONE PADDING", 0, 50, 5)
        escape_mode = st.checkbox("USE ESCAPE SEQUENCES (\\n)", value=True)
        st.markdown(f'<div class="engine-status-tag">ACTIVE: {res_dpi} DPI</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- GÉNÉRATION ---
    if st.button(ui["generate"], use_container_width=True):
        try:
            region_code = "QC" if region_name == "Quebec" else region_name[:2].upper()
            # Construction simplified AAMVA
            aamva_head = f"ANSI {active_iin}050102DL00410287ZO02900045DL"
            raw_string = (
                f"@\n{aamva_head}\nDCG{val_dcg}\nDCS{val_dcs}\nDAC{val_dac}\nDBB{val_dbb}\n"
                f"DAQ{val_daq}\nDAG{val_dag}\nDAI{val_dai}\nDAJ{region_code}\nDAK{val_dak}\n"
                f"DBD{val_dbd}\nDBC{val_dbc}"
            )

            st.success(ui["success"])
            out_l, out_r = st.columns([1, 1.2])

            with out_l:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["raw"])
                disp = raw_string.replace("\n", "\\n") if escape_mode else raw_string
                st.code(disp, language="text")
                st.markdown('</div>', unsafe_allow_html=True)

            with out_r:
                st.markdown('<div class="crystal-card" style="text-align:center;">', unsafe_allow_html=True)
                st.subheader(ui["preview"])
                
                # Rendu PDF417
                codes = encode(raw_string, columns=matrix_density)
                # Calcul auto du scale par rapport au DPI (DPI 300 ~ Scale 8)
                dynamic_scale = max(2, int(res_dpi / 40))
                img = render_image(codes, scale=dynamic_scale, padding=quiet_padding)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                data_png = buf.getvalue()
                
                st.image(data_png, use_column_width=True)
                
                # Téléchargement
                st.download_button(
                    label=f"DOWNLOAD PNG ({res_dpi} DPI)",
                    data=data_png,
                    file_name=f"GEN_{region_code}_{val_dcs}.png",
                    mime="image/png",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception:
            st.error("SYSTEM ERROR")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    show_identity_gen()
