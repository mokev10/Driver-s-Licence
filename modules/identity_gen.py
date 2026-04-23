import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# ==============================================================================

# CONFIGURATION ET IMPORTS SYSTÈME

# ==============================================================================

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(**file**), "..")))

try:
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
from utils.svg_vectorizer import png_to_svg
except ImportError:
IIN_US = {"California": "603273", "New York": "603219"}
IIN_CA = {"Quebec": "604428", "Ontario": "604430"}

# ==============================================================================

# CSS GLOBAL FINAL (UNIFIÉ + CORRIGÉ)

# ==============================================================================

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: #020203;
    color: #ffffff;
}

/* Animation */
@keyframes cardGlowFade {
    0% { transform: translateY(20px); opacity: 0; }
    100% { transform: translateY(0px); opacity: 1; }
}

/* Cartes */
.crystal-card {
    background: rgba(255,255,255,0.015);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 40px;
    margin-bottom: 35px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    animation: cardGlowFade 0.8s ease;
}

/* ===== SLIDER ===== */
div[data-testid="stTickBar"] { display: none !important; }

div[data-baseweb="slider"] > div:first-child {
    height: 14px !important;
    background: rgba(255,255,255,0.05) !important;
    border-radius: 20px !important;
}

/* progress */
div[role="presentation"] > div > div:first-child {
    background: linear-gradient(90deg, #8122ff, #3a82ff) !important;
    border-radius: 20px !important;
}

/* thumb */
div[role="slider"] {
    height: 28px !important;
    width: 28px !important;
    background: #fff !important;
    border: 5px solid #8122ff !important;
    box-shadow: 0 0 25px rgba(129,34,255,0.8) !important;
}

/* ===== INPUTS ===== */
.stTextInput input, .stSelectbox [data-baseweb="select"] {
    background: rgba(10,10,12,0.6) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f2f2f2 !important;
}

/* ===== BOUTONS UNIFIÉS ===== */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(129,34,255,0.25), rgba(58,130,255,0.25)) !important;
    backdrop-filter: blur(25px) !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 80px !important;
    padding: 18px 50px !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    box-shadow: 0 15px 30px rgba(0,0,0,0.4) !important;
    transition: all 0.4s ease !important;
}

/* hover */
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #8122ff, #3a82ff) !important;
    transform: translateY(-5px);
    box-shadow: 0 20px 45px rgba(129,34,255,0.5) !important;
}

/* active */
div.stButton > button:active,
div.stDownloadButton > button:active {
    transform: scale(0.96);
}

/* ===== VISUEL ===== */
.flag-container {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 15px 25px;
    background: rgba(255,255,255,0.03);
    border-radius: 80px;
}

.flag-image {
    width: 48px;
}

.jurisdiction-title {
    font-size: 1.4rem;
    font-weight: 900;
}

/* FIX LABEL */
label p {
    color: rgba(200,200,255,0.6) !important;
    font-size: 0.75rem !important;
}

</style>

""", unsafe_allow_html=True)

# ==============================================================================

# UI PRINCIPALE

# ==============================================================================

def show_identity_gen():

```
st.title("Quantum AAMVA Studio")
st.divider()

st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

country_choice = st.selectbox("Country", ["Canada", "United States"])

region = st.selectbox(
    "Region",
    list(IIN_CA.keys()) if country_choice=="Canada" else list(IIN_US.keys())
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="crystal-card">', unsafe_allow_html=True)

name = st.text_input("Name", "JEAN")
surname = st.text_input("Surname", "NICOLAS")

st.markdown('</div>', unsafe_allow_html=True)

if st.button("Initialize Generation Sequence", use_container_width=True):

    raw = f"{name}-{surname}-{region}"

    st.success("Generated")

    col1, col2 = st.columns(2)

    with col1:
        st.code(raw)

    with col2:
        fake_img = b"123"  # placeholder

        st.download_button(
            "EXPORT PNG",
            data=fake_img,
            file_name="test.png",
            use_container_width=True
        )

        st.download_button(
            "EXPORT SVG VECTOR",
            data=fake_img,
            file_name="test.svg",
            use_container_width=True
        )
```
