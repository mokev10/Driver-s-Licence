## 2026-08-27 - Streamlit Tooltip Contrast in Custom Dark Mode
**Learning:** Overriding global text colors (`p, span, label`) to white in custom Streamlit dark themes causes tooltip popup text (`div[data-testid="stTooltipContent"]`) to render white text on a default white background, making tooltips invisible.
**Action:** Explicitly target `div[data-testid="stTooltipContent"] p, div[data-testid="stTooltipContent"] span` in CSS to enforce dark text (`#111827`) on light tooltip popups.
