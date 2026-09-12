## 2026-09-12 - Streamlit Header Accessibility and Tooltip Contrast

**Learning:** Streamlit selectboxes with visually collapsed labels (`label_visibility="collapsed"`) still require a valid, non-empty localized label string to generate accessible screen-reader names in the DOM. Icon-only buttons (like theme toggles) require a `help` parameter to provide tooltips and accessible names. Additionally, custom dark CSS overrides must explicitly target `div[data-testid="stTooltipContent"]` to prevent white-on-white text in default Streamlit tooltip popups.

**Action:** Always provide descriptive localized label strings for collapsed selectboxes, supply `help` text for icon buttons, and explicitly style tooltip containers in custom dark themes.
