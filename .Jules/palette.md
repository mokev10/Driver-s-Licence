## 2026-07-23 - Streamlit Selectbox Label Accessibility
**Learning:** Collapsing selectbox labels in Streamlit can render elements nameless for screen readers if an empty string label is used. Providing a localized non-empty label text while keeping `label_visibility="collapsed"` generates a valid `aria-label` attribute on the underlying DOM element, keeping the UI accessible and visually clean.
**Action:** Always provide a non-empty localized label string to Streamlit components even when setting `label_visibility="collapsed"`.
