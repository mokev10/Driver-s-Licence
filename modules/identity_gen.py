import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# PATH FIX (STRICTEMENT CONSERVÉ)
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =========================
# IMPORTS
# =========================
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# ANIMATION CSS (STRICTEMENT CONSERVÉE ET UNIFIÉE)
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

    /* UNIFICATION DES BOUTONS SANS TOUCHER AU RESTE */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(37, 117, 252, 0.5) !important;
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%) !important;
    }

    .dpi-info {
        color: #4facfe;
        font-weight: bold;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# MAIN FUNCTION
# =========================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced tool for generating forensic-quality AAMVA raw data strings",
            "step1": "Step 1: Select the country and state or province",
            "country": "Select Country",
            "state": "Select State/Territory",
            "prov": "Select Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Configuration & Generation",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed.",
            "raw": "Raw Data String",
            "use": "Use this string in external tools.",
            "preview": "Preview"
        },
        "FR": {
            "title": "Générateur de données AAMVA",
            "desc": "Outil avancé pour générer des chaînes AAMVA",
            "step1": "Étape 1 : Choisir le pays et la région",
            "country": "Sélectionner le Pays",
            "state": "Sélectionner l'État/Territoire",
            "prov": "Sélectionner la Province",
            "step2": "Étape 2 : Champs obligatoires (AAMVA)",
            "step3": "Étape 3 : Configuration & Génération",
            "generate": "GÉNÉRER LE CODE-BARRES & LA CHAÎNE",
            "success": "Génération terminée.",
            "raw": "Chaîne brute",
            "use": "Utilisez cette chaîne dans vos outils externes.",
            "preview": "Aperçu"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # =========================
    # HEADER (STEP 1 - Configuration du Permis)
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        # Basé sur l'image, c'est un permis canadien
        country = st.selectbox(t["country"], ["Canada", "United States"])

    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States" else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    st.markdown(f"""<div class="step-animated overlay-box"><div style="display:flex;align-items:center;gap:10px;"><img src="{icon}" width="24"><h3 style="margin:0;">{t["step1"]}</h3></div></div>""", unsafe_allow_html=True)

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            # Basé sur l'image, la province est le Québec. J'utilise 'Quebec' comme valeur par défaut.
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()), index=sorted(IIN_CA.keys()).index("Quebec"))
            mock_iin = IIN_CA[region]

    st.divider()

    # =========================
    # STEP 2: SAISIE DES DONNÉES (MISES À JOUR SELON L'IMAGE EXEMPLE)
    # =========================
    st.markdown(f"""<div class="step-animated-delay-1 overlay-box"><h3>{t["step2"]}</h3></div>""", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        # Valeurs mises à jour d'après l'image ejemplo
        dcg = st.text_input("DCG (Country)", "CAN") # Canada
        dac = st.text_input("DAC (First Name)", "JEAN")
        dcs = st.text_input("DCS (Last Name)", "NICOLAS")
        dbb = st.text_input("DBB (Date of Birth YYYYMMDD)", "19941208") # 1994-12-08
        daq = st.text_input("DAQ (License Number)", "N2420-941208-96")
        dag = st.text_input("DAG (Address)", "1560 SHERBROOKE ST E")
    with colB:
        dai = st.text_input("DAI (City)", "MONTREAL")
        dak = st.text_input("DAK (Postal Code)", "H2L 4M1")
        dbd = st.text_input("DBD (Issue Date YYYYMMDD)", "20230510") # Validé le : 2023-05-10
        dba = st.text_input("DBA (Expiry Date YYYYMMDD)", "20310509") # Expire le : 2031-05-09
        dbc = st.selectbox("DBC (Sex M=1, F=2)", ["1", "2"], index=0) # Sexe : M (Homme = 1 dans AAMVA)
        dcf = st.text_input("DCF (Document Discriminator / Ref N°)", "PEJQ04N96") # N° de référence

    st.divider()

    # =========================
    # STEP 3: CONFIGURATION TECHNIQUE (STRICTEMENT CONSERVÉE)
    # =========================
    st.markdown(f"""<div class="step-animated-delay-2 overlay-box"><h3>{t["step3"]}</h3></div>""", unsafe_allow_html=True)

    c_cfg1, c_cfg2, c_cfg3, c_cfg4 = st.columns(4)
    with c_cfg1:
        dpi_val = st.select_slider("Resolution (DPI)", options=[72, 150, 300, 600, 1200], value=600)
        calc_scale = max(1, int(dpi_val / 40))
    with c_cfg2:
        barcode_padding = st.slider("Padding", 0, 50, 3)
    with c_cfg3:
        barcode_columns = st.slider("Columns", 1, 30, 10)
    with c_cfg4:
        use_escape = st.checkbox("Escape Sequences (\\n)", value=True)

    st.markdown(f'<p class="dpi-info">Active Render: {dpi_val} DPI | Scale: {calc_scale}</p>', unsafe_allow_html=True)
    st.divider()

    # =========================
    # GENERATION LOGIC (STRICTEMENT CONSERVÉE)
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            # Détermination du code de l'état/province (DAJ)
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            
            # Utilisation de la version AAMVA 2005 (05) pour correspondre au format Header existant
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # Construction de la chaîne brute intégrale avec tous les champs saisis
            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{state_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])

            # --- RÉSULTATS UI/UX OPTIMISÉS (ORGANISATION SANS SUPPRESSION DE CODE) ---
            res_left, res_right = st.columns([1, 1.2])

            with res_left:
                st.subheader(t["raw"])
                display_raw = raw.replace("\n", "\\n") if use_escape else raw
                st.code(display_raw)
                st.info(t["use"])

            with res_right:
                st.subheader(t["preview"])
                codes = encode(raw, columns=barcode_columns)
                image = render_image(codes, scale=calc_scale, padding=barcode_padding)

                buf = io.BytesIO()
                image.save(buf, format="PNG", dpi=(dpi_val, dpi_val))
                png_bytes = buf.getvalue()

                st.image(png_bytes, use_column_width=True)

                # Boutons de téléchargement côte à côte
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    st.download_button(f"📥 PNG ({dpi_val} DPI)", png_bytes, f"{dcs}.png", "image/png", use_container_width=True)
                
                potrace_path = shutil.which("potrace")
                svg = None
                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                        with btn_c2:
                            st.download_button("📥 SVG VECTORIEL", svg, f"{dcs}.svg", "image/svg+xml", use_container_width=True)
                    except Exception as e: 
                        st.warning(f"SVG error: {e}")

                if svg:
                    with st.expander("👁️ View SVG Data"):
                        st.markdown(f'<div class="step-fade overlay-box" style="background:white;">{svg}</div>', unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
