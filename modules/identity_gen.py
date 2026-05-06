import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# SYSTEM PATH & IMPORTS
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    IIN_US = {"California": "603273", "New York": "603219"}
    IIN_CA = {"Quebec": "604428", "Ontario": "604430"}


# =========================
# MODERN LIQUID GLASS CSS ENGINE
# =========================
def inject_advanced_css():
    """Inject professional Liquid Glass CSS with animations and responsive design"""
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ===== ROOT VARIABLES ===== */
        :root {
            --primary-color: #8122ff;
            --secondary-color: #3a82ff;
            --accent-color: #00e5ff;
            --success-color: #10b981;
            --error-color: #ef4444;
            --warning-color: #f59e0b;
            --bg-primary: #0E1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #0a0e27;
            --text-primary: #fafafa;
            --text-secondary: #b0b8d4;
            --border-color: rgba(255, 255, 255, 0.08);
        }

        /* ===== RESET & BASE ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* ===== MAIN APP ===== */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #161b22 50%, #0E1117 100%) !important;
            background-attachment: fixed;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
        }

        /* ===== HEADER STYLING ===== */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
            font-family: 'Inter', sans-serif !important;
        }

        h1 {
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
            background: linear-gradient(135deg, #fff 0%, #a0a0ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h2 {
            font-size: 1.8rem !important;
            margin-bottom: 1.2rem !important;
        }

        h3 {
            font-size: 1.3rem !important;
            margin-bottom: 1rem !important;
        }

        /* ===== TEXT & PARAGRAPHS ===== */
        p, span, label, li {
            color: var(--text-primary) !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
        }

        /* ===== DIVIDERS ===== */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--border-color), transparent) !important;
            margin: 2rem 0 !important;
        }

        /* ===== CRYSTAL CARD ANIMATION ===== */
        @keyframes cardGlowFade {
            0% {
                transform: translateY(20px);
                opacity: 0;
                box-shadow: 0 0 0 rgba(129, 34, 255, 0);
            }
            100% {
                transform: translateY(0px);
                opacity: 1;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            }
        }

        @keyframes glowPulse {
            0% {
                box-shadow: 0 0 15px rgba(129, 34, 255, 0.25), 0 10px 25px rgba(0, 0, 0, 0.4);
            }
            50% {
                box-shadow: 0 0 25px rgba(129, 34, 255, 0.4), 0 10px 30px rgba(0, 0, 0, 0.5);
            }
            100% {
                box-shadow: 0 0 35px rgba(129, 34, 255, 0.6), 0 15px 40px rgba(0, 0, 0, 0.6);
            }
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* ===== CRYSTAL CARDS ===== */
        .crystal-card {
            background: rgba(255, 255, 255, 0.015);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), inset 0 0 30px rgba(255, 255, 255, 0.01);
            animation: cardGlowFade 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            transition: all 0.3s ease;
        }

        .crystal-card:hover {
            border-color: rgba(129, 34, 255, 0.3);
            box-shadow: 0 25px 50px rgba(129, 34, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        /* ===== INPUT FIELDS ===== */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        input[type="text"],
        input[type="number"],
        select {
            background: rgba(10, 10, 12, 0.6) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            padding: 12px 16px !important;
            font-size: 0.95rem !important;
            font-family: 'Inter', sans-serif !important;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        input[type="text"]:focus,
        input[type="number"]:focus,
        select:focus {
            border-color: var(--secondary-color) !important;
            background: rgba(15, 15, 20, 0.8) !important;
            box-shadow: 0 0 25px rgba(58, 130, 255, 0.2), inset 0 2px 10px rgba(0, 0, 0, 0.5) !important;
            outline: none !important;
        }

        /* ===== SLIDERS (PRO STYLE) ===== */
        div[data-testid="stTickBar"] { display: none !important; }

        div[data-baseweb="slider"] > div:first-child {
            height: 6px !important;
            background: rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }

        div[role="presentation"] > div > div:first-child {
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
            height: 6px !important;
            border-radius: 10px !important;
            box-shadow: 0 0 20px rgba(129, 34, 255, 0.4) !important;
        }

        div[role="slider"] {
            height: 24px !important;
            width: 24px !important;
            background-color: #ffffff !important;
            border: 3px solid var(--primary-color) !important;
            box-shadow: 0 0 30px rgba(129, 34, 255, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
            border-radius: 50% !important;
            transition: all 0.2s ease !important;
        }

        div[role="slider"]:hover {
            transform: scale(1.15) !important;
            box-shadow: 0 0 40px rgba(129, 34, 255, 1) !important;
        }

        /* ===== SELECT SLIDER ===== */
        div[data-testid="stSelectSlider"] {
            padding: 1rem 0 !important;
        }

        /* ===== CHECKBOXES ===== */
        .stCheckbox > label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .stCheckbox > label:hover {
            color: var(--accent-color) !important;
        }

        /* ===== BUTTONS ===== */
        div.stButton > button,
        div.stDownloadButton > button {
            background: linear-gradient(135deg, rgba(129, 34, 255, 0.12), rgba(58, 130, 255, 0.12)) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            color: var(--text-primary) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            font-size: 0.9rem !important;
            font-family: 'Inter', sans-serif !important;
            box-shadow: 0 0 25px rgba(129, 34, 255, 0.35), 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(255, 255, 255, 0.05) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            animation: glowPulse 3s infinite alternate;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            transform: translateY(-4px) scale(1.02);
            border-color: rgba(129, 34, 255, 0.5) !important;
            box-shadow: 0 0 50px rgba(129, 34, 255, 0.9), 0 25px 60px rgba(129, 34, 255, 0.5) !important;
        }

        div.stButton > button:active,
        div.stDownloadButton > button:active {
            transform: scale(0.96);
        }

        div.stButton > button:disabled,
        div.stDownloadButton > button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* ===== FLAG CONTAINER ===== */
        .flag-container {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px 20px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 14px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
            animation: slideIn 0.6s ease;
        }

        .flag-image {
            width: 44px;
            height: 44px;
            border-radius: 8px;
            filter: drop-shadow(0 4px 12px rgba(129, 34, 255, 0.3));
            transition: all 0.3s ease;
        }

        .flag-image:hover {
            transform: scale(1.1) rotate(2deg);
        }

        .jurisdiction-title {
            font-size: 1.2rem;
            font-weight: 600;
            background: linear-gradient(to right, #ffffff, #a0a0ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* ===== ALERTS & INFO ===== */
        div[data-testid="stAlert"] {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid var(--success-color) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            padding: 16px 20px !important;
            animation: fadeIn 0.4s ease;
        }

        /* ===== ERROR ALERTS ===== */
        div[role="alert"] {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid var(--error-color) !important;
            border-radius: 12px !important;
        }

        /* ===== CODE BLOCKS ===== */
        .stCodeBlock {
            background: rgba(10, 10, 12, 0.8) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-color) !important;
        }

        code {
            background: rgba(255, 255, 255, 0.05) !important;
            color: var(--accent-color) !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
        }

        /* ===== EXPANDERS ===== */
        details[data-testid="stExpander"] > summary {
            background: rgba(15, 15, 20, 0.75) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            color: var(--text-primary) !important
