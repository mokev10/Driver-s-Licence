## 2026-10-28 - Streamlit Tooltip Button CSS Selector & Collapsed Selectbox Accessibility

**Learning:** Passing `help` to Streamlit's `st.button` wraps the button in a `span.stTooltipIcon` element in the DOM, breaking direct child CSS selectors like `div.stButton > button`. Additionally, `st.selectbox` with `label_visibility="collapsed"` still requires a non-empty localized label string to provide an accessible name for screen readers.

**Action:** Use descendant CSS selectors (`div.stButton button`) when customizing button styling, and always provide localized label strings to collapsed Streamlit input controls.
