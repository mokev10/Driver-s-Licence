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
# CSS (FULL + FLOATING MENU + ANIMATIONS)
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

/* ================= FLOATING MENU ================= */
.floating-menu {
    width: 100%;
    max-width: 750px;
    margin-top: 20px;
    background: #0f172a;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
}

.menu-header {
    display: flex;
    justify-content: space-between;
    padding: 14px;
    background: #111827;
    color: white;
    font-weight: bold;
}

.close-btn {
    cursor: pointer;
    color: #ff4d4d;
}

.menu-body {
    padding: 16px;
    color: white;
    font-family: monospace;
}

.param-box {
    margin-bottom: 12px;
    padding: 10px;
    border-radius: 10px;
    background: rgba(255,255,255,0.05);
}

.param-box input,
.param-box select {
    width: 100%;
    margin-top: 6px;
    padding: 6px;
    border-radius: 6px;
    border: none;
    background: #1f2937;
    color: white;
}

.param-box small {
    color: #9ca3af;
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
            "step1": "Step 1: Select country and region",
            "country": "Select Country",
            "state": "Select State",
            "prov": "Select Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Barcode Parameters",
            "generate": "GENERATE BARCODE & STRING",

            "escape": "Escape Sequences",
            "escape_help": "Use \\n for line breaks",
            "human": "Human readable text",
            "module": "Module width (mm)",
            "dpi": "Resolution (DPI)",
            "format": "Image format",
            "padding": "Padding (quiet zone)",

            "success": "HDR generation completed"
        },
        "FR": {
            "title": "Générateur AAMVA",
            "desc": "Outil avancé de génération de données forensic",
            "step1": "Étape 1 : Sélection pays et région",
            "country": "Pays",
            "state": "État",
            "prov": "Province",
            "step2": "Étape 2 : Champs obligatoires",
            "step3": "Étape 3 : Paramètres du code-barres",
            "generate": "GÉNÉRER CODE & CHAÎNE",

            "escape": "Séquences d'échappement",
            "escape_help": "Utiliser \\n pour retour ligne",
            "human": "Texte lisible",
            "module": "Largeur module (mm)",
            "dpi": "Résolution (DPI)",
            "format": "Format image",
            "padding": "Zone de silence",

            "success": "Génération terminée"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # ================= HEADER =================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox(t["country"], ["United States", "Canada"])

    # ✅ ICON RESTAURÉ EXACTEMENT COMME DEMANDÉ
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

    # ================= STEP 2 =================
    st.markdown(
        f"""
        <div class="step-animated-delay-1 overlay-box">
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

    # ================= STEP 3 FLOATING MENU =================
    escape = st.checkbox(t["escape"], value=True)

    st.markdown(f"""
    <div class="floating-menu">
        <div class="menu-header">
            <span>{t["step3"]}</span>
            <span class="close-btn">✕</span>
        </div>

        <div class="menu-body">

            <div class="param-box">
                <b>{t["escape"]}</b><br>
                <small>{t["escape_help"]}</small><br>
                <input type="checkbox" {"checked" if escape else ""}>
            </div>

            <div class="param-box">
                <b>{t["human"]}</b><br>
                <input type="checkbox">
            </div>

            <div class="param-box">
                <b>{t["module"]}</b><br>
                <input type="text" value="0.254">
            </div>

            <div class="param-box">
                <b>{t["dpi"]}</b><br>
                <input type="text" value="600">
            </div>

            <div class="param-box">
                <b>{t["format"]}</b><br>
                <select>
                    <option>PNG</option>
                    <option>SVG</option>
                </select>
            </div>

            <div class="param-box">
                <b>{t["padding"]}</b><br>
                <input type="text" value="3">
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ================= GENERATION =================
    if st.button(t["generate"], use_container_width=True):

        try:
            header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

            raw = (
                f"@\n{header}\n"
                f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
                f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
                f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            )

            # IMPORTANT: escape mode
            display_raw = raw.replace("\n", "\\n") if escape else raw

            st.success(t["success"])

            col1, col2 = st.columns(2)

            with col1:
                st.code(display_raw)

            codes = encode(raw, columns=10)
            image = render_image(codes, scale=3, padding=3)

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            with col2:
                st.image(png_bytes)

                st.download_button("📥 PNG", png_bytes, file_name=f"{dcs}.png")

                potrace_path = shutil.which("potrace")
                svg = None

                if potrace_path:
                    try:
                        svg = png_to_svg(png_bytes, potrace_path)
                    except:
                        pass

                if svg:
                    st.download_button("📥 SVG", svg, file_name=f"{dcs}.svg")

                    st.markdown(f"""
                    <div class="step-fade overlay-box">
                        {svg}
                    </div>
                    """, unsafe_allow_html=True)

        except Exception:
            st.error(traceback.format_exc())
