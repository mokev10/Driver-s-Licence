import streamlit as st
import os
import sys

# =========================
# FORCE ROOT PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# =========================
# IMPORTS SAFE (NO PACKAGE IMPORT)
# =========================
import importlib.util

# Load utils/helpers.py
helpers_path = os.path.join(BASE_DIR, "utils", "helpers.py")
spec_helpers = importlib.util.spec_from_file_location("helpers", helpers_path)
helpers = importlib.util.module_from_spec(spec_helpers)
spec_helpers.loader.exec_module(helpers)

header_component = helpers.header_component

# Load modules/identity_gen.py
identity_path = os.path.join(BASE_DIR, "modules", "identity_gen.py")
spec_identity = importlib.util.spec_from_file_location("identity_gen", identity_path)
identity_gen = importlib.util.module_from_spec(spec_identity)
spec_identity.loader.exec_module(identity_gen)

show_identity_gen = identity_gen.show_identity_gen


# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="AI Generator PDF417",
    page_icon="https://img.icons8.com/external-inipagistudio-mixed-inipagistudio/24/external-ai-web-programmer-inipagistudio-mixed-inipagistudio.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# TEXTS
# =========================
TEXTS = {
    "EN": {
        "theme_dark": "🌙 Dark",
        "theme_light": "☀️ Light",
        "sidebar_title": "🪪 Identity Gen",
        "sidebar_info": "Identity generation module is active.",
    },
    "FR": {
        "theme_dark": "🌙 Sombre",
        "theme_light": "☀️ Clair",
        "sidebar_title": "🪪 Générateur d'identité",
        "sidebar_info": "Module de génération actif.",
    }
}


# =========================
# BUTTON STYLE + CENTER FIX
# =========================
st.markdown("""
<style>

/* CENTRAGE RÉEL DU BOUTON */
div.stButton {
    display: flex;
    justify-content: center;
}

/* STYLE DU BOUTON */
div.stButton > button {
    background: linear-gradient(135deg, #4facfe 0%, #a066ff 100%) !important;
    color: white !important;
    border: none !important;
    padding: 10px 25px !important;
    border-radius: 50px !important;
    font-weight: bold !important;
    box-shadow: 0 0 15px rgba(160, 102, 255, 0.5) !important;
    transition: all 0.3s ease !important;
    height: auto !important;
    width: auto !important;
}

/* HOVER */
div.stButton > button:hover {
    box-shadow: 0 0 25px rgba(255, 0, 0, 0.78)) !important;
    transform: scale(1.02) !important;
    color: white !important;
}

/* CLICK */
div.stButton > button:active {
    transform: scale(0.98) !important;
}

</style>
""", unsafe_allow_html=True)


def apply_custom_style(dark_mode=True):
    bg = "#0E1117" if dark_mode else "#FFFFFF"
    text = "#FAFAFA" if dark_mode else "#000000"
    card = "#161B22" if dark_mode else "#F5F5F5"

    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {bg};
                color: {text};
            }}
            section[data-testid="stSidebar"] {{
                background-color: {card};
            }}
        </style>
    """, unsafe_allow_html=True)


def main():

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "lang" not in st.session_state:
        st.session_state.lang = "EN"

    t = TEXTS[st.session_state.lang]

    col1, col2, col3 = st.columns([10, 1, 1])

    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    with col3:
        lang = st.selectbox(
            "",
            ["EN", "FR"],
            index=0 if st.session_state.lang == "EN" else 1,
            label_visibility="collapsed"
        )

        if lang != st.session_state.lang:
            st.session_state.lang = lang
            st.rerun()

    apply_custom_style(st.session_state.dark_mode)

    with st.sidebar:
        st.markdown(f"### {t['sidebar_title']}")
        st.info(t["sidebar_info"])

    header_component()

    show_identity_gen(st.session_state.lang)


if __name__ == "__main__":
    main()


