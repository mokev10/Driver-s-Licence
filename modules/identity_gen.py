import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


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


def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced tool for generating forensic-quality AAMVA raw data strings",
            "step1": "Step 1: Select country and region",
            "country": "Select Country",
            "state": "Select State",
            "prov": "Select Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "generate": "GENERATE BARCODE",
            "success": "Generation completed"
        },
        "FR": {
            "title": "Générateur AAMVA",
            "desc": "Outil de génération avancée",
            "step1": "Étape 1 : Sélection",
            "country": "Pays",
            "state": "État",
            "prov": "Province",
            "step2": "Étape 2 : Champs",
            "generate": "GÉNÉRER",
            "success": "Terminé"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

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

    step2_ready = country and region

    if step2_ready:

        st.markdown(f"<div class='step-animated-delay-1'>{t['step2']}</div>", unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            dcg = st.text_input("DCG", dcg_auto, disabled=True)
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

        if st.button(t["generate"]):

            try:
                header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

                raw = (
                    f"@\n{header}\n"
                    f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                    f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                    f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
                )

                st.success(t["success"])

                st.code(raw)

                codes = encode(raw, columns=10)
                image = render_image(codes, scale=3, padding=3)

                buf = io.BytesIO()
                image.save(buf, format="PNG")

                st.image(buf.getvalue())

            except Exception as e:
                st.error(str(e))
    else:
        st.info("Sélectionnez pays + région")
