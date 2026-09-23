## 2026-09-23 - Accessibility Names for Collapsed Streamlit Labels
**Learning:** In Streamlit, controls with `label_visibility="collapsed"` still require a meaningful localized text label parameter so screen readers can properly compute accessible names and tooltips.
**Action:** Always provide localized non-empty label strings to `st.selectbox` and `st.button` components even when visually hiding labels via `label_visibility="collapsed"`.
