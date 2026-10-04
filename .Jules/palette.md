## 2026-10-04 - Accessible Labels with Collapsed Visibility in Streamlit
**Learning:** In Streamlit, selectbox components with `label_visibility="collapsed"` still require a meaningful, non-empty label text string to ensure screen readers generate an accessible name for visually hidden labels.
**Action:** Always provide localized descriptive label text to `st.selectbox` even when setting `label_visibility="collapsed"`.
