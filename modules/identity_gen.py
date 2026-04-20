import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io

def show_identity_gen():
    st.title("🪪 AAMVA Raw Data Generator")
    st.write("Advanced tool for generating forensic-quality AAMVA raw data strings")
    st.divider()

    # STEP 1: JURISDICTION
    st.markdown("### Step 1: Select the country and state or province")
    col_geo1, col_geo2 = st.columns(2)
    
    with col_geo1:
        country = st.selectbox("Sélectionner le Pays", ["United States", "Canada"], key="country_sel")
    
    with col_geo2:
        if country == "United States":
            region = st.selectbox("Sélectionner l'État/Territoire", sorted(list(IIN_US.keys())), index=4, key="state_sel")
            mock_iin = IIN_US.get(region)
        else:
            region = st.selectbox("Sélectionner la Province", sorted(list(IIN_CA.keys())), key="prov_sel")
            mock_iin = IIN_CA.get(region)

    st.divider()

    # STEP 2: MANDATORY FIELDS
    st.markdown("### ✍️ Étape 2 : Champs obligatoires (AAMVA)")
    
    col1, col2 = st.columns(2)
    with col1:
        dcg = st.text_input("DCG (Country)", "USA" if country == "United States" else "CAN")
        dac = st.text_input("DAC (First Name)", "JEAN")
        dcs = st.text_input("DCS (Last Name)", "NICOLAS")
        dbb = st.text_input("DBB (DOB YYYYMMDD)", "19941208")
        daq = st.text_input("DAQ (License No)", "D9823415")
        dag = st.text_input("DAG (Address)", "1560 SHERBROOKE ST E")
        
    with col2:
        dai = st.text_input("DAI (City)", "MONTREAL")
        dak = st.text_input("DAK (Postal Code)", "H2L4M1")
        dbd = st.text_input("DBD (Issue Date)", "20230510")
        dba = st.text_input("DBA (Expiry Date)", "20310509")
        dbc = st.selectbox("DBC (Sex)", ["1", "2", "3"])
        dcf = st.text_input("DCF (Reference No)", "PEJQ04N96")

    st.divider()

    # STEP 3: OPTIONS & GENERATION
    st.markdown("### 🚀 Étape 3 : Configuration & Génération")
    
    with st.expander("🛠️ Paramètres du Code-barres (Avancé)", expanded=True):
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            unit = st.selectbox("Largeur de module unité", ["Pixel", "mm", "mils"], index=1)
            module_width = st.number_input("Largeur du module", min_value=0.1, max_value=1.0, value=0.38, step=0.01)
            dpi = st.slider("Résolution d'image (DPI)", 72, 600, 600)
            img_format = st.selectbox("Format d'image", ["SVG", "PNG"], index=0)
            
        with adv_col2:
            show_hrt = st.radio("Afficher le texte lisible (HRT)", ["NON", "OUI"], index=0)
            quiet_unit = st.selectbox("Unité de la zone de repos", ["mm", "Pixel", "mils"], index=0)
            quiet_zone = st.number_input("Zone de repos (Padding)", min_value=0.0, max_value=50.0, value=3.0)
            eval_escapes = st.checkbox("Évaluer les séquences d'échappement", value=True)

    if st.button("GÉNÉRER LE CODE-BARRES & LA CHAÎNE", use_container_width=True):
        # AAMVA Header Construction
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        # Internal raw data (with real newlines for generation)
        raw_data_internal = f"@\n{aamva_header}\nDCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\nDAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        
        # Display Raw Data String (with literal \n for user copy-paste)
        raw_data_display = raw_data_internal.replace("\n", "\\n")
        
        st.success("Génération HDR (600 DPI) terminée.")
        
        col_out1, col_out2 = st.columns([1, 1])
        
        with col_out1:
            st.markdown("#### 📄 Chaîne Brute (Raw Data)")
            st.code(raw_data_display, language="text")
            st.info("Utilisez cette chaîne dans vos outils externes.")

        try:
            # Generate PDF417 Bit Codes
            codes = encode(raw_data_internal, columns=10)
            
            # Rendering scale logic (DPI-Aware Precision)
            # 1 inch = 25.4 mm
            pixels_per_inch = dpi
            pixels_per_mm = pixels_per_inch / 25.4
            
            if unit == "mm":
                scale_factor = module_width * pixels_per_mm
            elif unit == "mils":
                # 1 mil = 1/1000 inch
                scale_factor = (module_width / 1000) * pixels_per_inch
            else: # Pixel
                scale_factor = module_width
            
            # For SVG/PNG rendering, we need at least 1 pixel module width
            final_scale = max(1.0, float(scale_factor))
            padding = int(quiet_zone)
            
            with col_out2:
                st.markdown(f"#### 🖼️ Aperçu ({img_format})")
                # GENERATE PNG
                if img_format == "PNG":
                    image = render_image(codes, scale=max(1, int(final_scale)), padding=padding)
                    buf = io.BytesIO()
                    image.save(buf, format="PNG", dpi=(dpi, dpi))
                    byte_im = buf.getvalue()
                    
                    st.image(byte_im, use_container_width=True)
                    
                    st.download_button(
                        label="📥 Télécharger PNG",
                        data=byte_im,
                        file_name=f"pdf417_{dcs}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                # GENERATE SVG
                else:
                    from reportlab.graphics.shapes import Drawing, Rect
                    from reportlab.graphics import renderSVG
                    from reportlab.lib import colors
                    
                    mod_width = final_scale
                    mod_height = mod_width * 3
                    
                    rows = len(codes)
                    cols = len(codes[0]) if rows > 0 else 0
                    
                    draw_width = (cols * mod_width) + (2 * padding * mod_width)
                    draw_height = (rows * mod_height) + (2 * padding * mod_height)
                    
                    d = Drawing(draw_width, draw_height)
                    
                    # Fill white background
                    d.add(Rect(0, 0, draw_width, draw_height, fillColor=colors.white, strokeColor=None))
                    
                    for r_idx, row in enumerate(codes):
                        # Coordinate system for reportlab starts from bottom
                        y = draw_height - ((r_idx + padding + 1) * mod_height)
                        for c_idx, bit in enumerate(row):
                            if bit:
                                x = (c_idx + padding) * mod_width
                                d.add(Rect(x, y, mod_width, mod_height, fillColor=colors.black, strokeColor=None))
                    
                    svg_data = renderSVG.drawToString(d)
                    if isinstance(svg_data, bytes):
                        svg_data = svg_data.decode("utf-8")
                    
                    # Make SVG responsive for the preview window
                    # We inject a viewBox and remove hardcoded width/height to let the browser scale it
                    responsive_svg = svg_data.replace('<svg ', f'<svg viewBox="0 0 {draw_width} {draw_height}" preserveAspectRatio="xMinYMin meet" ')
                    # Force the SVG to take 100% width of the parent div
                    responsive_svg = responsive_svg.replace('width=', 'data-orig-width=').replace('height=', 'data-orig-height=')
                    
                    st.markdown(
                        f'''
                        <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #444; width: 100%;">
                            {responsive_svg}
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                    
                    st.download_button(
                        label="📥 Télécharger SVG",
                        data=svg_data,
                        file_name=f"pdf417_{dcs}.svg",
                        mime="image/svg+xml",
                        use_container_width=True
                    )
                    
        except Exception as e:
            st.error(f"Erreur lors de la génération visuelle : {str(e)}")
