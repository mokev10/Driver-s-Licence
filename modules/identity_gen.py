import streamlit as st
import datetime
from utils.constants import IIN_US, IIN_CA
from pdf417gen import encode, render_image
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

    st.title(t["title"])
    st.write(t["desc"])
    st.divider()

    # ================= STEP 1 =================
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
            region = st.selectbox(t["state"], sorted(IIN_US.keys()), key="state_sel")
            mock_iin = IIN_US[region]
        else:
            region = st.selectbox(t["prov"], sorted(IIN_CA.keys()), key="prov_sel")
            mock_iin = IIN_CA[region]

    st.divider()

    # ================= STEP 2 =================
    st.markdown(f"### {t['step2']}")

    col1, col2 = st.columns(2)

    with col1:
        dcg = st.text_input("DCG", "USA" if country == "United States" else "CAN")
        dac = st.text_input("DAC", "JEAN")
        dcs = st.text_input("DCS", "NICOLAS")
        dbb = st.text_input("DBB", "19941208")
        daq = st.text_input("DAQ", "D9823415")
        dag = st.text_input("DAG", "1560 SHERBROOKE ST E")

    with col2:
        dai = st.text_input("DAI", "MONTREAL")
        dak = st.text_input("DAK", "H2L4M1")
        dbd = st.text_input("DBD", "20230510")
        dba = st.text_input("DBA", "20310509")
        dbc = st.selectbox("DBC", ["1", "2", "3"])
        dcf = st.text_input("DCF", "PEJQ04N96")

    st.divider()

    # ================= STEP 3 =================
    st.markdown(f"### {t['step3']}")

    with st.expander("Barcode Settings"):

        unit = st.selectbox("Unit", ["Pixel", "mm", "mils"], index=1)
        module_width = st.number_input("Module width", 0.1, 1.0, 0.38)
        dpi = st.slider("DPI", 72, 600, 600)
        img_format = st.selectbox("Format", ["SVG", "PNG"])

        quiet_zone = st.number_input("Padding", 0.0, 50.0, 3.0)

    if st.button(t["generate"], use_container_width=True):

        header = f"ANSI {mock_iin}050102DL00410287ZO02900045DL"

        raw_data = (
            f"@\n{header}\n"
            f"DCG{dcg}\nDCS{dcs}\nDAC{dac}\nDBB{dbb}\nDAQ{daq}\n"
            f"DAG{dag}\nDAI{dai}\nDAJ{region[:2].upper()}\nDAK{dak}\n"
            f"DBD{dbd}\nDBA{dba}\nDBC{dbc}\nDCF{dcf}"
        )

        st.success(t["success"])

        col_out1, col_out2 = st.columns(2)

        with col_out1:
            st.code(raw_data.replace("\n", "\\n"))

        codes = encode(raw_data, columns=10)

        # SCALE
        dpi_factor = dpi / 25.4
        scale = max(1, module_width * dpi_factor)

        with col_out2:
            if img_format == "PNG":

                img = render_image(codes, scale=int(scale), padding=int(quiet_zone))

                buf = io.BytesIO()
                img.save(buf, format="PNG", dpi=(dpi, dpi))

                st.image(buf.getvalue())

                st.download_button(
                    "Download PNG",
                    buf.getvalue(),
                    f"{dcs}.png",
                    "image/png"
                )

            else:
                # ================= SVG REAL (NO padding bug) =================
                from reportlab.graphics.shapes import Drawing, Rect
                from reportlab.graphics import renderSVG
                from reportlab.lib import colors

                mod = scale
                h = mod * 3

                rows = len(codes)
                cols = len(codes[0])

                width = cols * mod
                height = rows * h

                d = Drawing(width, height)

                d.add(Rect(0, 0, width, height, fillColor=colors.white))

                for r, row in enumerate(codes):
                    for c, bit in enumerate(row):
                        if bit:
                            x = c * mod
                            y = height - (r * h)
                            d.add(Rect(x, y, mod, h, fillColor=colors.black))

                svg = renderSVG.drawToString(d)

                st.markdown(
                    f'<div style="background:white;padding:10px">{svg}</div>',
                    unsafe_allow_html=True
                )

                st.download_button(
                    "Download SVG",
                    svg,
                    f"{dcs}.svg",
                    "image/svg+xml"
                )
