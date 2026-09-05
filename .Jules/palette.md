## 2026-09-05 - Accessible Labels on Collapsed Streamlit Inputs
**Learning:** Streamlit selectboxes using `label_visibility="collapsed"` still require a meaningful, localized text string passed as the `label` parameter for screen readers to properly compute an accessible name (`aria-label`).
**Action:** Always provide a localized label string even when visually collapsing input labels in Streamlit components.
