import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io

def show_identity_gen():
    st.title("🪪 PDF417 Free Generator")
    st.write("Professional AAMVA-compliant barcode orchestration service.")
    st.divider()

    # STEP 1: JURISDICTION
    st.markdown("### 🌍 Étape 1 : Sélection de la Juridiction")
    col_geo1, col_geo2 = st.columns(2)
    
    with col_geo1:
        country = st.selectbox("Sélectionner le Pays", ["United States", "Canada"], key="country_sel")
    
    with col_geo2:
        if country == "United States":
            region = st.selectbox("Sélectionner l'État", sorted(list(IIN_US.keys())), index=4, key="state_sel")
            mock_iin = IIN_US.get(region)
        else:
            region = st.selectbox("Sélectionner la Province", sorted(list(IIN_CA.keys())), key="prov_sel")
            mock_iin = IIN_CA.get(region)

    st.divider()

    # STEP 2: FIELDS
    st.markdown("### ✍️ Étape 2 : Champs préfixés (saisie)")
    
    col1, col2 = st.columns(2)
    with col1:
        dcg = st.text_input("DCG", "USA" if country == "United States" else "CAN", help="Country Identification")
        dac = st.text_input("DAC", "JEAN", help="First Name")
        dcs = st.text_input("DCS", "NICOLAS", help="Last Name")
        dbb = st.text_input("DBB", "19941208", help="Date of Birth (YYYYMMDD)")
        daq = st.text_input("DAQ", "D9823415", help="License Number")
        dag = st.text_input("DAG", "1560 SHERBROOKE ST E", help="Street Address")
        
    with col2:
        dai = st.text_input("DAI", "MONTREAL", help="City")
        dak = st.text_input("DAK", "H2L4M1", help="Postal Code")
        dbd = st.text_input("DBD", "20230510", help="Document Issue Date")
        dba = st.text_input("DBA", "20310509", help="Document Expiration Date")
        dbc = st.selectbox("DBC", ["1", "2", "3"], help="Sex (1=Male, 2=Female, 3=Other)")
        dcf = st.text_input("DCF", "PEJQ04N96", help="Document Discriminator")

    st.divider()

    # STEP 3: OPTIONS & GENERATION
    st.markdown("### 🚀 Étape 3 : Configuration & Génération")
    
    with st.expander("🛠️ Paramètres du Code-barres (Avancé)", expanded=False):
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            unit = st.selectbox("Largeur de module unité", ["Pixel", "mm", "mils"], index=1) # Default to mm
            module_width = st.number_input("Largeur du module", min_value=0.1, max_value=1.0, value=0.38, step=0.01)
            dpi = st.slider("Résolution d'image (DPI)", 72, 600, 600) # High default
            img_format = st.selectbox("Format d'image", ["SVG", "PNG"], index=0)
            
        with adv_col2:
            show_hrt = st.radio("Afficher le texte lisible (HRT)", ["NON", "OUI"], index=0)
            quiet_unit = st.selectbox("Unité de la zone de repos", ["mm", "Pixel", "mils"], index=0)
            quiet_zone = st.number_input("Zone de repos (Padding)", min_value=0.0, max_value=50.0, value=3.0)
            eval_escapes = st.checkbox("Évaluer les séquences d'échappement", value=True)

    if st.button("Générer le Bloc AAMVA & Code-barres", use_container_width=True):
        # AAMVA Header Construction
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        # Build the structured data string
        # DL is already part of the header usually or a segment
        raw_data = f"@\n{aamva_header}\nDCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\nDAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        
        # Process escape sequences
        if eval_escapes:
            raw_data = raw_data.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
            
        st.success("Données AAMVA générées avec succès")
        with st.expander("Voir le Code Brut"):
            st.code(raw_data, language="text")

        try:
            # Generate PDF417 Bit Codes
            columns = 10
            codes = encode(raw_data, columns=columns)
            
            # Rendering scale logic
            scale_factor = module_width
            if unit == "mm": scale_factor = int(module_width * 3.78)
            elif unit == "mils": scale_factor = int(module_width * 0.096)
            
            padding = quiet_zone
            
            # GENERATE PNG
            if img_format == "PNG":
                image = render_image(codes, scale=max(1, scale_factor), padding=padding)
                buf = io.BytesIO()
                image.save(buf, format="PNG", dpi=(dpi, dpi))
                byte_im = buf.getvalue()
                
                st.subheader("Aperçu du Code-barres (PNG)")
                st.image(byte_im, use_container_width=True)
                
                st.download_button(
                    label="📥 Télécharger le Code-barres (PNG)",
                    data=byte_im,
                    file_name=f"pdf417_{region}_{dcs}.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            # GENERATE SVG
            else:
                from reportlab.graphics.shapes import Drawing, Rect
                from reportlab.graphics import renderSVG
                from reportlab.lib import colors
                
                # pdf417gen codes is a list of integers representing bit patterns
                mod_width = max(1, scale_factor)
                mod_height = mod_width * 3
                
                rows = len(codes)
                cols = len(codes[0]) if rows > 0 else 0
                
                draw_width = (cols * mod_width) + (2 * padding * mod_width)
                draw_height = (rows * mod_height) + (2 * padding * mod_height)
                
                d = Drawing(draw_width, draw_height)
                
                # Draw white background using proper color object
                d.add(Rect(0, 0, draw_width, draw_height, fillColor=colors.white, strokeColor=None))
                
                for r_idx, row in enumerate(codes):
                    y = draw_height - ((r_idx + padding + 1) * mod_height)
                    for c_idx, bit in enumerate(row):
                        if bit:
                            x = (c_idx + padding) * mod_width
                            d.add(Rect(x, y, mod_width, mod_height, fillColor=colors.black, strokeColor=None))
                
                svg_data = renderSVG.drawToString(d)
                
                # Ensure svg_data is a string (drawToString can sometimes return bytes)
                if isinstance(svg_data, bytes):
                    svg_data = svg_data.decode("utf-8")
                
                st.subheader("Aperçu du Code-barres (SVG)")
                st.markdown(f'<div style="background: white; padding: 20px; border-radius: 8px; display: inline-block;">{svg_data}</div>', unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Télécharger le Code-barres (SVG)",
                    data=svg_data,
                    file_name=f"pdf417_{region}_{dcs}.svg",
                    mime="image/svg+xml",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Erreur lors de la génération : {str(e)}")
