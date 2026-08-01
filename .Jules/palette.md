## 2026-08-01 - [Streamlit Selectbox Accessible Names]
**Learning:** In Streamlit, selectbox components with visually collapsed labels (via `label_visibility="collapsed"`) still require a valid, non-empty localized text label. Leaving the label string as empty results in form inputs without accessible names, violating accessibility guidelines (WCAG 2.1) and making elements confusing for screen readers.
**Action:** Always provide a meaningful localized label string to the label argument of `st.selectbox` even when configuring its layout behavior with `label_visibility="collapsed"`.
