## 2025-05-18 - Tooltip text contrast in Streamlit dark mode
**Learning:** In Streamlit apps with custom dark-mode CSS (such as setting global 'p, span, label' colors to white or primary text), default tooltips with light backgrounds render tooltip text as white on white, rendering them invisible.
**Action:** When adding tooltips to Streamlit apps with aggressive global CSS overrides, explicitly override 'div[data-testid="stTooltipContent"] p' with an accessible dark font color.
