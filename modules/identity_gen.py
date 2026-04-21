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

    @keyframes slideUp {
        from { transform: translateY(80px); opacity: 0; }
        to { transform: translateY(0px); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .step-animated { animation: slideUp 0.8s ease-out; }
    .step-animated-delay-1 { animation: slideUp 1.0s ease-out; }
    .step-animated-delay-2 { animation: slideUp 1.2s ease-out; }
    .step-fade { animation: fadeIn 1.5s ease-in; }

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
            "step3": "Step 3: Barcode Parameters",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation completed."
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

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
    # STEP 2
    # =========================
    st.markdown(f"<div class='step-animated-delay-1 overlay-box'><h3>{t['step2']}</h3></div>", unsafe_allow_html=True)

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
    # STEP 3 (AJOUT SIMPLE + NON MODIFIÉ)
    # =========================
    st.markdown(f"<div class='step-animated-delay-2 overlay-box'><h3>{t['step3']}</h3></div>", unsafe_allow_html=True)

    escape_sequences = st.checkbox("Escape Sequences (use \\n)", value=True)
    show_human_readable = st.checkbox("Show Human Readable Text", value=False)

    st.divider()

    # =========================
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # ✔ STRICT ORIGINAL STRUCTURE
            if escape_sequences:
                nl = "\\n"
            else:
                nl = "\n"

            raw = (
                f"@{nl}"
                f"{aamva_header}{nl}"
                f"DCG{dcg}{nl}"
                f"DCS{dcs}{nl}"
                f"DAC{dac}{nl}"
                f"DBB{dbb}{nl}"
                f"DAQ{daq}{nl}"
                f"DAG{dag}{nl}"
                f"DAI{dai}{nl}"
                f"DAJ{region[:2].upper()}{nl}"
                f"DAK{dak}{nl}"
                f"DBD{dbd}{nl}"
                f"DBA{dba}{nl}"
                f"DBC{dbc}{nl}"
                f"DCF{dcf}"
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

                st.download_button("📥 PNG", png_bytes, file_name=f"{dcs}.png", mime="image/png")

                potrace_path = shutil.which("potrace")
                svg = None

                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                    except Exception as e:
                        st.warning(f"SVG error: {e}")

                if svg:
                    st.download_button("📥 SVG", svg, file_name=f"{dcs}.svg", mime="image/svg+xml")
                    st.markdown(f"<div class='step-fade overlay-box'>{svg}</div>", unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
