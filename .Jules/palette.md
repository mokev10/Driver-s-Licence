## 2025-05-20 - Streamlit Collapsed Label Accessibility
**Learning:** Streamlit selectboxes with visually collapsed labels (`label_visibility="collapsed"`) still require a valid non-empty text label parameter to serve as an accessible name for screen readers.
**Action:** Always provide a localized label string for Streamlit inputs even when `label_visibility="collapsed"` is specified.
