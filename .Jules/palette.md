## 2026-09-18 - Streamlit Collapsed Label Accessibility and Tooltip Contrast
**Learning:** In Streamlit, selectboxes with `label_visibility="collapsed"` still require a meaningful localized text label to populate the accessible name for screen readers. Additionally, global CSS overrides in dark mode can make tooltips illegible unless `div[data-testid="stTooltipContent"]` is explicitly styled with contrast rules.
**Action:** Always provide descriptive localized labels for collapsed form fields and explicitly style `div[data-testid="stTooltipContent"]` in custom Streamlit CSS.
