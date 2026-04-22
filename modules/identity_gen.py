import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION DU CHEMIN ET IMPORTS CORE
# ==============================================================================
# Ajout du répertoire parent au chemin système pour les imports de modules internes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    # Fallback pour le développement local si les utilitaires sont manquants
    IIN_US = {"California": "603273"}
    IIN_CA = {"Quebec": "604428"}

# ==============================================================================
# MOTEUR CSS : LIQUID GLASS UI (EDITION PROFESSIONNELLE)
# ==============================================================================
# Ce bloc définit l'identité visuelle de l'application sans aucun emoji.
# Focus sur la réfraction, les flous et les dégradés néon.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    /* Configuration globale du viewport */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #030303;
        color: #ffffff;
    }

    /* Animation d'entrée des cartes */
    @keyframes cardArrival {
        from { transform: translateY(40px); opacity: 0; }
        to { transform: translateY(0px); opacity: 1; }
    }

    /* Conteneur de section style Crystal Slab */
    .crystal-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 24px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,255,255,0.02);
        animation: cardArrival 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    /* --- SLIDERS PROFESSIONNELS (OPTICAL CONFIG) --- */
    /* Masquage des éléments natifs Streamlit redondants */
    div[data-testid="stTickBar"] { display: none !important; }
    
    /* Rail du slider style verre fumé */
    div[data-baseweb="slider"] > div:first-child {
        height: 10px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Remplissage du slider avec dégradé progressif */
    div[role="presentation"] > div > div:first-child {
        background: linear-gradient(90deg, #7000ff 0%, #0072ff 100%) !important;
        height: 10px !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(112, 0, 255, 0.5) !important;
    }

    /* Curseur (Thumb) style capsule de verre poli */
    div[role="slider"] {
        height: 22px !important;
        width: 22px !important;
        background-color: #ffffff !important;
        border: 4px solid #7000ff !important;
        box-shadow: 0 0 25px rgba(112, 0, 255, 0.8) !important;
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    div[role="slider"]:hover {
        transform: scale(1.25) !important;
        cursor: grab;
    }

    /* --- INPUTS ET SELECTS (GLASSMOPHISM NOIR) --- */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #e0e0e0 !important;
        padding: 12px 20px !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus {
        border-color: #0072ff !important;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.2), inset 0 2px 8px rgba(0,0,0,0.4) !important;
        background: rgba(0, 0, 0, 0.4) !important;
    }

    /* --- BOUTONS D'ACTION (PILL DESIGN) --- */
    div.stButton > button, div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 60px !important;
        padding: 15px 45px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.3) !important;
        transition: all 0.4s ease !important;
        width: 100% !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(112, 0, 255, 0.1) 0%, rgba(0, 114, 255, 0.1) 100%) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-5px);
        box-shadow: 0 18px 36px rgba(0, 114, 255, 0.3) !important;
    }

    /* --- TYPOGRAPHIE ET ELEMENTS DE CONTROLE --- */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    .status-badge {
        font-family: 'Monaco', 'Consolas', monospace;
        background: rgba(0, 114, 255, 0.08);
        color: #00bfff;
        padding: 6px 14px;
        border-radius: 10px;
        border: 1px solid rgba(0, 114, 255, 0.2);
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 10px;
    }

    .svg-container svg {
        max-width: 100% !important;
        height: auto !important;
        max-height: 450px !important;
        display: block;
        margin: 0 auto;
        filter: drop-shadow(0 20px 40px rgba(0,0,0,0.7));
    }

    /* Styles spécifiques pour les labels de widgets */
    label p {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
    }

    /* Custom scrollbar pour l'aspect sombre */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #030303; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# LOGIQUE PRINCIPALE DU GÉNÉRATEUR
# ==============================================================================
def show_identity_gen(lang="EN"):
    """
    Affiche le générateur de données AAMVA avec l'interface Liquid Glass.
    Arguments:
        lang (str): 'EN' ou 'FR' pour la langue de l'interface.
    """

    # Définition des textes (Sans Emoji)
    TEXT = {
        "EN": {
            "title": "Quantum AAMVA Interface",
            "desc": "High-fidelity digital payload engine for forensic research",
            "step1": "Jurisdiction Analysis",
            "country": "Source Nation",
            "state": "Regional State",
            "prov": "Regional Province",
            "step2": "Identity Matrix Parameters",
            "step3": "Optical Engine Configuration",
            "generate": "Execute Matrix Generation",
            "success": "Sequence generation completed successfully.",
            "raw": "AAMVA Raw String",
            "use": "Standardized payload for external renderers.",
            "preview": "Digital Preview"
        },
        "FR": {
            "title": "Interface Quantum AAMVA",
            "desc": "Moteur de payload numérique haute fidélité pour la recherche légale",
            "step1": "Analyse de Juridiction",
            "country": "Nation Source",
            "state": "État Régional",
            "prov": "Province Régionale",
            "step2": "Paramètres de la Matrice d'Identité",
            "step3": "Configuration du Moteur Optique",
            "generate": "Exécuter la génération de la matrice",
            "success": "Génération de la séquence terminée avec succès.",
            "raw": "Chaîne brute AAMVA",
            "use": "Payload standardisé pour les moteurs de rendu externes.",
            "preview": "Aperçu numérique"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # En-tête de l'application
    st.title(t["title"])
    st.markdown(f"*{t['desc']}*")
    st.divider()

    # --- ÉTAPE 1 : SELECTION DE LA JURIDICTION ---
    # Cette étape définit l'IIN (Issuer Identification Number) pour le header AAMVA
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step1"])
    
    col_geo_1, col_geo_2 = st.columns(2)
    with col_geo_1:
        country = st.selectbox(t["country"], ["Canada", "United States"])

    with col_geo_2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            # Quebec par défaut selon l'exemple utilisateur
            available_provinces = sorted(IIN_CA.keys())
            default_idx = available_provinces.index("Quebec") if "Quebec" in available_provinces else 0
            region = st.selectbox(t["prov"], available_provinces, index=default_idx)
            mock_iin = IIN_CA[region]
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : MATRICE DE DONNÉES D'IDENTITÉ ---
    # Champs obligatoires pour la norme AAMVA (Format 2005-2020)
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step2"])
    
    col_data_a, col_data_b = st.columns(2)
    with col_data_a:
        # DCG est dynamique en fonction de la sélection de l'étape 1
        default_dcg_val = "CAN" if country == "Canada" else "USA"
        dcg = st.text_input("DCG - Country Identifier", default_dcg_val)
        
        dac = st.text_input("DAC - Given Names", "JEAN")
        dcs = st.text_input("DCS - Family Name", "NICOLAS")
        dbb = st.text_input("DBB - Date of Birth (YYYYMMDD)", "19941208")
        daq = st.text_input("DAQ - Identification Number", "N2420-941208-96")
        dag = st.text_input("DAG - Residential Street", "1560 SHERBROOKE ST E")
        
    with col_data_b:
        dai = st.text_input("DAI - Locality / City", "MONTREAL")
        dak = st.text_input("DAK - Postal / Zip Code", "H2L 4M1")
        dbd = st.text_input("DBD - Issue Date (YYYYMMDD)", "20230510")
        dba = st.text_input("DBA - Expiry Date (YYYYMMDD)", "20310509")
        dbc = st.selectbox("DBC - Biological Sex (1:M / 2:F)", ["1", "2"], index=0)
        dcf = st.text_input("DCF - Document Discriminator", "PEJQ04N96")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 3 : CONFIGURATION OPTIQUE (MOTEUR PRO) ---
    # Paramètres de rendu pour le code-barres PDF417
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.subheader(t["step3"])

    col_cfg_1, col_cfg_2 = st.columns(2)
    with col_cfg_1:
        dpi_value = st.select_slider(
            "RENDER RESOLUTION DENSITY (DPI)", 
            options=[72, 150, 300, 600, 1200], 
            value=600
        )
        # Calcul de l'échelle relative pour le rendu image
        scale_factor = max(1, int(dpi_value / 40))
        
        matrix_cols = st.slider("MATRIX COLUMN DENSITY", 1, 30, 10)
        
    with col_cfg_2:
        matrix_padding = st.slider("QUIET ZONE PADDING", 0, 50, 5)
        
        st.write("") # Espacement vertical
        use_escape_seq = st.checkbox("FORMAT PAYLOAD WITH ESCAPE SEQUENCES (\\n)", value=True)
        
        # Affichage du statut technique du moteur
        engine_status = f"ENGINE STATUS: {dpi_value} DPI | ACTIVE SCALE: {scale_factor}X"
        st.markdown(f'<div class="status-badge">{engine_status}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================================================================
    # LOGIQUE D'EXÉCUTION ET GÉNÉRATION DES RÉSULTATS
    # ==============================================================================
    if st.button(t["generate"], use_container_width=True):

        try:
            # Détermination du code de province (DAJ)
            province_code = "QC" if region == "Quebec" else region[:2].upper()
            
            # Assemblage du Header AAMVA (Format standard)
            # Structure : ANSI + IIN + Version + DL + Offsets
            aamva_header_str = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # Construction de la chaîne de données brute
            # Le caractère '@' est le marqueur de début de fichier AAMVA
            raw_payload = (
                f"@\n{aamva_header_str}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{province_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])
            st.divider()

            # --- AFFICHAGE DES RÉSULTATS ---
            # Layout en deux colonnes pour le code et l'image
            res_col_left, res_col_right = st.columns([1, 1.4])

            with res_col_left:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(t["raw"])
                
                # Formatage de sortie pour l'utilisateur
                final_output_str = raw_payload.replace("\n", "\\n") if use_escape_seq else raw_payload
                st.code(final_output_str, language="text")
                st.info(t["use"])
                st.markdown('</div>', unsafe_allow_html=True)

            with res_col_right:
                st.markdown('<div class="crystal-card" style="text-align:center;">', unsafe_allow_html=True)
                st.subheader(t["preview"])
                
                # Génération du code-barres PDF417
                try:
                    barcode_codes = encode(raw_payload, columns=matrix_cols)
                    barcode_image = render_image(barcode_codes, scale=scale_factor, padding=matrix_padding)

                    # Préparation du buffer pour l'export PNG
                    png_buffer = io.BytesIO()
                    barcode_image.save(png_buffer, format="PNG", dpi=(dpi_value, dpi_value))
                    png_data_bytes = png_buffer.getvalue()

                    # Affichage de l'aperçu
                    st.image(png_data_bytes, use_column_width=True)

                    # Section des téléchargements (Boutons Pill)
                    dl_col_1, dl_col_2 = st.columns(2)
                    with dl_col_1:
                        st.download_button(
                            label=f"EXPORT PNG ({dpi_value} DPI)",
                            data=png_data_bytes,
                            file_name=f"PAYLOAD_{dcs}_{region}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Logique vectorielle SVG (Potrace)
                    potrace_bin_path = shutil.which("potrace")
                    vector_svg_content = None
                    
                    if potrace_bin_path:
                        try:
                            vector_svg_content = png_to_svg(png_bytes=png_data_bytes, potrace_path=potrace_bin_path)
                            with dl_col_2:
                                st.download_button(
                                    label="EXPORT SVG VECTOR",
                                    data=vector_svg_content,
                                    file_name=f"PAYLOAD_{dcs}_{region}.svg",
                                    mime="image/svg+xml",
                                    use_container_width=True
                                )
                        except Exception as svg_err:
                            st.error(f"SVG Error: {str(svg_err)}")
                    else:
                        with dl_col_2:
                            st.button("VECTOR ENGINE OFFLINE", disabled=True, use_container_width=True)

                    # Inspecteur vectoriel pour vérification de précision
                    if vector_svg_content:
                        with st.expander("INSPECT VECTOR CONTENT"):
                            st.markdown(
                                f'<div class="svg-container" style="background:white; padding:25px; border-radius:12px;">{vector_svg_content}</div>', 
                                unsafe_allow_html=True
                            )
                except Exception as gen_err:
                    st.error(f"Barcode Generation Error: {str(gen_err)}")
                
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as global_err:
            st.error("CRITICAL ENGINE FAULT")
            st.code(traceback.format_exc())

# ==============================================================================
# DOCUMENTATION ET MAINTENANCE
# ==============================================================================
# Ce module est conçu pour être intégré dans une application Streamlit multi-pages.
# Il respecte les normes AAMVA pour les codes-barres de permis de conduire.
# Aucune modification n'a été apportée aux payloads pour garantir la validité.
# Design : Liquid Glass UI Kit - Zero Emoji Edition.
# ==============================================================================
