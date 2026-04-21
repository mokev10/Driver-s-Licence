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
    page_icon="🧾",
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
        "header_title": "🧾 PDF417 Identity Generator",
        "header_desc": "Streamlit tool for AAMVA + PNG/SVG vector output",
    },
    "FR": {
        "theme_dark": "🌙 Sombre",
        "theme_light": "☀️ Clair",
        "sidebar_title": "🪪 Générateur d'identité",
        "sidebar_info": "Module de génération actif.",
        "header_title": "🧾 Générateur d'identité PDF417",
        "header_desc": "Outil Streamlit pour AAMVA + export PNG/SVG",
    }
}


# =========================
# GLOBAL UI FIX (THEME SAFE)
# =========================
st.markdown("""
<style>

/* Bouton principal */
div.stButton > button {
    height: 70px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;

    background-color: var(--primary-color);
    color: var(--background-color);
    border: 1px solid var(--primary-color);
}

div.stButton > button:hover {
    filter: brightness(1.1);
}

div.stButton > button:active {
    transform: scale(0.98);
}

/* Texte adaptatif */
.stApp {
    color: var(--text-color);
}

</style>
""", unsafe_allow_html=True)


# =========================
# STYLE CUSTOM DARK/LIGHT
# =========================
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


# =========================
# MAIN APP
# =========================
def main():

    # STATE INIT
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "lang" not in st.session_state:
        st.session_state.lang = "EN"

    t = TEXTS[st.session_state.lang]

    # =========================
    # TOP BAR
    # =========================
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

    # APPLY STYLE
    apply_custom_style(st.session_state.dark_mode)

    # =========================
    # HEADER (fusion main.py)
    # =========================
    st.markdown(
        f"""
        <h1 style='text-align:center;'>
            {t['header_title']}
        </h1>
        <p style='text-align:center; color:gray;'>
            {t['header_desc']}
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================
    # SIDEBAR
    # =========================
    with st.sidebar:
        st.markdown(f"### {t['sidebar_title']}")
        st.info(t["sidebar_info"])

    # =========================
    # CUSTOM HEADER COMPONENT
    # =========================
    header_component()

    # =========================
    # MAIN MODULE
    # =========================
    show_identity_gen(st.session_state.lang)


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    main()
