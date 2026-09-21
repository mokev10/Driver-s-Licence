## 2026-09-21 - Accessible Names for Collapsed Streamlit Controls
**Learning:** Streamlit controls like `st.selectbox` using `label_visibility="collapsed"` still require a meaningful localized text label parameter (e.g., `"Language"`) rather than `""` so that screen readers generate an accessible accessible-name computation.
**Action:** Always provide a descriptive label string to Streamlit input components even when visually collapsing labels with `label_visibility="collapsed"`.
