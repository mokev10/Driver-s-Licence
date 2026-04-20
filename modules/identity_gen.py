import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image, render_svg
import io


def show_identity_gen(lang="EN"):

    TEXT = {
        "EN": {
            "title": "AAMVA Raw Data Generator",
            "desc": "Advanced tool for generating forensic-quality AAMVA raw data strings",
            "step1": "Step 1: Select the country and state or province",
            "country": "Select Country",
            "state": "Select State/Territory",
            "prov": "Select Province",
            "step2": "Step 2: Required fields (AAMVA)",
            "step3": "Step 3: Configuration & Generation",
            "generate": "GENERATE BARCODE & STRING",
            "success": "HDR generation (600 DPI) completed.",
            "raw": "Raw Data String",
            "use": "Use this string in external tools.",
            "preview": "Preview"
        },
        "FR": {
            "title": "Générateur de données AAMVA",
            "desc": "Outil avancé pour générer des chaînes AAMVA",
            "step1": "Étape 1 : Choisir le pays et la région",
            "country": "Sélectionner le Pays",
            "state": "Sélectionner l'État/Territoire",
            "prov": "Sélectionner la Province",
            "step2": "Étape 2 : Champs obligatoires (AAMVA)",
            "step3": "Étape 3 : Configuration & Génération",
            "generate": "GÉNÉRER LE CODE-BARRES & LA CHAÎNE",
            "success": "Génération HDR (600 DPI) terminée.",
            "raw": "Chaîne brute",
            "use": "Utilisez cette chaîne dans vos outils externes.",
            "preview": "Aperçu"
        }
    }

    t = TEXT.get(lang, TEXT["EN"])

    # =========================
    # HEADER
    # =========================
    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # =========================
    # STEP 1
    # =========================
    col_geo1, col_geo2 = st.columns(2)

    with col_geo1:
        country = st.selectbox(
            t["country"],
            ["United States", "Canada"],
            key="country_sel"
        )

    icon_url = (
        "https://img.icons8.com/external-justicon-flat-justicon/64/external-united-states-countrys-flags-justicon-flat-justicon.png"
        if country == "United States"
        else "https://img.icons8.com/external-justicon-flat-justicon/64/external-canada-countrys-flags-justicon-flat-justicon.png"
    )

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="{icon_url}" width="24">
            <h3 style="margin:0;">{t["step1"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col_geo2:
        if country == "United States":
            region = st.selectbox(
                t["state"],
                sorted(list(IIN_US.keys())),
                index=4,
                key="state_sel"
            )
            mock_iin = IIN_US.get(region)
        else:
            region = st.selectbox(
                t["prov"],
                sorted(list(IIN_CA.keys())),
                key="prov_sel"
            )
            mock_iin = IIN_CA.get(region)

    st.divider()

    # =========================
    # STEP 2
    # =========================
    st.markdown(f"### {t['step2']}")

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

    # =========================
    # STEP 3
    # =========================
    st.markdown(f"### {t['step3']}")

    with st.expander("Barcode Settings (Advanced)"):

        unit = st.selectbox("Unit width", ["Pixel", "mm", "mils"], index=1)
        module_width = st.number_input("Module width", 0.1, 1.0, 0.38, 0.01)
        dpi = st.slider("DPI", 72, 600, 600)
        img_format = st.selectbox("Image format", ["SVG", "PNG"], index=0)
        quiet_zone = st.number_input("Padding", 0.0, 50.0, 3.0)

    # =========================
    # GENERATION
    # =========================
    if st.button(t["generate"], use_container_width=True):

        aamva_header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

        raw_data_internal = (
            f"@\n{aamva_header}\n"
            f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
            f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
            f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        )

        raw_data_display = raw_data_internal.replace("\n", "\\n")

        st.success(t["success"])

        col_out1, col_out2 = st.columns(2)

        with col_out1:
            st.markdown(f"#### 📄 {t['raw']}")
            st.code(raw_data_display)
            st.info(t["use"])

        try:
            codes = encode(raw_data_internal, columns=10)

            pixels_per_inch = dpi
            pixels_per_mm = pixels_per_inch / 25.4

            if unit == "mm":
                scale_factor = module_width * pixels_per_mm
            elif unit == "mils":
                scale_factor = (module_width / 1000) * pixels_per_inch
            else:
                scale_factor = module_width

            final_scale = max(1.0, float(scale_factor))
            padding = int(quiet_zone)

            with col_out2:
                st.markdown(f"#### 🖼️ {t['preview']} ({img_format})")

                # =========================
                # PNG EXPORT
                # =========================
                if img_format == "PNG":

                    image = render_image(
                        codes,
                        scale=max(1, int(final_scale)),
                        padding=padding
                    )

                    buf = io.BytesIO()
                    image.save(buf, format="PNG", dpi=(dpi, dpi))
                    byte_im = buf.getvalue()

                    st.image(byte_im, use_container_width=True)

                    st.download_button(
                        "📥 PNG Export",
                        data=byte_im,
                        file_name=f"pdf417_{dcs}.png",
                        mime="image/png"
                    )

                # =========================
                # SVG EXPORT (REAL 600 DPI SCALE)
                # =========================
                else:

                    svg = render_svg(
                        codes,
                        scale=int(final_scale),
                        ratio=3,
                        padding=padding,
                        color="black"
                    )

                    svg_string = svg.toxml()

                    st.markdown(
                        f"""
                        <div style="background:white;padding:15px;border-radius:8px;">
                            {svg_string}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.download_button(
                        "📥 SVG Export (600 DPI)",
                        data=svg_string,
                        file_name=f"pdf417_{dcs}.svg",
                        mime="image/svg+xml"
                    )

        except Exception as e:
            st.error(f"Erreur : {str(e)}")
