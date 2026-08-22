## 2026-08-22 - Screen Reader Accessibility for Collapsed Selectbox Labels
**Learning:** In Streamlit, using `st.selectbox("", ..., label_visibility="collapsed")` removes the accessible name for screen readers even when visually hidden. Providing a localized descriptive string as the label parameter while keeping `label_visibility="collapsed"` preserves visual design while maintaining full accessibility.
**Action:** Always supply a valid localized string label to `st.selectbox` components even when `label_visibility="collapsed"` is used.
