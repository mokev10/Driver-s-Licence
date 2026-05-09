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
# MULTILINGUAL TEXTS
# =========================
TEXTS = {
    "EN": {
        "theme_dark": "🌙 Dark",
        "theme_light": "☀️ Light",
        "sidebar_title": "🪪 Identity Generator",
        "sidebar_info": "Generate realistic digital identities with AI",
        "settings": "⚙️ Settings",
    },
    "FR": {
        "theme_dark": "🌙 Sombre",
        "theme_light": "☀️ Clair",
        "sidebar_title": "🪪 Générateur d'Identité",
        "sidebar_info": "Générez des identités numériques réalistes avec l'IA",
        "settings": "⚙️ Paramètres",
    }
}

# =========================
# COLOR PALETTES
# =========================
COLORS = {
    "dark": {
        "bg_primary": "#0A0E27",
        "bg_secondary": "#1a1f3a",
        "bg_tertiary": "#242a45",
        "text_primary": "#ffffff",
        "text_secondary": "#b0b8d4",
        "accent_primary": "#6366f1",
        "accent_secondary": "#a855f7",
        "accent_tertiary": "#ec4899",
        "border": "#2d3748",
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b",
    },
    "light": {
        "bg_primary": "#f9fafb",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#f3f4f6",
        "text_primary": "#111827",
        "text_secondary": "#6b7280",
        "accent_primary": "#6366f1",
        "accent_secondary": "#a855f7",
        "accent_tertiary": "#ec4899",
        "border": "#e5e7eb",
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b",
    }
}


# =========================
# MODERN CSS STYLING
# =========================
def apply_modern_css(dark_mode=True):
    """Apply modern, professional CSS styling based on theme"""
    
    colors = COLORS["dark"] if dark_mode else COLORS["light"]
    
    st.markdown(f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        /* ROOT VARIABLES */
        :root {{
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --accent-primary: {colors['accent_primary']};
            --accent-secondary: {colors['accent_secondary']};
            --accent-tertiary: {colors['accent_tertiary']};
            --border: {colors['border']};
            --success: {colors['success']};
            --error: {colors['error']};
            --warning: {colors['warning']};
        }}

        /* MAIN APP BACKGROUND */
        .stApp {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(135deg, {colors['bg_secondary']} 0%, {colors['bg_tertiary']} 100%) !important;
            border-right: 1px solid var(--border) !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}

        /* MAIN CONTENT AREA */
        .main {{
            background-color: var(--bg-primary) !important;
        }}

        /* TEXT STYLING */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }}

        h1 {{ font-size: 2.5rem !important; margin-bottom: 1.5rem !important; }}
        h2 {{ font-size: 2rem !important; margin-bottom: 1.2rem !important; }}
        h3 {{ font-size: 1.5rem !important; margin-bottom: 1rem !important; }}

        p, span, label {{
            color: var(--text-primary) !important;
        }}

        /* CARDS & CONTAINERS */
        .stCard, div[data-testid="stExpander"] {{
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stCard:hover {{
            border-color: var(--accent-primary) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15) !important;
            transform: translateY(-2px) !important;
        }}

        /* INFO BOX */
        div[data-testid="stAlert"] {{
            background-color: rgba(99, 102, 241, 0.1) !important;
            border: 1px solid var(--accent-primary) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            padding: 1rem 1.5rem !important;
        }}

        /* BUTTONS - PRIMARY */
        div.stButton > button {{
            background: linear-gradient(135deg, {colors['accent_primary']} 0%, {colors['accent_secondary']} 100%) !important;
            color: white !important;
            border: none !important;
            padding: 12px 32px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }}

        div.stButton > button:hover {{
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5) !important;
            transform: translateY(-2px) !important;
        }}

        div.stButton > button:active {{
            transform: translateY(0) !important;
        }}

        /* INPUTS & TEXTAREAS */
        input, textarea, select {{
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            transition: all 0.2s ease !important;
            font-size: 0.95rem !important;
        }}

        input:focus, textarea:focus, select:focus {{
            background-color: var(--bg-secondary) !important;
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            outline: none !important;
        }}

        /* SELECTBOX */
        div[data-testid="stSelectbox"] {{
            margin-bottom: 1.5rem !important;
        }}

        /* TABS */
        button[data-baseweb="tab"] {{
            color: var(--text-secondary) !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.3s ease !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: var(--accent-primary) !important;
            border-bottom-color: var(--accent-primary) !important;
        }}

        /* HEADER AREA - CUSTOM */
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--border);
        }}

        .settings-container {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        /* THEME & LANGUAGE BUTTONS */
        .theme-toggle, .lang-toggle {{
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
            padding: 8px 14px !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            font-weight: 600 !important;
        }}

        .theme-toggle:hover, .lang-toggle:hover {{
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.2) !important;
            transform: translateY(-1px) !important;
        }}

        /* SIDEBAR TITLE */
        .sidebar-title {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            margin-bottom: 1rem !important;
        }}

        /* SPACING UTILITIES */
        .spacing-small {{ margin-bottom: 0.5rem !important; }}
        .spacing-medium {{ margin-bottom: 1rem !important; }}
        .spacing-large {{ margin-bottom: 2rem !important; }}

        /* RESPONSIVENESS */
        @media (max-width: 768px) {{
            .settings-container {{
                flex-direction: column;
                gap: 0.5rem;
            }}

            h1 {{ font-size: 1.8rem !important; }}
            h2 {{ font-size: 1.4rem !important; }}
        }}

        /* SCROLLBAR STYLING */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--bg-tertiary);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--accent-primary);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-secondary);
        }}

        /* TOOLTIP ACCESSIBILITY */
        div[data-testid="stTooltipContent"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid var(--accent-primary) !important;
            border-radius: 4px !important;
        }}

        div[data-testid="stTooltipContent"] p {{
            color: #000000 !important;
        }}

    </style>
    """, unsafe_allow_html=True)


def render_header(lang, dark_mode):
    """Render modern header with theme/language controls"""
    t = TEXTS[lang]
    
    col1, col2, col3 = st.columns([8, 1, 1])
    
    with col1:
        st.markdown(f"<h1 style='margin: 0;'>✨ AI Generator PDF417</h1>", unsafe_allow_html=True)
    
    with col2:
        theme_tip = t["theme_light"] if dark_mode else t["theme_dark"]
        if st.button("🌙" if dark_mode else "☀️", key="theme_toggle", use_container_width=True, help=theme_tip):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    with col3:
        lang_val = st.selectbox(
            "",
            ["EN", "FR"],
            index=0 if lang == "EN" else 1,
            label_visibility="collapsed",
            key="lang_select",
        )
        
        if lang_val != lang:
            st.session_state.lang = lang_val
            st.rerun()
    
    st.markdown("---")


def render_sidebar(lang):
    """Render enhanced sidebar"""
    t = TEXTS[lang]
    
    with st.sidebar:
        st.markdown(f"<p class='sidebar-title'>{t['sidebar_title']}</p>", unsafe_allow_html=True)
        st.info(t["sidebar_info"])
        
        st.markdown("---")
        st.markdown(f"### {t['settings']}")
        
        with st.expander("🎨 Appearance", expanded=False):
            st.caption("Customize your visual experience")
            st.write("")


def main():
    """Main application entry point"""
    
    # Initialize session state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "lang" not in st.session_state:
        st.session_state.lang = "EN"

    # Apply theme
    apply_modern_css(st.session_state.dark_mode)
    
    # Render header
    render_header(st.session_state.lang, st.session_state.dark_mode)
    
    # Render sidebar
    render_sidebar(st.session_state.lang)
    
    # Load and display header component
    header_component()
    
    # Load and display identity generation module
    show_identity_gen(st.session_state.lang)


if __name__ == "__main__":
    main()
