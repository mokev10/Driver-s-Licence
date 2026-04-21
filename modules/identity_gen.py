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

# =========================
# IMPORTS
# =========================
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .overlay-box {
        padding: 14px;
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# MAIN
# =========================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced forensic PDF417 generator",

            "step1": "Step 1: Location",
            "country": "Country",
            "state": "State",
            "prov": "Province",

            "step2": "Step 2: Required fields",

            "step3": "Step 3: PDF417 Parameters",
            "generate": "GENERATE BARCODE & STRING",
            "success": "Generation completed",

            # PDF417 settings
            "pdf417_settings": "PDF417 Settings",
            "type": "Type: PDF417",
            "escape": "Escape sequences",
            "eval_escape": "Evaluate escape sequences (\\n \\t \\F)",
            "human": "Human readable text",
            "module": "Module width: 0.254 mm",
            "dpi": "Resolution (DPI)",
            "format": "Image format",

            "preview": "Preview",
            "png": "Download PNG",
            "svg": "Download SVG"
        },

        "FR": {
            "title": "Générateur AAMVA",
            "desc": "Générateur PDF417 forensic avancé",

            "step1": "Étape 1 : Localisation",
            "country": "Pays",
            "state": "État",
            "prov": "Province",

            "step2": "Étape 2 : Champs obligatoires",

            "step3": "Étape 3 : Paramètres PDF417",
            "generate": "GÉNÉRER CODE-BARRES & CHAÎNE",
            "success": "Génération terminée",

            # PDF417 settings
            "pdf417_settings": "Paramètres PDF417",
            "type": "Type : PDF417",
            "escape": "Séquences d'échappement",
            "eval_escape": "Évaluer les séquences (\\n \\t \\F)",
            "human": "Texte lisible humain",
            "module": "Largeur module : 0.254 mm",
            "dpi": "Résolution (DPI)",
            "format": "Format image",

            "preview": "Aperçu",
            "png": "Télécharger PNG",
            "svg": "Télécharger SVG"
        }
    }

    t = TEXT[lang]

    # =========================
    # HEADER
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

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.markdown(
        f"""
        <div class="overlay-box">
            <img src="{icon}" width="24">
            <h3>{t["step1"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================
    # PDF417 FULL SETTINGS (RESTORED)
    # =========================
    st.markdown(f"### {t['pdf417_settings']}")

    colS1, colS2 = st.columns(2)

    with colS1:
        escape_sequences = st.checkbox(t["escape"], value=True)
        eval_escape = st.checkbox(t["eval_escape"], value=True)
        human_readable = st.checkbox(t["human"], value=False)

    with colS2:
        dpi = st.number_input(t["dpi"], 72, 1200, 600, 50)
        format_img = st.selectbox(t["format"], ["PNG", "SVG"])

    st.markdown(f"- {t['type']}")
    st.markdown(f"- {t['module']}")

    st.divider()

    # =========================
    # INPUTS
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
    # GENERATE
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

            # escape handling
            if escape_sequences:
                display = raw.replace("\n", "\\n").replace("\t", "\\t").replace("\\F", "FNC1")
            else:
                display = raw

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {t['preview']}")
                st.code(display)

            # =========================
            # BARCODE
            # =========================
            codes = encode(raw, columns=10)
            image = render_image(codes, scale=3, padding=3)

            buf = io.BytesIO()
            image.save(buf, format="PNG", dpi=(dpi, dpi))
            png_bytes = buf.getvalue()

            with col2:
                st.image(png_bytes)

                st.download_button(
                    t["png"],
                    png_bytes,
                    file_name=f"{dcs}.png",
                    mime="image/png"
                )

                if format_img == "SVG":
                    potrace_path = shutil.which("potrace")
                    if potrace_path:
                        svg = png_to_svg(png_bytes, potrace_path)
                        st.download_button(
                            t["svg"],
                            svg,
                            file_name=f"{dcs}.svg",
                            mime="image/svg+xml"
                        )
                        st.markdown(svg, unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
