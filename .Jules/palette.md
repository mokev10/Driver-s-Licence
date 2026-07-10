
## 2025-05-15 - [Streamlit Accessibility and Tooltip Verification]
**Learning:** In Streamlit, even when using `label_visibility='collapsed'` for an `st.selectbox`, providing a descriptive label is crucial as it populates the `aria-label` for screen readers. Additionally, native tooltips (`help` parameter) in Streamlit can be reliably verified in Playwright by targeting `button[aria-label^="Help for "]` and checking for `div[data-testid="stTooltipContent"]`.
**Action:** Always provide meaningful labels to input components regardless of their visibility setting, and use precise ARIA-based locators for verifying Streamlit-native UI enhancements.
