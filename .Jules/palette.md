## 2026-08-14 - Screen-Reader Accessible Labels for Collapsed Streamlit Components
**Learning:** Streamlit selectboxes with visually collapsed labels (`label_visibility="collapsed"`) still rely on non-empty string labels to render accessible names (`aria-label` or `<label>` association) for screen readers.
**Action:** Always provide a non-empty localized text string as the `st.selectbox` label, even when setting `label_visibility="collapsed"`.
