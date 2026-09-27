## 2026-09-27 - Accessible Name for Collapsed Streamlit Controls
**Learning:** In Streamlit, selectboxes and inputs with visually collapsed labels (`label_visibility="collapsed"`) still require a non-empty localized text label (e.g. `Select Language`) so that screen readers generate an accessible name rather than announcing an unlabelled field.
**Action:** Always provide descriptive localized label strings to Streamlit controls even when hiding them visually with `label_visibility="collapsed"`.
