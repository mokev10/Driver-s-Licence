import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
import io

def show_identity_gen():
    st.header("🪪 Identity Generation Module")
    st.write("Specialized module for generating AAMVA-compliant identity data and PDF417 barcodes.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Personal Data")
        first_name = st.text_input("First Name", "ELIJAH")
        last_name = st.text_input("Last Name", "WALKER")
        dob = st.date_input("Date of Birth", datetime.date(1992, 7, 24))
        
    with col2:
        st.subheader("Regional Config")
        country = st.selectbox("Country", ["United States", "Canada"])
        if country == "United States":
            region = st.selectbox("State", sorted(list(IIN_US.keys())), index=4) # Default to California
        else:
            region = st.selectbox("Province", sorted(list(IIN_CA.keys())))

    if st.button("Generate AAMVA Data Block & Barcode", use_container_width=True):
        # Get correct IIN from constants
        mock_iin = IIN_US.get(region) if country == "United States" else IIN_CA.get(region)
        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"
        
        raw_data = f"@\n{aamva_header}\nDAQD9823415\nDCS{last_name}\nDAC{first_name}\nDBB{dob.strftime('%Y%m%d')}"
        
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
                file_name=f"dl_barcode_{last_name}.png",
                mime="image/png",
            )
        except Exception as e:
            st.error(f"Error generating barcode: {str(e)}")
