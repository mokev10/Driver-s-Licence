import streamlit as st
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

    .box {
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
# MAIN APP
# =========================
def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA PDF417 Generator",
            "desc": "Forensic-grade PDF417 generator (TEC-IT style parameters)",
            "step1": "Step 1: Country Selection",
            "step2": "Step 2: Required Fields",
            "step3": "Step 3: Barcode Parameters",
            "generate": "GENERATE PDF417",
            "success": "Generation completed"
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
        country = st.selectbox("Select Country", ["United States", "Canada"])

    with col2:
        if country == "United States":
            region = st.selectbox("State", sorted(IIN_US.keys()))
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox("Province", sorted(IIN_CA.keys()))
            mock_iin = IIN_CA[region]

    st.divider()

    # =========================
    # STEP 2 INPUTS
    # =========================
    st.markdown(f"<div class='step-animated-delay-1 box'><h3>{t['step2']}</h3></div>", unsafe_allow_html=True)

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
    # STEP 3 - FULL PARAMETERS
    # =========================
    st.markdown(f"<div class='step-animated-delay-2 box'><h3>{t['step3']}</h3></div>", unsafe_allow_html=True)

    with st.expander("PDF417 Parameters (TEC-IT Style)", expanded=True):

        # ✔ PARAMETRES EXACTS DEMANDÉS
        code_type = st.selectbox("Type de code", ["PDF417"], index=0)

        escape_sequences = st.checkbox(
            "Séquences d'échappement (activé)",
            value=True
        )

        eval_escape = st.checkbox(
            "Évaluer les séquences d'évasion (\\n, \\t, \\F)",
            value=True
        )

        show_human_readable = st.checkbox(
            "Show Human Readable Text (OFF recommandé)",
            value=False
        )

        module_width = st.number_input(
            "Largeur de module (mm)",
            value=0.254,
            step=0.001
        )

        dpi = st.number_input(
            "Résolution (DPI)",
            value=600,
            step=50
        )

        image_format = st.selectbox(
            "Format d'image",
            ["PNG", "SVG"]
        )

    st.divider()

    # =========================
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        try:
            header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            # =========================
            # ESCAPE ENGINE (REALISTIC)
            # =========================
            sep = "\n"

            raw = (
                f"@{sep}"
                f"{header}{sep}"
                f"DCG{dcg}{sep}"
                f"DCS{dcs}{sep}"
                f"DAC{dac}{sep}"
                f"DBB{dbb}{sep}"
                f"DAQ{daq}{sep}"
                f"DAG{dag}{sep}"
                f"DAI{dai}{sep}"
                f"DAJ{region[:2].upper()}{sep}"
                f"DAK{dak}{sep}"
                f"DBD{dbd}{sep}"
                f"DBA{dba}{sep}"
                f"DBC{dbc}{sep}"
                f"DCF{dcf}"
            )

            # ✔ ESCAPE EVALUATION LOGIC (TEC-IT STYLE SIMULATION)
            if eval_escape:
                raw = raw.replace("\\n", "\n").replace("\\t", "\t").replace("\\F", "\x1c")

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.code(raw.replace("\n", "\\n"))

            # =========================
            # PDF417 GENERATION
            # =========================
            codes = encode(raw, columns=10)

            image = render_image(
                codes,
                scale=3,
                padding=3
            )

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

                svg = None
                potrace_path = shutil.which("potrace")

                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes=png_bytes, potrace_path=potrace_path)
                    except Exception as e:
                        st.warning(f"SVG error: {e}")

                if svg:
                    st.download_button(
                        "📥 SVG",
                        svg,
                        file_name=f"{dcs}.svg",
                        mime="image/svg+xml"
                    )

                    st.markdown(f"<div class='step-fade box'>{svg}</div>", unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
