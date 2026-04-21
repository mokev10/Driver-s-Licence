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
# CSS ANIMATION (IMPORTANT)
# =========================
def inject_animation_css():
    st.markdown(
        """
        <style>

        /* container animation */
        .fade-slide {
            animation: fadeSlide 0.9s ease-out forwards;
            transform: translateY(40px);
            opacity: 0;
        }

        @keyframes fadeSlide {
            to {
                transform: translateY(0px);
                opacity: 1;
            }
        }

        .block {
            padding: 10px;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================
# MAIN FUNCTION
# =========================
def show_identity_gen(lang="EN"):

    inject_animation_css()

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
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # =========================
    # INTERFACE 1 (TOUJOURS VISIBLE)
    # =========================
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

    st.markdown(
        f"""
        <div class="fade-slide block">
            <h3>{t["step1"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================
    # INTERFACE 2 (OVERLAY + ANIMATION)
    # =========================
    show_second_ui = True  # toujours affiché (pas de remplacement)

    if show_second_ui:

        st.markdown(
            f"""
            <div class="fade-slide block">
                <h3>{t["step2"]}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

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

            except Exception:
                st.error(traceback.format_exc())
