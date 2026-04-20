import streamlit as st
import os

st.set_page_config(
    page_title="AI Generator PDF417",
    page_icon="https://img.icons8.com/external-inipagistudio-mixed-inipagistudio/24/external-ai-web-programmer-inipagistudio-mixed-inipagistudio.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.helpers import header_component
from modules.identity_gen import show_identity_gen


# 🌍 Traductions globales
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


def apply_custom_style(dark_mode=True):
    if dark_mode:
        bg = "#0E1117"
        text = "#FAFAFA"
        card = "#161B22"
    else:
        bg = "#FFFFFF"
        text = "#000000"
        card = "#F5F5F5"

    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {bg};
                color: {text};
            }}

            section[data-testid="stSidebar"] {{
                background-color: {card};
            }}

            div[data-testid="stButton"] > button {{
                border-radius: 8px;
                width: 100%;
            }}
        </style>
    """, unsafe_allow_html=True)


def main():

    # 🔘 Init states
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "lang" not in st.session_state:
        st.session_state.lang = "EN"

    t = TEXTS[st.session_state.lang]

    # 🔘 Top bar (Theme + Language)
    col1, col2, col3 = st.columns([10, 1, 1])

    # 🌙 Theme button
    with col2:
        if st.button(
            t["theme_dark"] if st.session_state.dark_mode else t["theme_light"],
            key="theme_toggle"
        ):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # 🌍 Language selector + ICON
    with col3:

        lang = st.selectbox(
            "",
            ["EN", "FR"],
            index=0 if st.session_state.lang == "EN" else 1,
            key="lang_select"
        )

        if lang != st.session_state.lang:
            st.session_state.lang = lang
            st.rerun()

        # ✅ ICON fiable (UTILISE st.image → FIX BUG)
        icon_url = (
            "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
            if st.session_state.lang == "EN"
            else "https://img.icons8.com/external-justicon-flat-justicon/64/external-france-countrys-flags-justicon-flat-justicon.png"
        )

        st.image(icon_url, width=28)

    # 🎨 Apply theme
    apply_custom_style(st.session_state.dark_mode)

    # 📌 Sidebar
    with st.sidebar:
        st.markdown(f"### {t['sidebar_title']}")
        st.info(t["sidebar_info"])

    # 🧠 Header
    header_component()

    # 📄 Main content
    show_identity_gen(st.session_state.lang)


if __name__ == "__main__":
    main()
