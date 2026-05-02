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
# Extension du path pour garantir l'accès aux utilitaires de constantes et vecteurs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    # Fallback technique pour environnement de test
    IIN_US = {"California": "603273", "New York": "603219"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430"}

# ==============================================================================
# MOTEUR DE STYLE LIQUID GLASS - VERSION PRO 500
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Fond de page et conteneur principal */
   :root {
    --bg-color: #0E1117;
    --text-color: #FAFAFA;
}

.stApp {
    background-color: var(--bg-color) !important;
    color: var(--text-color) !important;
}


    /* Animation de déploiement des cartes Crystal */
    @keyframes cardGlowFade {
        0% { transform: translateY(20px); opacity: 0; box-shadow: 0 0 0 rgba(0,0,0,0); }
        100% { transform: translateY(0px); opacity: 1; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    }

    /* Styles des Cartes Crystal (Sections) */
    .crystal-card {
        background: rgba(255, 255, 255, 0.015);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6), inset 0 0 30px rgba(255,255,255,0.01);
        animation: cardGlowFade 0.9s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* --- SLIDERS PROFESSIONNELS (STYLE IMAGE 7D64EC) --- */
    div[data-testid="stTickBar"] { display: none !important; }
    
    /* Rail principal du slider */
    div[data-baseweb="slider"] > div:first-child {
        height: 14px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5) !important;
    }

    /* Barre de progression avec dégradé liquide */
    div[role="presentation"] > div > div:first-child {
        background: linear-gradient(90deg, #8122ff 0%, #3a82ff 100%) !important;
        height: 14px !important;
        border-radius: 20px !important;
        box-shadow: 0 0 20px rgba(129, 34, 255, 0.4) !important;
    }

    /* Curseur (Thumb) style capsule de verre poli */
    div[role="slider"] {
        height: 28px !important;
        width: 28px !important;
        background-color: #ffffff !important;
        border: 5px solid #8122ff !important;
        box-shadow: 0 0 30px rgba(129, 34, 255, 0.9), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[role="slider"]:hover {
        transform: scale(1.15) !important;
        box-shadow: 0 0 40px rgba(129, 34, 255, 1) !important;
    }

    /* --- INPUTS TEXTE ET CHAMPS DE SELECTION (NOIR GLASS) --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(10, 10, 12, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f2f2f2 !important;
        padding: 14px 22px !important;
        font-size: 1rem !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextInput input:focus {
        border-color: #3a82ff !important;
        background: rgba(15, 15, 20, 0.8) !important;
        box-shadow: 0 0 25px rgba(58, 130, 255, 0.2), inset 0 2px 10px rgba(0,0,0,0.5) !important;
    }

/* --- BOUTONS ULTRA BRILLANTS (VERSION FINAL FIX) --- */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(129, 34, 255, 0.12), rgba(58, 130, 255, 0.12)) !important;
    backdrop-filter: blur(25px) !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 80px !important;
    padding: 18px 50px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-size: 0.95rem !important;

    /* 🔥 GLOW PERMANENT */
    box-shadow: 
        0 0 25px rgba(129, 34, 255, 0.35),
        0 10px 30px rgba(0,0,0,0.5),
        inset 0 0 10px rgba(255,255,255,0.05) !important;

    transition: all 0.4s ease !important;

    /* ✨ animation douce continue */
    animation: glowPulse 3s infinite alternate;
}

/* 🔥 Animation breathing glow */
@keyframes glowPulse {
    0% {
        box-shadow: 
            0 0 15px rgba(129, 34, 255, 0.25),
            0 10px 25px rgba(0,0,0,0.4);
    }
    100% {
        box-shadow: 
            0 0 35px rgba(129, 34, 255, 0.6),
            0 15px 40px rgba(0,0,0,0.6);
    }
}

/* 🖱 Hover encore plus puissant */
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 
        0 0 50px rgba(129, 34, 255, 0.9),
        0 25px 60px rgba(129, 34, 255, 0.5) !important;
}

/* 🖱 Click */
div.stButton > button:active,
div.stDownloadButton > button:active {
    transform: scale(0.96);
}



    /* --- ELEMENTS VISUELS DE JURIDICTION --- */
    .flag-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 25px;
        padding: 15px 25px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .flag-image {
        width: 48px;
        height: auto;
        border-radius: 6px;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.5));
    }

    .jurisdiction-title {
        font-size: 1.4rem;
        font-weight: 600;
        background: linear-gradient(to right, #fff, #999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
/* ================================
   SVG INSIDE EXPANDER FIX (STABLE DARK MODE)
================================== */

.barcode-preview-box {
    background: rgba(0, 0, 0, 0.35) !important;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

/* SVG RENDER FIX */
.barcode-preview-box svg {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    filter: brightness(1.7) contrast(1.25) !important;
}

/* ================================
   STREAMLIT EXPANDER FIX (LOCK DARK MODE)
================================== */

/* HEADER */
details[data-testid="stExpander"] > summary {
    background: rgba(15, 15, 20, 0.75) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    padding: 10px 14px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}

/* FORCE TEXT COLOR INSIDE HEADER */
details[data-testid="stExpander"] > summary * {
    color: #ffffff !important;
}

/* CONTENT AREA */
details[data-testid="stExpander"] > div[role="region"] {
    background: rgba(10, 10, 15, 0.80) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 15px !important;
}

/* GLOBAL TEXT INSIDE EXPANDER */
details[data-testid="stExpander"] * {
    color: #ffffff !important;
}

/* ICON FIX */
details[data-testid="stExpander"] svg {
    fill: white !important;
}

/* ANTI LIGHT MODE GLITCH AFTER SVG RENDER */
details[data-testid="stExpander"][open] > summary {
    background: rgba(15, 15, 20, 0.85) !important;
    color: #ffffff !important;
}

/* ================================
   ENGINE TAG
================================== */

.engine-status-tag {
    font-family: 'JetBrains Mono', monospace;
    color: #00e5ff;
    background: rgba(0, 229, 255, 0.08);
    padding: 8px 18px;
    border-radius: 12px;
    border: 1px solid rgba(0, 229, 255, 0.3);
    font-size: 0.85rem;
    display: inline-block;
    letter-spacing: 1px;
}

/* ================================
   LABEL STYLE FIX (KEEP THIS)
================================== */

label p {
    color: rgba(255, 255, 255, 0.9) !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    margin-left: 5px !important;
}

/* HIGH CONTRAST FOR NOTIFICATIONS */
div[data-testid="stNotification"] * {
    color: #ffffff !important;
}

</style>
""",
unsafe_allow_html=True
)


# ==============================================================================
# LOGIQUE MÉTIER ET INTERFACE UTILISATEUR
# ==============================================================================
def show_identity_gen(lang="EN"):
    """
    Point d'entrée principal du module de génération d'identité.
    Gère le multilingue, les entrées utilisateur et le moteur de rendu PDF417.
    """

    # Matrice de traduction (SANS EMOJIS)
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

    # HEADER DE L'APPLICATION
    st.title(ui["title"])
    st.markdown(f"*{ui['desc']}*")
    st.divider()

    # --- ÉTAPE 1 : JURIDICTION ET DRAPEAUX DYNAMIQUES ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    
    col_geo_left, col_geo_right = st.columns(2)
    with col_geo_left:
        country_choice = st.selectbox(ui["country"], ["Canada", "United States"])

    # Sélection de l'URL du drapeau en fonction du pays (Image HD)
    flag_url = (
        "https://cdn-icons-png.flaticon.com/512/323/323310.png" # USA
        if country_choice == "United States" else 
        "https://cdn-icons-png.flaticon.com/512/323/323277.png" # Canada
    )

    # Affichage dynamique de l'en-tête de juridiction avec drapeau
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
            # Quebec par défaut comme spécifié
            prov_list = sorted(IIN_CA.keys())
            def_prov_idx = prov_list.index("Quebec") if "Quebec" in prov_list else 0
            region_name = st.selectbox(ui["prov"], prov_list, index=def_prov_idx)
            active_iin = IIN_CA[region_name]
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : MATRICE DE DONNÉES D'IDENTITÉ ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step2"])
    
    field_col_a, field_col_b = st.columns(2)
    with field_col_a:
        # Code Pays ISO dynamique
        iso_country = "CAN" if country_choice == "Canada" else "USA"
        val_dcg = st.text_input("DCG - ISO Country", iso_country)
        
        val_dac = st.text_input("DAC - Given Names", "JEAN")
        val_dcs = st.text_input("DCS - Surname", "NICOLAS")
        val_dbb = st.text_input("DBB - Date of Birth (YYYYMMDD)", "19941208")
        val_daq = st.text_input("DAQ - License Identifier", "N2420-941208-96")
        val_dag = st.text_input("DAG - Residential Street", "1560 SHERBROOKE ST E")
        
    with field_col_b:
        val_dai = st.text_input("DAI - City / Locality", "MONTREAL")
        val_dak = st.text_input("DAK - Postal Code", "H2L 4M1")
        val_dbd = st.text_input("DBD - Issue Date (YYYYMMDD)", "20230510")
        val_dba = st.text_input("DBA - Expiry Date (YYYYMMDD)", "20310509")
        val_dbc = st.selectbox("DBC - Gender (1:M / 2:F)", ["1", "2"], index=0)
        val_dcf = st.text_input("DCF - Audit Number", "PEJQ04N96")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : CONFIGURATION OPTIQUE (MOTEUR PRO) ---
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(ui["step3"])

    opt_col_1, opt_col_2 = st.columns(2)
    with opt_col_1:
        # Sélection de la densité DPI avec slider custom
        res_dpi = st.select_slider(
            "RENDER RESOLUTION DENSITY (DPI)", 
            options=[72, 150, 300, 600, 1200], 
            value=600
        )
        scale_val = max(1, int(res_dpi / 40))
        
        # Densité des colonnes de la matrice
        matrix_density = st.slider("MATRIX COLUMN COUNT", 1, 30, 10)
        
    with opt_col_2:
        # Zone de protection (Quiet Zone)
        quiet_padding = st.slider("QUIET ZONE PADDING", 0, 60, 5)
        
        st.write("") # Espacement cosmétique
        escape_mode = st.checkbox("FORMAT PAYLOAD WITH ESCAPE SEQUENCES (\\n)", value=True)
        
        # Badge d'état du moteur
        engine_msg = f"ENGINE READY: {res_dpi} DPI | SCALE: {scale_val}X"
        st.markdown(f'<div class="engine-status-tag">{engine_msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # EXÉCUTION DU MOTEUR DE GÉNÉRATION
    # ==============================================================================
    if st.button(ui["generate"], use_container_width=True):

        try:
            # Traitement du code de territoire (DAJ)
            region_code = "QC" if region_name == "Quebec" else region_name[:2].upper()
            
            # Reconstruction du Header AAMVA (Format Standard DL/ID)
            # Structure : ANSI + IIN + Version + DL + Offsets
            aamva_head = f"ANSI {active_iin}050102DL00410287ZO02900045DL"

            # Construction de la chaîne brute finale
            raw_string = (
                f"@\n{aamva_head}\n"
                f"DCG{val_dcg}\nDCS{val_dcs}\nDAC{val_dac}\nDBB{val_dbb}\nDAQ{val_daq}\n"
                f"DAG{val_dag}\nDAI{val_dai}\nDAJ{region_code}\nDAK{val_dak}\n"
                f"DBD{val_dbd}\nDBA{val_dba}\nDBC{val_dbc}\nDCF{val_dcf}"
            )

            st.success(ui["success"])
            st.divider()

            # --- AFFICHAGE DES RÉSULTATS (LAYOUT DUAL CRYSTAL) ---
            out_left, out_right = st.columns([1, 1.4])

            with out_left:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["raw"])
                
                # Formatage de sortie (Escape chars ou Newlines)
                display_string = raw_string.replace("\n", "\\n") if escape_mode else raw_string
                st.code(display_string, language="text")
                st.info(ui["use"])
                st.markdown('</div>', unsafe_allow_html=True)

            with out_right:
                st.markdown('<div class="crystal-card" style="text-align:center;">', unsafe_allow_html=True)
                st.subheader(ui["preview"])
                
                # Génération du code-barres PDF417 haute fidélité
                try:
                    gen_codes = encode(raw_string, columns=matrix_density)
                    gen_image = render_image(gen_codes, scale=scale_val, padding=quiet_padding)

                    # Conversion mémoire pour export PNG
                    mem_buffer = io.BytesIO()
                    gen_image.save(mem_buffer, format="PNG", dpi=(res_dpi, res_dpi))
                    data_png = mem_buffer.getvalue()

                    # Zone d'aperçu Crystal
                    st.image(data_png, use_column_width=True)

                    # Groupe de boutons de téléchargement (Style Pill Sans Emoji)
                    btn_col_1, btn_col_2 = st.columns(2)
                    with btn_col_1:
                        st.download_button(
                            label=f"EXPORT PNG ({res_dpi} DPI)",
                            data=data_png,
                            file_name=f"AAMVA_{val_dcs}_{region_name}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Traitement vectoriel SVG via moteur Potrace
                    path_potrace = shutil.which("potrace")
                    data_svg = None
                    
                    if path_potrace:
                        try:
                            data_svg = png_to_svg(png_bytes=data_png, potrace_path=path_potrace)
                            with btn_col_2:
                                st.download_button(
                                    label="EXPORT SVG VECTOR",
                                    data=data_svg,
                                    file_name=f"AAMVA_{val_dcs}_{region_name}.svg",
                                    mime="image/svg+xml",
                                    use_container_width=True
                                )
                        except Exception as svge:
                            st.error(f"Vectorization Fault: {str(svge)}")
                    else:
                        with btn_col_2:
                            st.button("VECTOR ENGINE OFFLINE", disabled=True, use_container_width=True)

                    # Accordéon d'inspection vectorielle
                    if data_svg:
                        with st.expander("DETAILED VECTOR INSPECTION"):
                            st.components.v1.html(
    f"""
    <div class="barcode-preview-box">
        {str(data_svg)}
    </div>
    """,
    height=500,
    scrolling=True
)

                except Exception as bar_err:
                    st.error(f"Render Engine Fault: {str(bar_err)}")
                
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception:
            st.error("CRITICAL SYSTEM FAILURE")
            st.code(traceback.format_exc())

# ==============================================================================
# FIN DU MODULE IDENTITY_GEN (500 LINES TARGET)DETAILED VECTOR INSPECTION
# ==============================================================================
# Ce code intègre désormais :
# 1. Gestion dynamique des drapeaux Canada/USA (Image URL HD).
# 2. Suppression totale des emojis sur les boutons et paragraphes.
# 3. Sliders "Pro" style Liquid Glass avec lueur violette.
# 4. Architecture de code étendue pour atteindre la limite de volume demandée.
