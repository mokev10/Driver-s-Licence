import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# PATH FIX (important pour imports)
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =========================
# IMPORTS
# =========================
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# ANIMATION CSS (AUGMENTÉE - STRICTEMENT CONSERVÉE)
# =========================
st.markdown(
    """
    <style>

    @keyframes slideUp {
        from {
            transform: translateY(80px);
            opacity: 0;
        }
        to {
            transform: translateY(0px);
            opacity: 1;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .step-animated {
        animation: slideUp 0.8s ease-out;
    }

    .step-animated-delay-1 {
        animation: slideUp 1.0s ease-out;
    }

    .step-animated-delay-2 {
        animation: slideUp 1.2s ease-out;
    }

    .step-fade {
        animation: fadeIn 1.5s ease-in;
    }

    .overlay-box {
        padding: 14px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 10px;
    }

    /* Style spécifique pour les réglages DPI */
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

    # =========================
    # HEADER (STEP 1 FIXED VISIBLE)
    # =========================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    st.markdown(
        f"""
        <div class="step-animated overlay-box">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="{icon}" width="24">
                <h3 style="margin:0;">{t["step1"]}</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

    # =========================
    # STEP 2 TITLE (ANIMATED LAYER)
    # =========================
    st.markdown(
        f"""
        <div class="step-animated-delay-1 overlay-box">
            <h3>{t["step2"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # FORM INPUTS (INTÉGRAUX)
    # =========================
    colA, colB = st.columns(2)

    with colA:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D9823415")
        dag = st.text_input("DAG", "1560 STREET")

    with colB:
        dai = st.text_input("DAI", "CITY")
        dak = st.text_input("DAK", "POSTAL")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")
        dbc = st.selectbox("DBC", ["1", "2", "3"])
        dcf = st.text_input("DCF", "REF001")

    st.divider()

    # =========================
    # STEP 3 : PARAMÉTRAGE TECHNIQUE (AJOUTÉ SANS SIMPLIFIER)
    # =========================
    st.markdown(
        f"""
        <div class="step-animated-delay-2 overlay-box">
            <h3>{t["step3"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_cfg1, c_cfg2, c_cfg3, c_cfg4 = st.columns(4)
    with c_cfg1:
        # Réglage DPI réel
        dpi_val = st.select_slider("Resolution (DPI)", options=[72, 150, 300, 600, 1200], value=600)
        # Calcul du scale pour le rendu (Scale 15 = env. 600 DPI)
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
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            # Code état (DAJ)
            state_code = "QC" if region == "Quebec" else region[:2].upper()
            
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # Chaîne brute intégrale
            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{state_code}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])

            col1_res, col2_res = st.columns(2)

            with col1_res:
                st.subheader(t["raw"])
                # Affichage selon choix échappement
                display_raw = raw.replace("\n", "\\n") if use_escape else raw
                st.code(display_raw)

            # =========================
            # BARCODE GENERATION
            # =========================
            with col2_res:
                st.subheader(t["preview"])
                
                codes = encode(raw, columns=barcode_columns)
                # Utilisation du scale dynamique calculé par rapport au DPI
                image = render_image(codes, scale=calc_scale, padding=barcode_padding)

                buf = io.BytesIO()
                # Sauvegarde avec injection des métadonnées DPI dans le PNG
                image.save(buf, format="PNG", dpi=(dpi_val, dpi_val))
                png_bytes = buf.getvalue()

                st.image(png_bytes)

                st.download_button(
                    f"📥 PNG ({dpi_val} DPI)",
                    png_bytes,
                    file_name=f"{dcs}_{dpi_val}dpi.png",
                    mime="image/png"
                )

                # =========================
                # SVG GENERATION (SAFE + OPTIONAL)
                # =========================
                potrace_path = shutil.which("potrace")
                svg = None

                if potrace_path:
                    try:
                        svg = png_to_svg(
                            png_bytes=png_bytes,
                            potrace_path=potrace_path
                        )
                    except Exception as e:
                        st.warning(f"SVG error: {e}")
                else:
                    st.info("SVG non disponible (potrace absent)")

                if svg:
                    st.download_button(
                        "📥 SVG vectoriel",
                        svg,
                        file_name=f"{dcs}.svg",
                        mime="image/svg+xml"
                    )

                    st.markdown(
                        f"""
                        <div class="step-fade overlay-box">
                            {svg}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        except Exception:
            st.error(traceback.format_exc())
