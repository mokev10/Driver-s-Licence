import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io


def show_identity_gen():
    st.title("AAMVA Raw Data Generator")
    st.write("Advanced tool for generating forensic-quality AAMVA raw data strings")
    st.divider()

    # STEP 1: JURISDICTION

    col_geo1, col_geo2 = st.columns(2)

    with col_geo1:
        country = st.selectbox(
            "Sélectionner le Pays",
            ["United States", "Canada"],
            key="country_sel"
        )

    # ICON DYNAMIQUE (basé sur country sélectionné)
    icon_url = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="{icon_url}" width="24">
            <h3 style="margin:0;">Step 1: Select the country and state or province</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col_geo2:
        if country == "United States":
            region = st.selectbox(
                "Sélectionner l'État/Territoire",
                sorted(list(IIN_US.keys())),
                key="state_sel"
            )
            mock_iin = IIN_US.get(region)
        else:
            region = st.selectbox(
                "Sélectionner la Province",
                sorted(list(IIN_CA.keys())),
                key="prov_sel"
            )
            mock_iin = IIN_CA.get(region)

    st.divider()

    # STEP 2: MANDATORY FIELDS
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://img.icons8.com/external-itim2101-lineal-itim2101/64/external-pipeline-plumber-tools-itim2101-lineal-itim2101-6.png" width="24">
            <h3 style="margin:0;">Step 2: Required fields (AAMVA)</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

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

    # STEP 3
    st.markdown("### Step 3: Configuration & Generation")

    if st.button("GÉNÉRER LE CODE-BARRES & LA CHAÎNE", use_container_width=True):

        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

        raw_data_internal = (
            f"@\n{aamva_header}\n"
            f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\n"
            f"DAQ{daq}\nDAG{dag}\nDAI{dai}\n"
            f"DAJ{region[:2].upper()}\nDAK{dak}\n"
            f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        )

        raw_data_display = raw_data_internal.replace("\n", "\\n")

        st.success("Génération terminée")

        col_out1, col_out2 = st.columns(2)

        with col_out1:
            st.code(raw_data_display)

        try:
            codes = encode(raw_data_internal, columns=10)
            image = render_image(codes, scale=2, padding=3)

            with col_out2:
                st.image(image)

        except Exception as e:
            st.error(f"Erreur: {e}")
