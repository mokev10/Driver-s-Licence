import streamlit as st

from modules.identity_gen import show_identity_gen


# =========================
# CONFIG PAGE
# =========================

st.set_page_config(
    page_title="AI Generator PDF417",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================
# STATE INIT
# =========================

if "lang" not in st.session_state:
    st.session_state.lang = "EN"


# =========================
# LANG SWITCH UI
# =========================

col1, col2 = st.columns([10, 2])

with col2:
    lang = st.selectbox(
        "Language",
        ["EN", "FR"],
        index=0 if st.session_state.lang == "EN" else 1
    )

    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()


# =========================
# HEADER
# =========================

st.markdown(
    """
    <h1 style='text-align:center;'>
        🧾 PDF417 Identity Generator
    </h1>
    <p style='text-align:center; color:gray;'>
        Streamlit tool for AAMVA + PNG/SVG vector output
    </p>
    """,
    unsafe_allow_html=True
)


st.divider()


# =========================
# MAIN MODULE
# =========================

show_identity_gen(st.session_state.lang)
