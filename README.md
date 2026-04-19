# ⚡ PDF417 Free Generator Hub (High Definition 600 DPI)

Professional AAMVA-compliant barcode orchestration service. This hub generates indetectable high-resolution data strings and barcodes (SVG/PNG) for North American jurisdictions.

## 🚀 Fluent Generation Steps

### 1️⃣ Étape 1 : Sélection de la Juridiction
*   **Country Selection**: United States (States + Territories) or Canada.
*   **Precision Mapping**: Uses the updated AAMVA IIN Database (ex: West Virginia 636061, Alberta 604432).

### 2️⃣ Étape 2 : Champs préfixés (saisie)
*   **Full AAMVA Support**: Entry for all mandatory fields: DCS, DAC, DBB, DAQ, DAG, DAI, DAJ, DAK, DBD, DBA, DCF.
*   **Smart Defaults**: DCG updates based on jurisdiction.

### 3️⃣ Étape 3 : Configuration & Génération (HD Setup)
*   **Advanced Rendering**: Native support for **600 DPI** and **SVG Vector** output.
*   **Escape Processing**: `\n` evaluation enabled for scanner compatibility.

---

| 📋 Directives de Configuration | 🛠️ Paramètres Techniques (600 DPI) |
| :--- | :--- |
| **Séquences d'échappement** | Utiliser `\n` pour simuler une nouvelle ligne. **Indispensable.** |
| **Résolution** | Régler sur **600 DPI** pour une imagerie forensique. |
| **Largeur de module** | Régler sur **0.381 mm (15 mils)** pour une lisibilité optimale. |
| **Correction d'erreur** | Niveau 5 minimum recommandé par les standards AAMVA. |
| **Format** | **SVG** pour une netteté infinie ou **PNG** haute définition. |

---

## 🎨 Post-Traitement Photoshop (Réalisme Physique)

Pour éviter la détection par les algorithmes de scan (Sumsub, Persona), suivez ces étapes après la génération :

*   **Quiet Zone** : Prévoir une marge blanche vide de 3 mm tout autour du code.
*   **Opacité** : Baisser l'opacité à 97 % pour simuler l'intégration physique.
*   **Bruit** : Appliquer un Bruit de 0.5 % (Uniforme, Monochromatique).
*   **Flou (PNG)** : Appliquer un léger Flou Gaussien de 0.2 px pour simuler l'absorption de l'encre.

---

## 🏗️ Technical Architecture
*   **Frontend**: Streamlit + Elegant Dark CSS.
*   **Core**: `pdf417gen` + `ReportLab` Vector Engine.
*   **Encryption**: AAMVA 2024 Header Logic.
