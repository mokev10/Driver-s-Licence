import streamlit as st
from scripts.generate_datamatrix import generate_datamatrix

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Générateur 2D-Codes Data Matrix",
    page_icon="img.icons8.com/external-duo-tone-yogi-aprelliyanto/60/external-search-file-document-duo-tone-yogi-aprelliyanto.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Fond global */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

/* Titre */
h1 {
    text-align: center;
    color: white;
    font-weight: 700;
    margin-bottom: 25px;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    border: 2px solid #334155 !important;
    background-color: #0b1220 !important;
    color: white !important;
    transition: all 0.3s ease-in-out;
}

textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.5);
    transform: scale(1.01);
}

/* Slider */
.stSlider > div {
    color: white;
}

/* bouton */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
    border: none;
    padding: 0.7rem 2rem;
    border-radius: 12px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* ---------------- CENTRAGE IMAGE ---------------- */
.center-img {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-top: 20px;
}

/* force image centrée */
.center-img img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

st.title("Générateur DataMatrix")

data = st.text_area("Texte à encoder")

dpi = st.slider(
    "Image Resolution (DPI)",
    min_value=72,
    max_value=300,
    value=150,
    step=1
)

use_escape = st.checkbox("Activer escape sequences (\\n = retour ligne)")

# ---------------- BOUTON CENTRÉ ----------------
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate = st.button("Générer")

# ---------------- RESULT ----------------

if generate:
    if data.strip():

        if use_escape:
            data = data.encode().decode("unicode_escape")

        img_buffer = generate_datamatrix(data, dpi=dpi)

        # 🔥 WRAPPER CENTRÉ COMPLET
        st.markdown('<div class="center-img">', unsafe_allow_html=True)

        st.image(img_buffer, caption="DataMatrix généré")

        st.download_button(
            label="Télécharger l'image",
            data=img_buffer,
            file_name=f"datamatrix_{dpi}dpi.png",
            mime="image/png"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Veuillez entrer un texte à encoder")
