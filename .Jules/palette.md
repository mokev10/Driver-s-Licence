## 2026-09-08 - Streamlit Dark Theme Tooltip Styling and Collapsed Selectbox Accessibility
**Learning:** In Streamlit dark mode applications, global text rules like `p, span, label { color: white }` render text invisible inside light default tooltips (`div[data-testid="stTooltipContent"]`), requiring explicit CSS overrides. Additionally, collapsed selectbox controls still require valid localized labels for screen reader accessible names.
**Action:** Always target `div[data-testid="stTooltipContent"]` in custom dark mode CSS and provide localized label strings to collapsed selectbox controls.
