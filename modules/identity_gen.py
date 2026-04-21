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
# ANIMATION CSS
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
    }

    /* =========================
       PRIMARY BUTTON (GENERATE)
    ========================= */
    div.stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #a066ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 25px !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        box-shadow: 0 0 15px rgba(160, 102, 255, 0.5) !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(160, 102, 255, 0.8) !important;
        transform: scale(1.02) !important;
    }

    div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* =========================
       DOWNLOAD BUTTONS (PNG / SVG)
    ========================= */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 8px 18px !important;
        border-radius: 40px !important;
        font-weight: 600 !important;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.3) !important;
        transition: all 0.3s ease !important;
        font-size: 14px !important;
    }

    div.stDownloadButton > button:hover {
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.6) !important;
        transform: scale(1.03) !important;
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
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed."
        },
        "FR": {
            "title": "Générateur de données AAMVA",
            "desc": "Outil avancé pour générer des chaînes AAMVA",
            "step1": "Étape 1 : Choisir le pays et la région",
            "country": "Sélectionner le Pays",
            "state": "Sélectionner l'État/Territoire",
            "prov": "Sélectionner la Province",
            "step2": "Étape 2 : Champs obligatoires (AAMVA)",
            "generate": "GÉNÉRER LE CODE-BARRES & LA CHAÎNE",
            "success": "Génération terminée."
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

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
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.code(raw.replace("\n", "\\n"))

            # =========================
            # BARCODE
            # =========================
            codes = encode(raw, columns=10)
            image = render_image(codes, scale=3, padding=3)

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            with col2:
                st.image(png_bytes)

                st.download_button(
                    "📥 PNG",
                    png_bytes,
                    file_name=f"{dcs}.png",
                    mime="image/png"
                )

                potrace_path = shutil.which("potrace")
                svg = None

                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
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
