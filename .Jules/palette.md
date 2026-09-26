## 2026-09-26 - Accessible Screen Reader Names with Collapsed Streamlit Labels
**Learning:** In Streamlit, setting `label_visibility="collapsed"` visually hides the field label, but the label text string is still passed to the underlying HTML input component to form its accessible screen-reader name (`aria-label` or `<label>`). Using an empty string `""` as the label removes the accessible name for assistive technologies.
**Action:** Always provide a descriptive, localized string for Streamlit inputs even when `label_visibility="collapsed"` is used.
