## 2026-10-01 - Dark Theme Streamlit Tooltip Contrast Fix
**Learning:** Streamlit custom dark-mode CSS overrides on global text elements (`p`, `span`, `label`) can cause tooltips rendered in `div[data-testid="stTooltipContent"]` to display white text on light backgrounds or unstyled containers.
**Action:** Explicitly style `div[data-testid="stTooltipContent"]` with dark background and white text when applying custom Streamlit CSS themes.
