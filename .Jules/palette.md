## 2026-09-14 - Streamlit Selectbox Accessible Name with Collapsed Labels
**Learning:** Streamlit selectboxes configured with empty string labels `""` leave screen readers without an accessible name, even when visually hidden.
**Action:** Always provide a descriptive, localized label (such as `"Language"`) when using `label_visibility="collapsed"` in Streamlit selectboxes.
