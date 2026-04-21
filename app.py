import streamlit as st

from modules.identity_gen import show_identity_gen
from utils.helpers import header_component


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
    },
    "FR": {
        "theme_dark": "🌙 Sombre",
        "theme_light": "☀️ Clair",
        "sidebar_title": "🪪 Générateur d'identité",
        "sidebar_info": "Module de génération actif.",
    }
}


# =========================
# STYLE
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

    # TOP BAR
    col1, col2, col3 = st.columns([10, 1, 1])

    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    with col3:
        lang = st.selectbox("", ["EN", "FR"], label_visibility="collapsed")
        st.session_state.lang = lang

    # APPLY STYLE
    apply_custom_style(st.session_state.dark_mode)

    # SIDEBAR
    with st.sidebar:
        st.markdown(f"### {t['sidebar_title']}")
        st.info(t["sidebar_info"])

    # HEADER
    header_component()

    # MAIN MODULE
    show_identity_gen(st.session_state.lang)


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    main()
