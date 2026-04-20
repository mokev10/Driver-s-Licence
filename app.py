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
            }}
        </style>
    """, unsafe_allow_html=True)


def main():

    # 🔘 Init state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    # 🔘 Top bar
    col1, col2 = st.columns([12, 1])

    # ✅ FIX INDENTATION (IMPORTANT)
    with col2:
        icon_url = (
            "https://img.icons8.com/external-regular-kawalan-studio/28/external-dark-mode-user-interface-regular-kawalan-studio.png"
            if st.session_state.dark_mode
            else "https://img.icons8.com/external-flatart-icons-solid-flatarticons/28/external-sun-nature-flatart-icons-solid-flatarticons-2.png"
        )

        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="{icon_url}" width="28" style="opacity:0.9;">
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Toggle theme", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode

    # 🎨 Apply theme
    apply_custom_style(st.session_state.dark_mode)

    # 📌 Sidebar
    with st.sidebar:
        st.markdown("### 🪪 Identity Gen")
        st.info("Identity generation module is active.")

    # 🧠 Header
    header_component()

    # 📄 Main content
    show_identity_gen()


if __name__ == "__main__":
    main()
