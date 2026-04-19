import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0A0A0B;
        }
        [data-testid="stSidebar"] {
            background-color: #141417;
        }
        .stButton>button {
            background-color: #F59E0B;
            color: black;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #D97706;
            transform: scale(1.02);
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

def header_component():
    st.markdown("""
        <div style="background-color: #141417; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 25px;">
            <h1 style="color: white; margin: 0; font-size: 24px;">Streamlit <span style="color: #F59E0B;">Modular Hub</span></h1>
            <p style="color: #6B7280; font-size: 14px; margin-top: 5px;">Centralized orchestration for Python modules</p>
        </div>
    """, unsafe_allow_html=True)
