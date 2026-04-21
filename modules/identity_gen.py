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
# GLASSMORPHISM + ANIMATIONS (FULL UI LAYER)
# =========================
st.markdown(
    """
    <style>

    body {
        background: radial-gradient(circle at top, #0f172a, #020617);
    }

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
        from {opacity: 0;}
        to {opacity: 1;}
    }

    .wizard-step {
        animation: slideUp 0.8s ease-out;
    }

    .wizard-step-delay {
        animation: slideUp 1.1s ease-out;
    }

    .glass {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 18px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    }

    .title {
        font-size: 22px;
        font-weight: 600;
        color: white;
    }

    .subtitle {
        font-size: 14px;
        opacity: 0.7;
        color: white;
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
            "desc": "Advanced forensic-grade AAMVA generator",
            "step1": "Step 1 — Location Setup",
            "step2": "Step 2 — Identity Fields",
            "country": "Select Country",
            "state": "Select State",
            "prov": "Select Province",
            "generate": "GENERATE",
            "success": "Generation completed"
        },
        "FR": {
            "title": "Générateur AAMVA",
            "desc": "Génération avancée de données AAMVA",
            "step1": "Étape 1 — Localisation",
            "step2": "Étape 2 — Champs identité",
            "country": "Pays",
            "state": "État",
            "prov": "Province",
            "generate": "GÉNÉRER",
            "success": "Génération terminée"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # =========================
    # HEADER (GLASS)
    # =========================
    st.markdown(f"""
    <div class="glass wizard-step">
        <div class="title">{t["title"]}</div>
        <div class="subtitle">{t["desc"]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # STEP 1 (ALWAYS VISIBLE)
    # =========================
    st.markdown(f"<div class='glass wizard-step'><b>{t['step1']}</b></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    # DCG auto mapping (SMART LINK)
    dcg = "USA" if country == "United States" else "CAN"

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    # =========================
    # STEP VALIDATION (WIZARD TRIGGER)
    # =========================
    step2_ready = country is not None and region is not None

    # =========================
    # STEP 2 (ONLY WHEN READY)
    # =========================
    if step2_ready:

        st.markdown(f"""
        <div class="glass wizard-step-delay">
            <b>{t["step2"]}</b>
        </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            st.markdown("<div class='glass'>DCG (Country Code auto)</div>", unsafe_allow_html=True)
            dcg_input = st.text_input("DCG", dcg, disabled=True)

            dcs = st.text_input("DCS (Last Name)", "NICOLAS")
            dac = st.text_input("DAC (First Name)", "JEAN")
            dbb = st.text_input("DBB (Birth)", "19941208")
            daq = st.text_input("DAQ (License)", "D9823415")
            dag = st.text_input("DAG (Address)", "1560 STREET")

        with colB:
            dai = st.text_input("DAI (City)", "CITY")
            dak = st.text_input("DAK (Postal)", "POSTAL")
            dbd = st.text_input("DBD (Issue)", "20230510")
            dba = st.text_input("DBA (Expiry)", "20310509")
            dbc = st.selectbox("DBC (Gender)", ["1", "2", "3"])
            dcf = st.text_input("DCF (ID)", "REF001")

        st.divider()

        # =========================
        # GENERATION
        # =========================
        if st.button(t["generate"], use_container_width=True):

            try:
                aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

                raw = (
                    f"@\n{aamva_header}\n"
                    f"DCG{dcg_input}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                    f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                    f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
                )

                st.success(t["success"])

                col1, col2 = st.columns(2)

                with col1:
                    st.code(raw.replace("\n", "\\n"))

                # BARCODE
                codes = encode(raw, columns=10)
                image = render_image(codes, scale=3, padding=3)

                buf = io.BytesIO()
                image.save(buf, format="PNG")
                png_bytes = buf.getvalue()

                with col2:
                    st.image(png_bytes)

                    st.download_button(
                        "PNG",
                        png_bytes,
                        file_name=f"{dcs}.png",
                        mime="image/png"
                    )

                    # SVG OPTIONAL
                    potrace_path = shutil.which("potrace")
                    svg = None

                    if potrace_path:
                        try:
                            svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                        except:
                            pass

                    if svg:
                        st.download_button(
                            "SVG",
                            svg,
                            file_name=f"{dcs}.svg",
                            mime="image/svg+xml"
                        )

            except Exception:
                st.error(traceback.format_exc())
