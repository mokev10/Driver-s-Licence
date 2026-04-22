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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - QUANTUM_ENGINE - %(levelname)s - %(message)s'
)
logger = logging.getLogger("QuantumStudioAAMVA")

def initialize_session_state():
    if 'init_timestamp' not in st.session_state:
        st.session_state.init_timestamp = time.time()
    if 'gen_count' not in st.session_state:
        st.session_state.gen_count = 0
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'ui_theme' not in st.session_state:
        st.session_state.ui_theme = "quantum_dark"
    if 'render_mode' not in st.session_state:
        st.session_state.render_mode = "high_fidelity"

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

AAMVA_FIELD_MAP = {
    "DCA": "Jurisdiction-specific vehicle class",
    "DCB": "Jurisdiction-specific restriction codes",
    "DCD": "Jurisdiction-specific endorsement codes",
    "DBA": "Document Expiration Date",
    "DCS": "Customer Family Name",
    "DAC": "Customer First Name",
    "DAD": "Customer Middle Name(s)",
    "DBD": "Document Issue Date",
    "DBB": "Date of Birth",
    "DBC": "Physical Description - Sex",
    "DAY": "Physical Description - Eye Color",
    "DAU": "Physical Description - Height",
    "DAG": "Address - Street 1",
    "DAI": "Address - City",
    "DAJ": "Address - Jurisdiction Code",
    "DAK": "Address - Postal Code",
    "DAQ": "Customer ID Number",
    "DCF": "Document Discriminator",
    "DCG": "Country Identification",
    "DDA": "Compliance Type",
    "DDB": "Card Revision Date",
    "DDC": "HazMat Endorsement Expiry Date",
    "DDD": "Limited Duration Document Indicator",
    "DAW": "Weight (pounds)",
    "DAX": "Weight (kilograms)",
    "DDH": "Under 18 Until",
    "DDI": "Under 21 Until",
    "DDJ": "Under 21 Until"
}

class QuantumError(Exception):
    pass

class AAMVAEncoder:
    def __init__(self, iin, jurisdiction_code, auto_escape=True):
        self.iin = iin
        self.jurisdiction_code = jurisdiction_code
        self.auto_escape = auto_escape
        self.subfiles = {}
        self.header = f"@\nANSI {self.iin}050102DL00410287ZO02900045DL"
        
    def add_subfile(self, designator, data_dict):
        compiled_data = ""
        for key, value in data_dict.items():
            if value:
                compiled_data += f"{key}{value}\n"
        self.subfiles[designator] = compiled_data.strip()

    def build_payload(self):
        payload = self.header
        for designator, content in self.subfiles.items():
            payload += f"\n{designator}\n{content}"
        return payload
        
    def get_display_payload(self):
        raw = self.build_payload()
        if self.auto_escape:
            return raw.replace("\n", "\\n")
        return raw

class DataValidator:
    @staticmethod
    def check_date_format(date_str, field_name):
        if not re.match(r"^\d{8}$", date_str):
            raise QuantumError(f"{field_name} doit être au format YYYYMMDD (Reçu: {date_str})")
        return True

    @staticmethod
    def check_mandatory_fields(data_dict, required_keys):
        missing = [k for k in required_keys if not data_dict.get(k)]
        if missing:
            raise QuantumError(f"Champs obligatoires manquants : {', '.join(missing)}")
        return True

class QuantumPDF417:
    def __init__(self, payload, columns=12, security_level=2):
        self.payload = payload
        self.columns = columns
        self.security_level = security_level
        self.codes = None
        self.image = None
        self._render_time = 0

    def generate_matrix(self):
        start = time.time()
        try:
            self.codes = encode(self.payload, columns=self.columns, security_level=self.security_level)
            self._render_time = time.time() - start
            logger.info(f"Matrix encoding completed in {self._render_time:.4f}s")
            return self.codes
        except Exception as e:
            logger.error(f"Matrix generation failed: {str(e)}")
            raise QuantumError(f"Erreur d'encodage PDF417: {str(e)}")

    def render(self, scale=5, ratio=3, padding=20):
        if not self.codes:
            self.generate_matrix()
        start = time.time()
        self.image = render_image(self.codes, scale=scale, ratio=ratio, padding=padding)
        logger.info(f"Image rendering completed in {time.time() - start:.4f}s")
        return self.image

    def export_base64(self):
        if not self.image:
            return None
        buf = io.BytesIO()
        self.image.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()

    def get_svg(self, potrace_path):
        if not self.image:
            raise QuantumError("Aucune image rendue pour la vectorisation SVG.")
        if not potrace_path or not os.path.exists(potrace_path):
            logger.warning("Potrace non détecté. Export SVG impossible.")
            return None
            
        start = time.time()
        buf = io.BytesIO()
        self.image.save(buf, format="PNG")
        svg_output = png_to_svg(buf.getvalue(), potrace_path=potrace_path)
        logger.info(f"SVG Vectorization completed in {time.time() - start:.4f}s")
        return svg_output

def generate_random_string(length=8, digits_only=False):
    chars = string.digits if digits_only else string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def calculate_checksum(payload):
    return sum(ord(c) for c in payload) % 256

def inject_quantum_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        :root {
            --bg-color: #020204;
            --card-bg: rgba(20, 20, 25, 0.4);
            --border-color: rgba(157, 80, 255, 0.2);
            --primary-accent: #9d50ff;
            --secondary-accent: #3a82ff;
            --text-main: #f0f0f5;
            --text-muted: #8e8e9e;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            background-image: radial-gradient(circle at 50% 0%, rgba(157, 80, 255, 0.05) 0%, transparent 50%);
        }

        .crystal-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 35px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .crystal-card:hover {
            border-color: rgba(157, 80, 255, 0.4);
            box-shadow: 0 15px 50px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.1);
        }

        .purple-label {
            font-family: 'JetBrains Mono', monospace;
            color: var(--primary-accent);
            font-size: 0.70rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        
        .purple-label::before {
            content: '';
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--primary-accent);
            border-radius: 50%;
            margin-right: 8px;
            box-shadow: 0 0 10px var(--primary-accent);
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div {
            background-color: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            padding: 14px 18px !important;
            font-size: 0.95rem !important;
            font-family: 'JetBrains Mono', monospace !important;
            transition: all 0.2s ease-in-out;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within {
            border-color: var(--primary-accent) !important;
            box-shadow: 0 0 0 1px var(--primary-accent), 0 0 20px rgba(157, 80, 255, 0.2) !important;
            background-color: rgba(10, 10, 15, 0.8) !important;
        }

        /* Sliders */
        div[data-baseweb="slider"] > div:first-child { background: rgba(255, 255, 255, 0.05) !important; }
        div[role="presentation"] > div > div:first-child { background: linear-gradient(90deg, var(--primary-accent), var(--secondary-accent)) !important; }
        div[role="slider"] {
            background-color: #020204 !important;
            border: 3px solid var(--primary-accent) !important;
            box-shadow: 0 0 15px rgba(157, 80, 255, 0.5) !important;
        }

        /* Buttons */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, rgba(157, 80, 255, 0.1), rgba(58, 130, 255, 0.1)) !important;
            border: 1px solid var(--primary-accent) !important;
            color: #fff !important;
            border-radius: 14px !important;
            padding: 16px 0 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
            overflow: hidden;
            position: relative;
        }

        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: all 0.5s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, var(--primary-accent), var(--secondary-accent)) !important;
            box-shadow: 0 10px 30px rgba(157, 80, 255, 0.4) !important;
            transform: translateY(-2px);
            border-color: transparent !important;
        }
        
        .stButton > button:hover::before { left: 100%; }

        .stCodeBlock, pre {
            background: rgba(0, 0, 0, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px !important;
        }
        
        .metric-container {
            display: flex;
            justify-content: space-between;
            background: rgba(0,0,0,0.5);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="purple-label">System Diagnostics</div>', unsafe_allow_html=True)
        st.success("Quantum Engine : ONLINE")
        st.caption(f"Init: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider()
        st.markdown('<div class="purple-label">Jurisdiction Select</div>', unsafe_allow_html=True)
        country = st.selectbox("Source Nation", ["Canada", "United States"])
        
        if country == "United States":
            region = st.selectbox("State / Territory", sorted(IIN_US.keys()))
            iin = IIN_US[region]
        else:
            region = st.selectbox("Province / Territory", sorted(IIN_CA.keys()))
            iin = IIN_CA[region]
            
        st.divider()
        st.markdown('<div class="purple-label">Renderer Settings</div>', unsafe_allow_html=True)
        res_dpi = st.select_slider("Resolution (DPI)", options=[300, 600, 1200, 2400], value=600)
        m_cols = st.slider("Matrix Columns (Aspect Ratio)", 4, 30, 12)
        m_sec = st.slider("Error Correction (ECL)", 1, 8, 3)
        q_padding = st.slider("Quiet Zone Padding (px)", 0, 100, 15)
        
        st.divider()
        st.markdown('<div class="purple-label">Formatting Control</div>', unsafe_allow_html=True)
        use_escape = st.checkbox("Utilisez \\n pour ENTRÉE", value=True, help="Force l'affichage des séquences d'évasion.")
        auto_gen_id = st.checkbox("Auto-Generate Document IDs", value=False)
        
        st.markdown(
            '<div style="margin-top:50px; font-size:0.7rem; color:rgba(255,255,255,0.3); text-align:center;">'
            'AAMVA PDF417 Generator v3.0.0<br/>Strict Compliance Mode Active</div>', 
            unsafe_allow_html=True
        )
        return country, region, iin, res_dpi, m_cols, m_sec, q_padding, use_escape, auto_gen_id

def show_identity_gen():
    initialize_session_state()
    inject_quantum_styles()
    
    st.markdown(
        '<h1 style="text-align: center; font-weight: 800; font-size: 3rem; letter-spacing: -2px; margin-bottom: 0;">'
        'STUDIO <span style="color: #9d50ff;">QUANTUM</span></h1>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="text-align: center; color: #8e8e9e; font-size: 1.1rem; margin-bottom: 40px;">'
        'AAMVA Compliant Data-Matrix Synthesizer</p>', 
        unsafe_allow_html=True
    )

    country, region, iin, res_dpi, m_cols, m_sec, q_padding, use_escape, auto_gen_id = render_sidebar()

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.markdown('<div class="purple-label">Primary Identity Metadata</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        f_dcs = st.text_input("DCS (Family Name)", "NICOLAS")
        f_dac = st.text_input("DAC (First Name)", "JEAN")
        f_dad = st.text_input("DAD (Middle Name)", "")
    with col2:
        default_id = f"N{generate_random_string(4, True)}-{generate_random_string(6, True)}-{generate_random_string(2, True)}" if auto_gen_id else "N2420-941208-96"
        f_daq = st.text_input("DAQ (License Number)", default_id)
        f_dbb = st.text_input("DBB (Date of Birth)", "19941208", help="Format: YYYYMMDD")
        f_dbc = st.selectbox("DBC (Sex)", ["1 (Male)", "2 (Female)", "9 (Not Specified)"])
    with col3:
        f_dag = st.text_input("DAG (Address 1)", "1560 SHERBROOKE ST E")
        f_dai = st.text_input("DAI (City)", "MONTREAL")
        f_dak = st.text_input("DAK (Postal Code)", "H2L4M1")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="crystal-card">', unsafe_allow_html=True)
    st.markdown('<div class="purple-label">Document Validity & Physical Traits</div>', unsafe_allow_html=True)
    
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        f_dbd = st.text_input("DBD (Issue Date)", datetime.datetime.now().strftime("%Y%m%d"))
    with a2:
        exp_date = (datetime.datetime.now() + datetime.timedelta(days=365*5)).strftime("%Y%m%d")
        f_dba = st.text_input("DBA (Expiry Date)", exp_date)
    with a3:
        f_dau = st.text_input("DAU (Height)", "180 cm")
    with a4:
        f_day = st.selectbox("DAY (Eyes)", ["BLK", "BLU", "BRO", "GRY", "GRN", "HAZ", "PNK", "DIC"])

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("SYNTHESIZE MATRIX // EXECUTE"):
        try:
            DataValidator.check_date_format(f_dbb, "DBB (DOB)")
            DataValidator.check_date_format(f_dbd, "DBD (Issue)")
            DataValidator.check_date_format(f_dba, "DBA (Expiry)")
            DataValidator.check_mandatory_fields({'dcs': f_dcs, 'dac': f_dac, 'daq': f_daq}, ['dcs', 'dac', 'daq'])

            with st.spinner("Quantum Engine Processing..."):
                st_code = region[:2].upper() if country == "United States" else "QC"
                
                builder = AAMVAEncoder(iin, st_code, auto_escape=use_escape)
                builder.add_subfile("DL", {
                    "DAQ": f_daq.upper(),
                    "DCS": f_dcs.upper(),
                    "DAC": f_dac.upper(),
                    "DAD": f_dad.upper(),
                    "DFI": generate_random_string(5),
                    "DBD": f_dbd,
                    "DBB": f_dbb,
                    "DBC": f_dbc[0],
                    "DAY": f_day,
                    "DAU": f_dau,
                    "DAG": f_dag.upper(),
                    "DAI": f_dai.upper(),
                    "DAJ": st_code,
                    "DAK": f_dak.replace(" ", "").upper(),
                    "DBA": f_dba,
                    "DCF": generate_random_string(16, True),
                    "DCG": "USA" if country == "United States" else "CAN",
                    "DDA": "F",
                    "DDB": datetime.datetime.now().strftime("%m%d%Y")
                })

                raw_payload = builder.build_payload()
                display_payload = builder.get_display_payload()

                res_col1, res_col2 = st.columns([1, 1.2])
                
                with res_col1:
                    st.markdown('<div class="purple-label">Raw Binary Payload</div>', unsafe_allow_html=True)
                    st.code(display_payload, language="text")
                    
                    st.markdown('<div class="purple-label">Engine Telemetry</div>', unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class="metric-container"><span>Payload Size</span><span style="color:#9d50ff; font-family:monospace;">{len(raw_payload)} Bytes</span></div>
                        <div class="metric-container"><span>Checksum (Mod 256)</span><span style="color:#9d50ff; font-family:monospace;">{calculate_checksum(raw_payload)}</span></div>
                        <div class="metric-container"><span>Data Fields</span><span style="color:#9d50ff; font-family:monospace;">{len(builder.subfiles['DL'].split(chr(10)))} Active</span></div>
                        """, 
                        unsafe_allow_html=True
                    )

                with res_col2:
                    st.markdown('<div class="purple-label">Optical Render Output</div>', unsafe_allow_html=True)
                    
                    pdf417_engine = QuantumPDF417(raw_payload, columns=m_cols, security_level=m_sec)
                    render_scale = max(1, int(res_dpi / 90))
                    
                    img_output = pdf417_engine.render(scale=render_scale, padding=q_padding)
                    png_buf = io.BytesIO()
                    img_output.save(png_buf, format="PNG")
                    
                    st.image(png_buf.getvalue(), use_container_width=True, caption=f"Resolution: {res_dpi} DPI | ECL: {m_sec}")
                    
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        st.download_button(
                            label="EXPORT PNG RASTER",
                            data=png_buf.getvalue(),
                            file_name=f"AAMVA_{f_daq}_{int(time.time())}.png",
                            mime="image/png"
                        )
                    
                    with dl_col2:
                        path_potrace = shutil.which("potrace")
                        if path_potrace:
                            svg_data = pdf417_engine.get_svg(path_potrace)
                            if svg_data:
                                st.download_button(
                                    label="EXPORT SVG VECTOR",
                                    data=svg_data,
                                    file_name=f"AAMVA_{f_daq}_{int(time.time())}.svg",
                                    mime="image/svg+xml"
                                )
                        else:
                            st.error("Potrace Binary Missing - SVG Disabled")

                    if path_potrace and svg_data:
                        with st.expander("INSPECT VECTOR CODE (XML)"):
                            st.markdown(
                                f'<div style="background:#fff; padding:20px; border-radius:8px;">{svg_data}</div>', 
                                unsafe_allow_html=True
                            )
                            st.code(svg_data, language="xml")

                st.session_state.gen_count += 1
                st.session_state.history.append({
                    "id": f_daq,
                    "name": f"{f_dcs}, {f_dac}",
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        except QuantumError as qe:
            st.error(f"Quantum Validation Error: {str(qe)}")
        except Exception as e:
            st.error(f"Critical System Failure: {str(e)}")
            st.code(traceback.format_exc())

    if st.session_state.history:
        st.divider()
        st.markdown('<div class="purple-label">Session Ledger</div>', unsafe_allow_html=True)
        st.table(st.session_state.history[::-1][:10])

def selftest_routine():
    logger.info("Initiating Quantum Engine Self-Test")
    test_str = "19901231"
    try:
        DataValidator.check_date_format(test_str, "Test_DOB")
        logger.info("Self-Test Passed: Regex Validation")
    except Exception as e:
        logger.error(f"Self-Test Failed: {str(e)}")

if __name__ == "__main__":
    if os.environ.get("QUANTUM_DEBUG") == "1":
        selftest_routine()
    show_identity_gen()
