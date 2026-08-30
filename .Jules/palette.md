## 2026-08-30 - Screen Reader Accessibility for Collapsed Streamlit Labels
**Learning:** In Streamlit, passing an empty string `""` to `st.selectbox` when using `label_visibility="collapsed"` prevents screen readers from announcing an accessible name. Passing a localized label string generates a valid `aria-label` attribute on the underlying combobox input without displaying visual text in the layout.
**Action:** Always provide a descriptive localized string as the first argument to `st.selectbox` or `st.text_input` even when `label_visibility="collapsed"` is enabled.
