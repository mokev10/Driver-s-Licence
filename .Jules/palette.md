## 2026-10-21 - Accessible Names for Collapsed Streamlit Form Controls
**Learning:** In Streamlit, setting `label=""` on `st.selectbox` with `label_visibility="collapsed"` leaves screen readers without an accessible name.
**Action:** Always provide a descriptive localized string in `label` even when using `label_visibility="collapsed"`, and add `help` tooltips to icon-only buttons for screen-reader/hover clarity.
