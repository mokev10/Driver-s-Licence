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
# ANIMATION CSS
# =========================
st.markdown("""
<style>

@keyframes slideUp {
    from { transform: translateY(60px); opacity: 0; }
    to { transform: translateY(0px); opacity: 1; }
}

.step-animated {
    animation: slideUp 0.8s ease-out;
}

.step-animated-delay-1 {
    animation: slideUp 1.0s ease-out;
}

.overlay-box {
    padding: 12px;
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
            "step2": "Step 2: Required fields (AAMVA)",
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
            "step2": "Étape 2 : Champs obligatoires (AAMVA)",
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

    # =========================
    # DCG AUTO LINK (USER REQUEST)
    # =========================
    dcg_auto = "USA" if country == "United States" else "CAN"

    icon = (
        "https://img.icons8.com/external-justicon-flat-justicon/80/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/80/external-canada-countrys-flags-justicon-flat-justicon.png"
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
    # STEP 2 CONDITIONNEL (STRICT REQUEST)
    # =========================
    step2_ready = (country is not None and region is not None and country != "" and region != "")

    if step2_ready:

        st.markdown(f"""
            <div class="step-animated-delay-1 overlay-box">
                <h3>{t["step2"]}</h3>
                <small>DCG = Country Code (automatique)</small>
            </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            # DCG AUTO (locked + explained)
            dcg = st.text_input(
                "DCG (Country Code - auto)",
                value=dcg_auto,
                disabled=True,
                help="Code pays utilisé dans les standards AAMVA (USA / CAN)"
            )

            dac = st.text_input("DAC (First Name)", "JEAN")
            dcs = st.text_input("DCS (Last Name)", "NICOLAS")
            dbb = st.text_input("DBB (Birth Date YYYYMMDD)", "19941208")
            daq = st.text_input("DAQ (License Number)", "D9823415")
            dag = st.text_input("DAG (Address)", "1560 STREET")

        with colB:
            dai = st.text_input("DAI (City)", "CITY")
            dak = st.text_input("DAK (Postal Code)", "POSTAL")
            dbd = st.text_input("DBD (Issue Date)", "20230510")
            dba = st.text_input("DBA (Expiry Date)", "20310509")
            dbc = st.selectbox("DBC (Gender Code)", ["1", "2", "3"])
            dcf = st.text_input("DCF (Document Reference)", "REF001")

        st.divider()

        # =========================
        # GENERATION (UNCHANGED LOGIC)
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

        else:
            st.info("Complétez les sélections pour afficher Step 2")
