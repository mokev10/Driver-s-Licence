## 2026-09-11 - Streamlit Tooltip Contrast in Custom Dark Themes
**Learning:** Global CSS resets styling text tags (`p`, `span`, `label`) in Streamlit custom dark themes can render tooltip popups unreadable (e.g. white text on light default background).
**Action:** Always target `div[data-testid="stTooltipContent"]` explicitly in custom CSS to force matching background and text colors for tooltips.
