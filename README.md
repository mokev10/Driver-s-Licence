# ⚡ PDF417 Free Generator Hub

Professional AAMVA-compliant barcode orchestration service built with Python and Streamlit. This hub serves as a central platform for identity data generation, orchestration, and technical mapping.

## 🚀 Unified Workflow

The application starts directly on the **Identity Gen** interface for maximum efficiency. The generation process follows three fluid steps:

### 1️⃣ Étape 1 : Sélection de la Juridiction
*   **Country Selection**: Choose between the **United States** and **Canada** from a fluid dropdown.
*   **Jurisdiction Mapping**: Dynamically loads the specific AAMVA IIN (Issuer Identification Number) for:
    *   **50 US States** (California, New York, Texas, etc.)
    *   **10 Canadian Provinces** (Ontario, Quebec, British Columbia, etc.)
*   **Automatic IIN Assignment**: The system calculates the header based on the selected region instantly.

### 2️⃣ Étape 2 : Champs préfixés (saisie)
*   **AAMVA Technical Interface**: A modern 2-column grid layout specifically designed for the 14 standard AAMVA prefixes:
    *   **DCG, DCS, DAC, DBB, DAG, DAI, DAJ, DAK, DBD, DBA, DBC, DAU, DAY, DCF**.
*   **Smart Defaults**: The **DCG** field (Country Identification) intelligently updates to "USA" or "CAN" based on your Step 1 selection.
*   **Integrated Documentation**: Hover over the help icons (❓) to see the full description of each technical field.

### 3️⃣ Étape 3 : Génération du PDF417
*   **Dynamic Encoding**: One-click generation of the standardized AAMVA data block.
*   **High-Density Rendering**: Produces professional-grade PDF417 barcodes using the `pdf417gen` engine.
*   **Export Options**:
    *   **Raw Data**: View the encoded data block in a code expander.
    *   **PNG Download**: Instantly download the barcode as a high-quality image (`pdf417_[region]_[last_name].png`).

---

## 🏗️ Technical Architecture

*   **Frontend**: Streamlit with custom "Elegant Dark" CSS for a tactile, professional-grade interface.
*   **Animation Engine**: CSS-based `fadeIn` transitions for smooth component loading.
*   **Barcode Logic**: `pdf417gen` Python library for high-performance encoding.
*   **Navigation**: sidebar-based radio navigation allowing access to secondary modules:
    *   🏠 **Hub Overview**: View active modules and system uptime.
    *   📊 **Data Analysis**: Interactive Plotly-based analytics tools.
    *   ⚙️ **Settings**: Global system configuration.

## 🛠️ Getting Started

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Launch**:
    ```bash
    streamlit run app.py
    ```

Built for precision, reliability, and modern user experience.
