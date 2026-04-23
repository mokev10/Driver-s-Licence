import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================
# CONFIGURATION PATH
# ==============================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ==============================================================================
# IMPORTS AVEC FALLBACK
# ==============================================================================
try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    IIN_US = {"California": "603273", "New York": "603219"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430"}

# ==============================================================================
# CSS GLOBAL PRO (UNIFIÉ)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: #020203;
    color: #ffffff;
}

/* Cards */
.crystal-card {
    background: rgba(255,255,255,0.015);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 35px;
    margin-bottom: 30px;
}

/* Slider */
div[data-testid="stTickBar"] { display: none !important; }

div[data-baseweb="slider"] > div:first-child {
    height: 14px !important;
    background: rgba(255,255,255,0.05) !important;
    border-radius: 20px !important;
}

div[role="presentation"] > div > div:first-child {
    background: linear-gradient(90deg, #8122ff, #3a82ff) !important;
    border-radius: 20px !important;
}

div[role="slider"] {
    height: 26px !important;
    width: 26px !important;
    background: #fff !important;
    border: 4px solid #8122ff !important;
}

/* Inputs */
.stTextInput input {
    background: rgba(10,10,12,0.6) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Buttons */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(129,34,255,0.25), rgba(58,130,255,0.25)) !important;
    color: white !important;
    border-radius: 60px !important;
    padding: 16px 40px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #8122ff, #3a82ff) !important;
    transform: translateY(-4px);
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# HELPERS
# ==============================================================================
def build_aamva(data):
    return f"@\\nANSI {data['iin']}\\nDCS{data['name']}"

def log_event(msg):
    print(f"[LOG] {msg}")

# ==============================================================================
# MAIN UI
# ==============================================================================
def show_identity_gen():

    st.title("Quantum AAMVA Studio")
    st.caption("Liquid Glass Engine")

    # =========================
    # SECTION GEO
    # =========================
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("Country", ["Canada", "United States"])

    with col2:
        region = st.selectbox(
            "Region",
            list(IIN_CA.keys()) if country=="Canada" else list(IIN_US.keys())
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # SECTION DATA
    # =========================
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", "JEAN")
        surname = st.text_input("Surname", "NICOLAS")

    with col2:
        birth = st.text_input("Birth", "19941208")
        city = st.text_input("City", "MONTREAL")

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # SECTION CONFIG
    # =========================
    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

    dpi = st.select_slider("DPI", [72,150,300,600], value=300)
    density = st.slider("Density", 1, 30, 10)

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # GENERATION
    # =========================
    if st.button("Initialize Generation Sequence", use_container_width=True):

        try:
            iin = IIN_CA.get(region) if country=="Canada" else IIN_US.get(region)

            data = {
                "iin": iin,
                "name": name
            }

            raw = build_aamva(data)

            st.success("Generated")

            col1, col2 = st.columns(2)

            with col1:
                st.code(raw)

            with col2:
                fake = b"123"

                st.download_button("EXPORT PNG", data=fake, file_name="test.png")
                st.download_button("EXPORT SVG VECTOR", data=fake, file_name="test.svg")

        except Exception:
            st.error("ERROR")
            st.code(traceback.format_exc())

# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    show_identity_gen()
