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
from utils.helpers import apply_custom_style, header_component
from modules.identity_gen import show_identity_gen

# Apply custom Elegant Dark styling
apply_custom_style()

def main():
    # Sidebar (simplifiée)
    with st.sidebar:
        st.markdown("### 🪪 Identity Gen")
        st.info("Identity generation module is active.")

    # Header
    header_component()

    # Main content (unique module)
    show_identity_gen()

if __name__ == "__main__":
    main()
