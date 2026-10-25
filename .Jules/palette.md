# Palette's Journal

## 2025-05-20 - Accessible Names for Collapsed Streamlit Labels
**Learning:** Streamlit components with `label_visibility="collapsed"` still require a meaningful, localized text label so screen readers can announce an accessible name for interactive elements.
**Action:** Always provide localized descriptive text for `st.selectbox` and `st.text_input` labels even when setting `label_visibility="collapsed"`.
