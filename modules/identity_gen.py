import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io

def show_identity_gen():
    st.header("🪪 Identity Generation Module")
    st.write("Specialized module for generating AAMVA-compliant identity data and PDF417 barcodes.")
    
    st.markdown("### Champs préfixés (saisie)")
    
    # Organizing fields into a 2-column grid to match the screenshot
    col1, col2 = st.columns(2)
    
    with col1:
        dcg = st.text_input("DCG", "CAN", help="Country Identification")
        dac = st.text_input("DAC", "JEAN", help="First Name")
        dag = st.text_input("DAG", "1560 SHERBROOKE ST E", help="Street Address")
        daj = st.selectbox("DAJ", sorted(list(IIN_US.keys()) + list(IIN_CA.keys())), index=55, help="Jurisdiction")
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

    if st.button("Generate AAMVA Data Block & Barcode", use_container_width=True):
        # Determine IIN based on DAJ selection
        mock_iin = IIN_US.get(daj) or IIN_CA.get(daj) or "636000"
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        # Build the data string according to the prefixes
        raw_data = f"@\n{aamva_header}\nDCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAG{dag}\nDAI{dai}\nDAJ{daj[:2].upper()}\nDAK{dak}\nDBD{dbd}\nDBA{dba}\nDBC{dbc}\nDAU{dau}\nDAY{day}\nDCF{dcf}"
        
        st.success("AAMVA Data Block Generated Successfully")
        st.code(raw_data, language="text")
        
        try:
            # Generate PDF417 Barcode
            codes = encode(raw_data, columns=10)
            image = render_image(codes, scale=3)
            
            # Convert to buffer to display in Streamlit
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.subheader("Generated Barcode")
            st.image(byte_im, caption="AAMVA PDF417 Barcode", use_container_width=True)
            
            st.download_button(
                label="Download Barcode Image",
                data=byte_im,
                file_name=f"dl_barcode_{dcs}.png",
                mime="image/png",
            )
        except Exception as e:
            st.error(f"Error generating barcode: {str(e)}")
