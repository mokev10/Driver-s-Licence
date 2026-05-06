import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback

# =========================
# IMPORTS SYSTÈME
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
# CSS MINIMALISTE PRO
# =========================
def apply_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        /* VARIABLES */
        :root {
            --primary: #8122ff;
            --secondary: #3a82ff;
            --accent: #00e5ff;
            --success: #10b981;
            --error: #ef4444;
            --bg: #0E1117;
            --card: #161b22;
            --text: #FAFAFA;
            --text-light: #b0b8d4;
            --border: rgba(255,255,255,0.08);
        }
        
        .stApp { background: var(--bg) !important; }
        
        /* TYPOGRAPHY */
        h1, h2, h3 {
            color: var(--text) !important;
            font-weight: 700 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.2rem !important; }
        
        /* CARDS */
        .crystal-card {
            background: rgba(255,255,255,0.01);
            backdrop-filter: blur(25px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* INPUTS */
        input, select, textarea {
            background: rgba(10,10,12,0.6) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text) !important;
            padding: 12px 16px !important;
            transition: all 0.3s ease !important;
        }
        
        input:focus, select:focus {
            border-color: var(--secondary) !important;
            box-shadow: 0 0 20px rgba(58,130,255,0.2) !important;
        }
        
        /* SLIDERS */
        div[data-baseweb="slider"] > div { height: 8px !important; background: var(--border) !important; border-radius: 10px !important; }
        div[role="presentation"] > div > div:first-child { background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important; height: 8px !important; box-shadow: 0 0 15px rgba(129,34,255,0.4) !important; }
        div[role="slider"] { background: white !important; border: 4px solid var(--primary) !important; height: 22px !important; width: 22px !important; box-shadow: 0 0 25px rgba(129,34,255,0.8) !important; }
        
        /* BUTTONS */
        div.stButton > button, div.stDownloadButton > button {
            background: linear-gradient(135deg, rgba(129,34,255,0.1), rgba(58,130,255,0.1)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: var(--text) !important;
            border-radius: 10px !important;
            padding: 12px 28px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            box-shadow: 0 0 20px rgba(129,34,255,0.3) !important;
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
        }
        
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 0 40px rgba(129,34,255,0.7) !important;
        }
        
        /* FLAG */
        .flag-box {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px;
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        
        .flag-box img { width: 40px; height: auto; border-radius: 6px; filter: drop-shadow(0 4px 10px rgba(129,34,255,0.3)); }
        
        .flag-title { font-size: 1.1rem; font-weight: 600; background: linear-gradient(to right, white, #a0a0ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        
        /* EXPANDERS */
        details > summary {
            background: rgba(15,15,20,0.7) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            color: var(--text) !important;
            font-weight: 600 !important;
            cursor: pointer !important;
        }
        
        details > div { background: rgba(10,10,15,0.8) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 12px !important; }
        
        /* ALERTS */
        div[data-testid="stAlert"] { background: rgba(16,185,129,0.1) !important; border: 1px solid var(--success) !important; border-radius: 10px !important; }
        
        /* BADGE */
        .engine-tag { color: var(--accent); background: rgba(0,229,255,0.1); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(0,229,255,0.3); font-size: 0.85rem; display: inline-block; font-weight: 600; }
        
    </style>
    """, unsafe_allow_html=True)


# =========================
# MODULE PRINCIPAL
# =========================
def show_identity_gen(lang="EN"):
    
    # TRADUCTIONS
    DICT = {
        "EN": {
            "title": "AAMVA PDF417 Studio",
            "subtitle": "Quantum Identity Matrix Engine",
            "step1": "Jurisdiction Analysis",
            "country": "Source Nation",
            "state": "Regional State",
            "prov": "Regional Province",
            "step2": "Identity Parameters",
            "step3": "Optical Configuration",
            "gen": "Generate PDF417",
            "success": "Matrix compiled successfully",
            "raw": "AAMVA Raw Output",
            "preview": "Barcode Preview",
            "dpi": "Resolution (DPI)",
            "density": "Matrix Density",
            "padding": "Quiet Zone",
            "escape": "Format with Escape Sequences",
            "engine": "ENGINE READY",
            "png": "Export PNG",
            "svg": "Export SVG",
            "inspect": "Vector Inspection"
        },
        "FR": {
            "title": "Studio AAMVA PDF417",
            "subtitle": "Moteur de Matrice d'Identité Quantique",
            "step1": "Analyse de Juridiction",
            "country": "Nation Source",
            "state": "État Régional",
            "prov": "Province Régionale",
            "step2": "Paramètres d'Identité",
            "step3": "Configuration Optique",
            "gen": "Générer PDF417",
            "success": "Matrice compilée avec succès",
            "raw": "Sortie Brute AAMVA",
            "preview": "Aperçu du Code-barres",
            "dpi": "Résolution (DPI)",
            "density": "Densité Matrix",
            "padding": "Zone Silencieuse",
            "escape": "Formater avec Échappement",
            "engine": "MOTEUR PRÊT",
            "png": "Exporter PNG",
            "svg": "Exporter SVG",
            "inspect": "Inspection Vectorielle"
        }
    }
    
    ui = DICT.get(lang, DICT["EN"])
    apply_css()
    
    # HEADER
    st.title(ui["title"])
    st.caption(ui["subtitle"])
    st.divider()
    
    # STEP 1: JURISDICTION
    with st.container():
        st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox(ui["country"], ["Canada", "United States"])
            flag_url = "https://cdn-icons-png.flaticon.com/512/323/323310.png" if country == "United States" else "https://cdn-icons-png.flaticon.com/512/323/323277.png"
            
            st.markdown(f"""
            <div class="flag-box">
                <img src="{flag_url}">
                <span class="flag-title">{ui['step1']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if country == "United States":
                region = st.selectbox(ui["state"], sorted(IIN_US.keys()))
                iin = IIN_US[region]
            else:
                prov_list = sorted(IIN_CA.keys())
                idx = prov_list.index("Quebec") if "Quebec" in prov_list else 0
                region = st.selectbox(ui["prov"], prov_list, index=idx)
                iin = IIN_CA[region]
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # STEP 2: IDENTITY DATA
    with st.container():
        st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
        st.subheader(ui["step2"])
        
        col1, col2 = st.columns(2)
        with col1:
            iso = "CAN" if country == "Canada" else "USA"
            dcg = st.text_input("DCG - ISO Country", iso)
            dac = st.text_input("DAC - Given Names", "JEAN")
            dcs = st.text_input("DCS - Surname", "NICOLAS")
            dbb = st.text_input("DBB - DOB (YYYYMMDD)", "19941208")
            daq = st.text_input("DAQ - License ID", "N2420-941208-96")
            dag = st.text_input("DAG - Street", "1560 SHERBROOKE ST E")
        
        with col2:
            dai = st.text_input("DAI - City", "MONTREAL")
            dak = st.text_input("DAK - Postal", "H2L 4M1")
            dbd = st.text_input("DBD - Issue (YYYYMMDD)", "20230510")
            dba = st.text_input("DBA - Expiry (YYYYMMDD)", "20310509")
            dbc = st.selectbox("DBC - Gender", ["1", "2"], index=0)
            dcf = st.text_input("DCF - Audit", "PEJQ04N96")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # STEP 3: RENDER OPTIONS
    with st.container():
        st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
        st.subheader(ui["step3"])
        
        col1, col2 = st.columns(2)
        with col1:
            dpi = st.select_slider(ui["dpi"], options=[72, 150, 300, 600, 1200], value=600)
            scale = max(1, int(dpi / 40))
        
        with col2:
            density = st.slider(ui["density"], 1, 30, 10)
            padding = st.slider(ui["padding"], 0, 60, 5)
        
        escape = st.checkbox(ui["escape"], value=True)
        st.markdown(f'<div class="engine-tag">{ui["engine"]}: {dpi} DPI | SCALE {scale}X</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # GENERATE
    if st.button(ui["gen"], use_container_width=True):
        try:
            # BUILD AAMVA STRING
            reg_code = "QC" if region == "Quebec" else region[:2].upper()
            header = f"ANSI {iin}050102DL00410287ZO02900045DL"
            raw = f"@\n{header}\nDCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\nDAG{dag}\nDAI{dai}\nDAJ{reg_code}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
            
            st.success(ui["success"])
            st.divider()
            
            # OUTPUT
            col1, col2 = st.columns([1, 1.4])
            
            with col1:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["raw"])
                display = raw.replace("\n", "\\n") if escape else raw
                st.code(display, language="text")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
                st.subheader(ui["preview"])
                
                # RENDER PDF417
                codes = encode(raw, columns=density)
                img = render_image(codes, scale=scale, padding=padding)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG", dpi=(dpi, dpi))
                png_data = buf.getvalue()
                
                st.image(png_data, use_column_width=True)
                
                # DOWNLOAD BUTTONS
                btn1, btn2 = st.columns(2)
                with btn1:
                    st.download_button(
                        label=f"{ui['png']} ({dpi} DPI
