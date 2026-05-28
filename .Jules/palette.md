## 2025-05-22 - Improving Technical Form Accessibility in Streamlit

**Learning:** For forms involving specialized industry standards (like AAMVA), providing localized tooltips for technical acronyms (DCG, DAC, etc.) significantly improves accessibility for non-expert users without cluttering the UI. In Streamlit, the `help` parameter on inputs is the most effective way to do this while adhering to design system constraints that prohibit custom CSS.

**Action:** Always include a `tips` or `help` key in localization dictionaries for technical fields and map them to the `help` parameter of Streamlit input components.
