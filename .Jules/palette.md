## 2025-05-15 - [Improving Technical Field Clarity and Label Contrast]
**Learning:** In a specialized tool like an AAMVA PDF417 generator, technical acronyms (DCG, DAC, DCS, etc.) can be confusing. Using Streamlit's 'help' parameter provides non-intrusive documentation. Additionally, the 'Liquid Glass' theme requires high-contrast labels (rgba(255, 255, 255, 0.9)) to remain readable against dark, blurred backgrounds.
**Action:** Always provide tooltips for technical acronyms and ensure label contrast is at least 0.9 opacity for white text on dark themed glassmorphism components.
