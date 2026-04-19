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
        dag = st.text_input("DAG", "1560 SHERBROOKE ST E", help="Street Address")
        dbd = st.text_input("DBD", "20230510", help="Document Issue Date")
        dbc = st.selectbox("DBC", ["1", "2", "3"], help="Sex (1=Male, 2=Female, 3=Other)")
        day = st.text_input("DAY", "BRUN", help="Eye Color")
        
    with col2:
        dcs = st.text_input("DCS", "NICOLAS", help="Last Name")
        dbb = st.text_input("DBB", "19941208", help="Date of Birth")
        dai = st.text_input("DAI", "MONTREAL", help="City")
        dak = st.text_input("DAK", "H2L4M1", help="Postal Code")
        dba = st.text_input("DBA", "20310509", help="Document Expiration Date")
        dau = st.text_input("DAU", "180", help="Height")
        dcf = st.text_input("DCF", "PEJQ04N96", help="Document Discriminator")

    st.divider()

    # STEP 3: GENERATION
    st.markdown("### 🚀 Étape 3 : Génération du PDF417")
    if st.button("Générer le Bloc AAMVA & Code-barres", use_container_width=True):
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        # Build the data string
        raw_data = f"@\n{aamva_header}\nDCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\nDAU{dau}\nDAY{day}\nDCF{dcf}"
        
        st.success("Données AAMVA générées avec succès")
        with st.expander("Voir le Code Brut"):
            st.code(raw_data, language="text")
        
        try:
            # Generate PDF417 Barcode
            codes = encode(raw_data, columns=10)
            image = render_image(codes, scale=3)
            
            # Convert to buffer
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(byte_im, caption="Code-barres PDF417 AAMVA", use_container_width=True)
            
            st.download_button(
                label="📥 Télécharger le Code-barres (PNG)",
                data=byte_im,
                file_name=f"pdf417_{region}_{dcs}.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erreur lors de la génération : {str(e)}")
