## 2025-05-15 - [AAMVA Tooltip Clarity and Visibility]
**Learning:** For forms involving specialized industry standards (like AAMVA), providing localized tooltips for technical acronyms significantly improves accessibility for non-expert users. In custom dark themes like 'Liquid Glass', Streamlit's default help icons have poor contrast and require specific CSS overrides targeting `button[aria-label^="Help for"]` and its nested `svg`.
**Action:** Always provide descriptive tooltips for technical acronyms and use targeted CSS to ensure help icons meet contrast standards in custom themes.
