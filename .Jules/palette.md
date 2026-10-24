## 2026-10-24 - Streamlit Tooltip Contrast with Global CSS Rules
**Learning:** Global CSS rules targeting `p` or `span` tags with white text in Streamlit dark mode apps can bleed into Streamlit tooltips (`div[data-testid="stTooltipContent"]`), causing white-on-white unreadable text.
**Action:** Always add an explicit override targeting `div[data-testid="stTooltipContent"] p, div[data-testid="stTooltipContent"] span` with high-contrast text color when styling dark mode Streamlit apps.
