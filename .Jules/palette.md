## 2026-10-11 - Streamlit Tooltip Contrast Overrides
**Learning:** Global CSS rules targeting `p` or `span` elements (e.g. `color: var(--text-primary)`) force white text inside Streamlit tooltip popups (`div[data-testid="stTooltipContent"]`), causing low contrast or white-on-white text against default light tooltip backgrounds.
**Action:** Always add an explicit rule for `div[data-testid="stTooltipContent"] p, div[data-testid="stTooltipContent"] span` with high-contrast text color when overriding global text styles in Streamlit apps.
