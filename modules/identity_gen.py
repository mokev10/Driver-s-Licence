import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io

def show_identity_gen():
    st.title("🪪 AAMVA Raw Data Generator")
    st.write("Expert tool for generating forensic-grade AAMVA raw data strings.")
    st.divider()

    # STEP 1: JURISDICTION
    st.markdown("### 🌍 Étape 1 : Sélection de la Juridiction")
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

    # STEP 3: GENERATION
    st.markdown("### 🚀 Étape 3 : Génération de la Chaîne Brute")
    
    st.info("Utilisez cette chaîne brute dans un générateur externe (ex: TEC-IT) avec l'option 'Évaluer les séquences d'échappement' cochée.")

    if st.button("GÉNÉRER LA CHAÎNE @ANSI", use_container_width=True):
        # AAMVA Header Construction
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        # Build the structured data string using \n for escape evaluation
        raw_data = f"@\\n{aamva_header}\\nDCG{dcg}\\nDCS{dcs}\\nDAC{dac}\\nDBB{dbb}\\nDAQ{daq}\\nDAG{dag}\\nDAI{dai}\\nDAJ{region[:2].upper()}\\nDAK{dak}\\nDBD{dbd}\\nDBA{dba}\\nDBC{dbc}\\nDCF{dcf}"
        
        st.success("Chaîne brute générée avec succès (Haute Définition)")
        
        st.markdown("#### Raw Data Output")
        st.code(raw_data, language="text")
        
        st.warning("Note: La séquence \\n est incluse pour être interprétée comme un retour chariot par votre encodeur PDF417.")
