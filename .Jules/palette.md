## 2026-07-29 - [Streamlit Accessible Controls]
**Learning:** In technical Streamlit interfaces, icon-only buttons (like theme toggle emojis) need clear visual/screen-reader labels to be fully accessible, and selectboxes with hidden label visibility still generate valid aria-labels if a non-empty label is supplied.
**Action:** Enhance the theme toggle button in `app.py` with an `help` tooltip that acts as a visual and accessible label, and provide clear names for form inputs.
