# ⚡ PDF417 Free Generator Hub

Professional AAMVA-compliant barcode orchestration service built with Python and Streamlit.

## 🚀 Fluent generation steps

The application is structured into three intuitive stages to ensure accuracy and ease of use:

### 🌍 Étape 1 : Sélection de la Juridiction
*   **Country Selection**: Choose between the United States and Canada.
*   **Jurisdiction Mapping**: Automatically loads the specific AAMVA IIN (Issuer Identification Number) for all 50 US States and 10 Canadian Provinces.

### ✍️ Étape 2 : Champs préfixés (saisie)
*   **Technical Mapping**: Input data directly into the standard AAMVA fields (DCG, DCS, DAC, etc.).
*   **Real-time Validation**: Tooltips provide documentation for each prefixed field to ensure compliance with identity standards.

### 🚀 Étape 3 : Génération du PDF417
*   **Dynamic Encoding**: Generates a raw AAMVA data block with standardized headers.
*   **High-Density Rendering**: Produces a high-resolution PDF417 barcode using the `pdf417gen` engine.
*   **Direct Export**: Instant PNG download for integration into card design software.

---

## 🛠️ Installation & Setup

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 🎨 Design Philosophy
*   **Modern Transitions**: Features CSS-based `fadeIn` animations for page loads.
*   **Tactile UI**: High-contrast dark theme with amber accents and interactive button feedback.
*   **Modular Hub**: Designed to be expanded with additional data analysis or generation tools.
