## 2025-05-18 - Accessible Names for Visually Collapsed Selectboxes
**Learning:** In Streamlit, selectbox components with `label_visibility="collapsed"` still require a non-empty, localized string label so that screen readers can convey a proper accessible name (e.g. "Select language" / "Sélectionner la langue") rather than an empty element name.
**Action:** Always provide a clear, localized label to Streamlit input widgets even when `label_visibility="collapsed"`.
