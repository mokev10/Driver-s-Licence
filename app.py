import streamlit as st
import os

# Set page config
st.set_page_config(
    page_title="AI Generator PDF417",
    page_icon="https://img.icons8.com/external-inipagistudio-mixed-inipagistudio/24/external-ai-web-programmer-inipagistudio-mixed-inipagistudio.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import local modules
from utils.helpers import header_component
from modules.identity_gen import show_identity_gen


# 🎨 Dynamic theme function
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

    # 🔘 Top bar with toggle (RIGHT aligned)
    col1, col2 = st.columns([12, 1])

    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️"):
            st.session_state.dark_mode = not st.session_state.dark_mode

    # 🎨 Apply theme AFTER toggle
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
