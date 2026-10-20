## 2026-10-20 - Streamlit Selectbox Accessible Names
**Learning:** Streamlit selectbox components with visually collapsed labels (`label_visibility="collapsed"`) still require a valid, non-empty localized text label parameter so screen readers can render a proper accessible name (aria-label).
**Action:** Always provide meaningful localized text labels even when using `label_visibility="collapsed"`.
