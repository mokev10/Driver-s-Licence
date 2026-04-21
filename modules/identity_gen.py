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
# SESSION STATE (WIZARD CONTROL - IMPORTANT)
# =========================
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

if "country_selected" not in st.session_state:
    st.session_state.country_selected = ""

if "region_selected" not in st.session_state:
    st.session_state.region_selected = ""


# =========================
# CSS ANIMATIONS + GLASSMORPHISM (FULL VERSION)
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
        from {opacity:0;}
        to {opacity:1;}
    }

    .glass {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 16px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .step1 {
        animation: slideUp 0.8s ease-out;
    }

    .step2 {
        animation: slideUp 1.1s ease-out;
    }

    .step3 {
        animation: fadeIn 1.2s ease-in;
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
            "step1": "Step 1 — Location Selection",
            "step2": "Step 2 — Identity Fields",
            "country": "Select Country",
            "state": "Select State",
            "prov": "Select Province",
            "generate": "GENERATE BARCODE",
            "locked": "Complete Step 1 to continue"
        }
    }

    t = TEXT[lang]

    # =========================
    # HEADER (NO MODIFICATION)
    # =========================
    st.title(t["title"])
    st.write(t["desc"])

    st.divider()

    # =========================
    # STEP 1 (ALWAYS VISIBLE)
    # =========================
    st.markdown(f"<div class='glass step1'><b>{t['step1']}</b></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    # SAVE STATE
    st.session_state.country_selected = country

    with col2:
        if country == "United States":
            region = st.selectbox(t["state"], sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    # SAVE STATE
    st.session_state.region_selected = region

    # =========================
    # REAL VALIDATION (NO FAKE CONDITION)
    # =========================
    step2_enabled = (
        st.session_state.country_selected is not None
        and st.session_state.country_selected != ""
        and st.session_state.region_selected is not None
        and st.session_state.region_selected != ""
    )

    st.divider()

    # =========================
    # STEP 2 (ONLY IF VALID)
    # =========================
    if step2_enabled:

        st.markdown(f"<div class='glass step2'><b>{t['step2']}</b></div>", unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            dcg = "USA" if country == "United States" else "CAN"
            dcg_input = st.text_input("DCG (Auto Country Code)", dcg, disabled=True)

            dcs = st.text_input("DCS (Surname)", "NICOLAS")
            dac = st.text_input("DAC (First Name)", "JEAN")
            dbb = st.text_input("DBB (Birth Date)", "19941208")
            daq = st.text_input("DAQ (License ID)", "D9823415")
            dag = st.text_input("DAG (Address)", "1560 STREET")

        with colB:
            dai = st.text_input("DAI (City)", "CITY")
            dak = st.text_input("DAK (Postal Code)", "POSTAL")
            dbd = st.text_input("DBD (Issue Date)", "20230510")
            dba = st.text_input("DBA (Expiry Date)", "20310509")
            dbc = st.selectbox("DBC (Gender)", ["1", "2", "3"])
            dcf = st.text_input("DCF (Document ID)", "REF001")

        st.divider()

        # =========================
        # GENERATION (FULL LOGIC PRESERVED)
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

                st.success("Generation completed")

                col1, col2 = st.columns(2)

                with col1:
                    st.code(raw.replace("\n", "\\n"))

                # =========================
                # BARCODE GENERATION
                # =========================
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

                    # =========================
                    # SVG (OPTIONAL - FULL PRESERVED LOGIC)
                    # =========================
                    potrace_path = shutil.which("potrace")
                    svg = None

                    if potrace_path:
                        try:
                            svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                        except Exception:
                            pass

                    if svg:
                        st.download_button(
                            "SVG",
                            svg,
                            file_name=f"{dcs}.svg",
                            mime="image/svg+xml"
                        )

                        st.markdown(
                            f"<div class='glass step3'>{svg}</div>",
                            unsafe_allow_html=True
                        )

            except Exception:
                st.error(traceback.format_exc())

    else:
        # =========================
        # LOCKED STATE (NO STEP 2)
        # =========================
        st.info("Step 2 locked — complete country and region selection")
