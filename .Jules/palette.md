## 2026-08-16 - Streamlit Collapsed Selectbox Accessible Labels
**Learning:** In Streamlit, calling `st.selectbox("", ..., label_visibility="collapsed")` removes the accessible name for assistive technology (screen readers), making the form element non-compliant with standard accessibility rules.
**Action:** Always provide a meaningful localized label string to `st.selectbox` even when `label_visibility="collapsed"` is used.
