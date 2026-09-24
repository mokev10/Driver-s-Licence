## 2026-09-24 - Accessible Names for Visually Collapsed Streamlit Controls
**Learning:** Streamlit controls rendered with `label_visibility="collapsed"` still require a non-empty localized text label so that screen readers generate an accessible name for accessibility trees.
**Action:** Always provide a descriptive localized label string even when visually collapsing labels with `label_visibility="collapsed"`.
