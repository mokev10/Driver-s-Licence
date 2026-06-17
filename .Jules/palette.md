## 2026-05-05 - Improving Contrast and Technical Clarity

**Learning:** In highly customized Streamlit themes like 'Liquid Glass', standard notification containers (`st.success`, `st.error`) can suffer from low contrast due to style inheritance. Additionally, technical-heavy interfaces (like AAMVA encoding) benefit significantly from localized tooltips to demystify technical acronyms without UI clutter.

**Action:** Always use CSS overrides to force high-contrast text (e.g., `#ffffff`) in `div[data-testid="stAlertContainer"]` for Streamlit apps with dark or transparent backgrounds. Implement the `help` parameter in input components to provide "on-demand" definitions for industry-specific terminology.
