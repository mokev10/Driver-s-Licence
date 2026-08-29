## 2026-08-29 - Streamlit Header Button & Tooltip Accessibility
**Learning:** Streamlit `st.button` with icon-only labels does not generate an accessible name unless the `help` parameter is provided. Furthermore, custom dark theme CSS rules can bleed into Streamlit tooltips unless `div[data-testid="stTooltipContent"]` is explicitly styled with proper background and text contrast.
**Action:** Always provide the `help` parameter on icon buttons for tooltips and screen reader accessibility, and explicitly style `div[data-testid="stTooltipContent"]` when defining custom Streamlit dark themes.
