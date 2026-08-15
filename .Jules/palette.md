## 2026-08-15 - Streamlit Tooltip Contrast and Accessible Names
**Learning:** Icon-only buttons and collapsed selectboxes in Streamlit lack accessible names unless provided with explicit localized `help` and `label` attributes. Additionally, custom dark theme styles require targeting `div[data-testid="stTooltipContent"]` to maintain sufficient contrast.
**Action:** Always provide localized `help` tooltips and `label` attributes on header controls, and override Streamlit tooltip CSS to match theme palette colors.
