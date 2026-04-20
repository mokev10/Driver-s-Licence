import streamlit as st
import os

# Set page config
st.set_page_config(
    page_title="Generator PDF417",
    page_icon="https://img.icons8.com/external-inipagistudio-mixed-inipagistudio/24/external-ai-web-programmer-inipagistudio-mixed-inipagistudio.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import local modules
from utils.helpers import apply_custom_style, header_component
from modules.data_analysis import show_data_analysis
from modules.identity_gen import show_identity_gen

# Apply custom Elegant Dark styling
apply_custom_style()

def main():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        app_mode = st.radio(
            "Select Dashboard Module",
            ["🏠 Hub Overview", "📊 Data Analysis", "🪪 Identity Gen", "⚙️ Settings"],
            index=2
        )
        
        st.divider()
        st.markdown("### 🛠️ System Info")
        st.info("Environment: Production\nKernel: V8 Optimized")

    # Header
    header_component()

    # Content Logic
    if app_mode == "🏠 Hub Overview":
        st.title("Welcome to the Modular Hub")
        st.write("This central platform orchestrates multiple Python-based services. Select a module from the sidebar to begin.")
        
        # Dashboard Grid (Summary Cards)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Active Modules", value="3", delta="1")
        with col2:
            st.metric(label="System Status", value="STABLE", delta="0.00042")
        with col3:
            st.metric(label="Uptime", value="99.9%", delta="0.1%")
            
        st.markdown("---")
        st.subheader("Recent Activity")
        st.write("- Identity Module updated to standards V20")
        st.write("- Data Analysis pipeline optimized for big data")

    elif app_mode == "📊 Data Analysis":
        show_data_analysis()
        
    elif app_mode == "🪪 Identity Gen":
        show_identity_gen()
        
    elif app_mode == "⚙️ Settings":
        st.header("⚙️ Global Settings")
        st.write("Manage environment variables and global configurations.")
        theme = st.toggle("Enable Performance Optimization", value=True)
        debug_mode = st.toggle("Debug Log Stream", value=False)
        
        if st.button("Save Changes"):
            st.success("Configurations saved locally.")

if __name__ == "__main__":
    main()
