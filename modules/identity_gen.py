import streamlit as st
import datetime
import io
import sys
import os
import shutil
import traceback
import logging
import base64
import time
import random
import string
import json
import re
from pathlib import Path
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumStudio")

def get_session_state():
    if 'init_timestamp' not in st.session_state:
        st.session_state.init_timestamp = time.time()
    if 'gen_count' not in st.session_state:
        st.session_state.gen_count = 0
    if 'history' not in st.session_state:
        st.session_state.history = []

try:
    from utils.constants import IIN_US, IIN_CA
    from pdf417gen import encode, render_image
    from utils.svg_vectorizer import png_to_svg
except ImportError:
    IIN_US = {
        "Alabama": "603201", "Alaska": "603202", "Arizona": "603203", "Arkansas": "603204",
        "California": "603273", "Colorado": "603206", "Connecticut": "603207", "Delaware": "603208",
        "Florida": "603211", "Georgia": "603212", "Hawaii": "603213", "Idaho": "603214",
        "Illinois": "603215", "Indiana": "603216", "Iowa": "603217", "Kansas": "603218",
        "Kentucky": "603219", "Louisiana": "603220", "Maine": "603221", "Maryland": "603222",
        "Massachusetts": "603223", "Michigan": "603224", "Minnesota": "603225", "Mississippi": "603226",
        "Missouri": "603227", "Montana": "603228", "Nebraska": "603229", "Nevada": "603230",
        "New Hampshire": "603231", "New Jersey": "603232", "New Mexico": "603233", "New York": "603219",
        "North Carolina": "603235", "North Dakota": "603236", "Ohio": "603237", "Oklahoma": "603238",
        "Oregon": "603239", "Pennsylvania": "603240", "Rhode Island": "603241", "South Carolina": "603242",
        "South Dakota": "603243", "Tennessee": "603244", "Texas": "603245", "Utah": "603246",
        "Vermont": "603247", "Virginia": "603248", "Washington": "603249", "West Virginia": "603250",
        "Wisconsin": "603251", "Wyoming": "603252"
    }
    IIN_CA = {
        "Alberta": "604432", "British Columbia": "604433", "Manitoba": "604434",
        "New Brunswick": "604435", "Newfoundland": "604436", "Nova Scotia": "604437",
        "Ontario": "604430", "Prince Edward Island": "604439", "Quebec": "604428", "Saskatchewan": "604441"
    }

class QuantumPDF417:
    def __init__(self, payload, columns=12, security_level=2):
        self.payload = payload
        self.columns = columns
        self.security_level = security_level
        self.codes = None
        self.image = None

    def generate_matrix(self):
        self.codes = encode(self.payload, columns=self.columns, security_level=self.security_level)
        return self.codes

    def render(self, scale=5, ratio=3, padding=20):
        self.image = render_image(self.codes, scale=scale, ratio=ratio, padding=padding)
        return self.image

    def get_svg(self, potrace_path):
        if not self.image:
            return None
        buf = io.BytesIO()
        self.image.save(buf, format="PNG")
        return png_to_svg(buf.getvalue(), potrace_path=potrace_path)

def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #020204;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        .crystal-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 30px;
            padding: 40px;
            margin-bottom: 35px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.7);
        }

        .purple-label {
            font-family: 'JetBrains Mono', monospace;
            color: #9d50ff;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-bottom: 12px;
            margin-top: 20px;
            display: block;
        }

        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
            color: #ffffff !important;
            padding: 12px 20px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #9d50ff !important;
            box-shadow: 0 0 15px rgba(157, 80, 255, 0.3) !important;
        }

        .stSelectbox > div > div {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
        }

        div[data-baseweb="slider"] > div:first-child {
            height: 12px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 6px !important;
        }

        div[role="presentation"] > div > div:first-child {
            background: linear-gradient(90deg, #9d50ff, #3a82ff) !important;
            height: 12px !important;
        }

        div[role="slider"] {
            height: 24px !important;
            width: 24px !important;
            background-color: #ffffff !important;
            border: 4px solid #9d50ff !important;
        }

        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #9d50ff 0%, #3a82ff 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 18px 0 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            margin-top: 20px;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(157, 80, 255, 0.4);
        }

        .stCodeBlock {
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        .sidebar-info {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.4);
            margin-top: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def validate_aamva_data(data_dict):
    errors = []
    if not re.match(r"^\d{8}$", data_dict['dbb']):
        errors.append("DOB doit être au format YYYYMMDD")
    if len(data_dict['dcs']) < 1:
        errors.append("Le nom est obligatoire")
    return errors

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def show_identity_gen(lang="FR"):
    get_session_state()
    inject_styles()
    
    st.markdown('<h1 style="text-align: center; font-weight: 300; letter-spacing: -1px;">STUDIO <span style="font-weight: 600; color: #9d50ff;">QUANTUM</span> AAMVA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.5); margin-bottom: 50px;">Générateur de Data-Matrix Haute Fidélité pour Systèmes OCR</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="purple-label">System Status</div>', unsafe_allow_html=True)
        st.success("Quantum Engine: Online")
        st.info(f"Session Active: {datetime.datetime.now().strftime('%H:%M')}")
        
        st.divider()
        st.markdown('<div class="purple-label">Module Configuration</div>', unsafe_allow_html=True)
        country = st.selectbox("Source Nation", ["Canada", "United States"], help="Définit la norme IIN")
        
        if country == "United States":
            region = st.selectbox("State / Territory", sorted(IIN_US.keys()))
            iin = IIN_US[region]
        else:
            region = st.selectbox("Province / Territory", sorted(IIN_CA.keys()))
            iin = IIN_CA[region]
            
        st.divider()
        st.markdown('<div class="purple-label">Output Parameters</div>', unsafe_allow_html=True)
        res_dpi = st.select_slider("Density (DPI)", options=[300, 600, 1200, 2400], value=600)
        m_cols = st.slider("Matrix Columns", 4, 30, 12)
        m_sec = st.slider("Error Correction Level", 1, 5, 2)
        q_padding = st.slider("Quiet Zone (px)", 0, 100, 10)
        
        st.divider()
        use_escape = st.checkbox("Utilisez \\n pour ENTRÉE", value=True)
        auto_gen_id = st.checkbox("Générer ID Aléatoire", value=False)
        
        st.markdown('<div class="sidebar-info">v2.4.0-STABLE<br/>Quantum Encryption Ready</div>', unsafe_allow_html=True)

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.markdown('<div class="purple-label">Identity Metadata Matrix</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="purple-label">DCS - Family Name</div>', unsafe_allow_html=True)
        f_dcs = st.text_input("DCS", "NICOLAS", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAC - First Name</div>', unsafe_allow_html=True)
        f_dac = st.text_input("DAC", "JEAN", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAG - Address Line</div>', unsafe_allow_html=True)
        f_dag = st.text_input("DAG", "1560 SHERBROOKE ST E", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAI - City</div>', unsafe_allow_html=True)
        f_dai = st.text_input("DAI", "MONTREAL", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="purple-label">DAQ - Document Number</div>', unsafe_allow_html=True)
        default_id = f"D{generate_random_string(7)}" if auto_gen_id else "N2420-941208-96"
        f_daq = st.text_input("DAQ", default_id, label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DBB - Date of Birth</div>', unsafe_allow_html=True)
        f_dbb = st.text_input("DBB", "19941208", label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DBC - Sex</div>', unsafe_allow_html=True)
        f_dbc = st.selectbox("DBC", ["1", "2", "3"], label_visibility="collapsed")
        
        st.markdown('<div class="purple-label">DAK - Postal Code</div>', unsafe_allow_html=True)
        f_dak = st.text_input("DAK", "H2L 4M1", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.markdown('<div class="purple-label">Secondary Attributes</div>', unsafe_allow_html=True)
    
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown('<div class="purple-label">DAU - Height</div>', unsafe_allow_html=True)
        f_dau = st.text_input("DAU", "180 cm", label_visibility="collapsed")
    with a2:
        st.markdown('<div class="purple-label">DAY - Eyes</div>', unsafe_allow_html=True)
        f_day = st.text_input("DAY", "BRUN", label_visibility="collapsed")
    with a3:
        st.markdown('<div class="purple-label">DAZ - Hair</div>', unsafe_allow_html=True)
        f_daz = st.text_input("DAZ", "NOIR", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Initialiser la Séquence de Synthèse"):
        data_bundle = {
            'dcs': f_dcs, 'dac': f_dac, 'dag': f_dag, 'dai': f_dai,
            'daq': f_daq, 'dbb': f_dbb, 'dbc': f_dbc, 'dak': f_dak
        }
        
        validation_errors = validate_aamva_data(data_bundle)
        if validation_errors:
            for err in validation_errors:
                st.error(f"Validation Fault: {err}")
            return

        try:
            with st.spinner("Quantum Rendering in progress..."):
                st_code = region[:2].upper() if country == "United States" else "QC"
                
                header = f"@\nANSI {iin}050102DL00410287ZO02900045DL"
                content = (
                    f"DCS{f_dcs.upper()}\n"
                    f"DAC{f_dac.upper()}\n"
                    f"DAD{generate_random_string(3)}\n"
                    f"DAG{f_dag.upper()}\n"
                    f"DAI{f_dai.upper()}\n"
                    f"DAJ{st_code}\n"
                    f"DAK{f_dak.replace(' ', '').upper()}\n"
                    f"DAQ{f_daq.upper()}\n"
                    f"DBB{f_dbb}\n"
                    f"DBC{f_dbc}\n"
                    f"DBD20230510\n"
                    f"DBA20310509\n"
                    f"DAU{f_dau}\n"
                    f"DAY{f_day}\n"
                    f"DAZ{f_daz}"
                )
                
                full_payload = f"{header}\n{content}"
                
                res_col_a, res_col_b = st.columns([1, 1.3])
                
                with res_col_a:
                    st.markdown('<div class="purple-label">Raw Payload Analysis</div>', unsafe_allow_html=True)
                    display_payload = full_payload.replace("\n", "\\n") if use_escape else full_payload
                    st.code(display_payload, language="text")
                    
                    st.markdown('<div class="purple-label">Data Statistics</div>', unsafe_allow_html=True)
                    stats = {
                        "Bytes": len(full_payload),
                        "Lines": len(full_payload.split('\n')),
                        "Jurisdiction": region,
                        "IIN": iin
                    }
                    st.json(stats)

                with res_col_b:
                    st.markdown('<div class="purple-label">Digital Twin Preview</div>', unsafe_allow_html=True)
                    
                    engine = QuantumPDF417(full_payload, columns=m_cols, security_level=m_sec)
                    engine.generate_matrix()
                    
                    render_scale = max(1, int(res_dpi / 90))
                    img_output = engine.render(scale=render_scale, padding=q_padding)
                    
                    png_buf = io.BytesIO()
                    img_output.save(png_buf, format="PNG")
                    
                    st.image(png_buf.getvalue(), use_container_width=True, caption=f"PDF417 Matrix - {res_dpi} DPI")
                    
                    c_down1, c_down2 = st.columns(2)
                    with c_down1:
                        st.download_button(
                            label="Download PNG",
                            data=png_buf.getvalue(),
                            file_name=f"quantum_id_{f_daq}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    with c_down2:
                        path_potrace = shutil.which("potrace")
                        if path_potrace:
                            svg_data = engine.get_svg(path_potrace)
                            if svg_data:
                                st.download_button(
                                    label="Download SVG",
                                    data=svg_data,
                                    file_name=f"quantum_id_{f_daq}.svg",
                                    mime="image/svg+xml",
                                    use_container_width=True
                                )
                    
                    if path_potrace:
                        with st.expander("Inspection Vectorielle SVG (Full)"):
                            st.markdown(
                                f'<div style="background:white; border-radius:10px; padding:20px; display:flex; justify-content:center;">{svg_data}</div>', 
                                unsafe_allow_html=True
                            )
                            st.markdown('<div class="purple-label">SVG XML Source</div>', unsafe_allow_html=True)
                            st.code(svg_data[:1000] + "...", language="xml")

                st.session_state.gen_count += 1
                st.session_state.history.append({
                    "id": f_daq,
                    "ts": datetime.datetime.now().isoformat(),
                    "region": region
                })

        except Exception as e:
            st.error(f"Critical Render Fault: {str(e)}")
            with st.expander("Traceback Stack"):
                st.code(traceback.format_exc())

    st.divider()
    if st.session_state.history:
        with st.expander("Session History Logs"):
            st.table(st.session_state.history[-5:])

    st.markdown(
        f"""
        <div style="text-align: center; color: rgba(255,255,255,0.2); font-size: 0.7rem; margin-top: 40px;">
            Total Generations this session: {st.session_state.gen_count} | 
            Buffer Load: {round(time.time() - st.session_state.init_timestamp, 2)}s
        </div>
        """, 
        unsafe_allow_html=True
    )

# ==============================================================================
# SECTEUR DE TESTS UNITAIRES (INTERNAL)
# ==============================================================================
def run_internal_tests():
    test_data = {'dbb': '19900101', 'dcs': 'TEST'}
    assert len(validate_aamva_data(test_data)) == 0
    logger.info("Unit Test: Validation Logic Passed")

if __name__ == "__main__":
    if os.environ.get("DEBUG_MODE") == "1":
        run_internal_tests()
    show_identity_gen()

# ==============================================================================
# END OF IDENTITY_GEN MODULE - PROTOTYPE 400L
# ==============================================================================
