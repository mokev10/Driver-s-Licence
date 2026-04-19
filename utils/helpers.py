import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Modern Transitions and Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stApp {
            animation: fadeIn 0.6s ease-out;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #0A0A0B;
        }
        
        [data-testid="stSidebar"] {
            background-color: #141417;
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        /* Technical Input Styling */
        .stTextInput>div>div>input, .stSelectbox>div>div>div {
            background-color: #1F1F23 !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #E5E7EB !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput>div>div>input:focus {
            border-color: #F59E0B !important;
            box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2) !important;
        }

        /* Modern Button Styling */
        .stButton>button {
            background-color: #F59E0B;
            color: #000;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }
        
        .stButton>button:hover {
            background-color: #D97706;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
            border: none;
        }

        .stButton>button:active {
            transform: translateY(0);
        }

        /* Metric/Card Styling */
        [data-testid="stMetricValue"] {
            color: #F59E0B !important;
        }
        
        .stMarkdown div p {
            color: #9CA3AF;
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
