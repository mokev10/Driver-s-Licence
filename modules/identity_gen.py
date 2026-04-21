import streamlit as st
import io
import sys
import os
import shutil
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AAMVA Generator", layout="wide")


# =========================
# ANIMATION CSS
# =========================
st.markdown(
    """
    <style>

    /* fade + slide up */
    .fade-up {
        animation: fadeUp 0.8s ease forwards;
        opacity: 0;
        transform: translateY(30px);
    }

    @keyframes fadeUp {
        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }

    /* progressive sections delay */
    .step1 { animation-delay: 0.1s; }
    .step2 { animation-delay: 0.3s; }
    .step3 { animation-delay: 0.5s; }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# STATE CONTROL
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1


# =========================
# STEP 1 (INTRO + SELECTION)
# =========================
def step_one():

    st.markdown('<div class="fade-up step1">', unsafe_allow_html=True)

    st.title("AAMVA Raw Data Generator")
    st.subheader("Advanced tool for generating forensic-quality AAMVA raw data strings")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="fade-up step2">', unsafe_allow_html=True)
    st.write("Step 1: Select the country and state or province")

    country = st.selectbox("Select Country", ["Canada"])

    province = st.selectbox("Select Province", ["Alberta"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="fade-up step3">', unsafe_allow_html=True)

    if st.button("Continue →", use_container_width=True):
        st.session_state.country = country
        st.session_state.region = province
        st.session_state.step = 2
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# STEP 2 (FORM + GENERATION)
# =========================
def step_two():

    st.markdown(
        '<div class="fade-up step1">',
        unsafe_allow_html=True
    )

    st.title("AAMVA Generator")
    st.markdown("Configure identity fields")

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # INPUTS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        dcg = st.text_input("DCG", "USA")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D9823415")
        dag = st.text_input("DAG", "1560 STREET")

    with col2:
        dai = st.text_input("DAI", "CITY")
        dak = st.text_input("DAK", "POSTAL")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")
        dbc = st.selectbox("DBC", ["1", "2", "3"])
        dcf = st.text_input("DCF", "REF001")

    st.markdown("---")

    # =========================
    # GENERATION
    # =========================
    if st.button("Generate", use_container_width=True):

        try:
            mock_iin = 636014  # fallback safe value

            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            raw = (
                f"@\n{aamva_header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{st.session_state.region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            st.success("Generation completed")

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
                    "Download PNG",
                    png_bytes,
                    file_name=f"{dcs}.png",
                    mime="image/png"
                )

                # =========================
                # SVG SAFE GENERATION
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
                        "Download SVG",
                        svg,
                        file_name=f"{dcs}.svg",
                        mime="image/svg+xml"
                    )

        except Exception:
            st.error(traceback.format_exc())


# =========================
# ROUTER (TRANSITION SYSTEM)
# =========================
if st.session_state.step == 1:
    step_one()
else:
    step_two()
