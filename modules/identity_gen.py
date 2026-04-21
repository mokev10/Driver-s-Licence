import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# PATH FIX
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# CSS (OPTIONNEL VISUEL)
# =========================
st.markdown("""
<style>

.field-help {
    font-size: 12px;
    opacity: 0.65;
    margin-top: -8px;
    margin-bottom: 8px;
}

.group-box {
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


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
            "step2": "Step 2: Required AAMVA Fields",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed.",
        },
        "FR": {
            "title": "Générateur de données AAMVA",
            "desc": "Outil avancé pour générer des chaînes AAMVA",
            "step1": "Étape 1 : Choisir le pays et la région",
            "country": "Sélectionner le Pays",
            "state": "Sélectionner l'État/Territoire",
            "prov": "Sélectionner la Province",
            "step2": "Étape 2 : Champs AAMVA requis",
            "generate": "GÉNÉRER LE CODE-BARRES & LA CHAÎNE",
            "success": "Génération terminée.",
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # =========================
    # HEADER
    # =========================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # =========================
    # STEP 1
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    dcg_auto = "USA" if country == "United States" else "CAN"

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

    # =========================
    # STEP 2 TITLE
    # =========================
    st.markdown(f"### {t['step2']}")

    colA, colB = st.columns(2)

    with colA:

        # =========================
        # DCG
        # =========================
        dcg = st.text_input("DCG (Country Code)", dcg_auto, disabled=True)
        st.markdown(
            "<div class='field-help'>"
            "DCG = Country Code (ISO / jurisdiction identifier). "
            "Auto-generated based on selected country."
            "</div>",
            unsafe_allow_html=True
        )

        # =========================
        # DCS
        # =========================
        dcs = st.text_input("DCS (Family Name)", "NICOLAS")
        st.markdown(
            "<div class='field-help'>"
            "DCS = Family Name / Last Name (surname of holder)."
            "</div>",
            unsafe_allow_html=True
        )

        # =========================
        # DAC
        # =========================
        dac = st.text_input("DAC (First Name)", "JEAN")
        st.markdown(
            "<div class='field-help'>"
            "DAC = First Name / Given Name."
            "</div>",
            unsafe_allow_html=True
        )

        dbb = st.text_input("DBB (Date of Birth)", "19941208")
        daq = st.text_input("DAQ (License Number)", "D9823415")
        dag = st.text_input("DAG (Address Line)", "1560 STREET")

    with colB:

        dai = st.text_input("DAI (City)", "CITY")
        dak = st.text_input("DAK (Postal Code)", "POSTAL")
        dbd = st.text_input("DBD (Issue Date)", "20230510")
        dba = st.text_input("DBA (Expiry Date)", "20310509")
        dbc = st.selectbox("DBC (Gender Code)", ["1", "2", "3"])
        dcf = st.text_input("DCF (Document Discriminator)", "REF001")

        st.markdown(
            "<div class='field-help'>"
            "DBC = Gender Code | DCF = Document unique identifier"
            "</div>",
            unsafe_allow_html=True
        )

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

                if svg:
                    st.download_button(
                        "📥 SVG vectoriel",
                        svg,
                        file_name=f"{dcs}.svg",
                        mime="image/svg+xml"
                    )

        except Exception:
            st.error(traceback.format_exc())
