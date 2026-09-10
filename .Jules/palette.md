## 2025-05-18 - Streamlit Tooltip Contrast and Visually Collapsed Selectbox Accessibility
**Learning:** In Streamlit apps with custom dark theme CSS overrides, default tooltips can have unreadable low contrast unless explicitly styled via `div[data-testid="stTooltipContent"]`. Additionally, `st.selectbox` with `label_visibility="collapsed"` still requires a descriptive, localized text label so screen readers announce its purpose accurately.
**Action:** Always provide meaningful localized labels for collapsed form inputs and explicitly target `div[data-testid="stTooltipContent"]` in theme CSS.
