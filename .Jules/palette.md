## 2025-05-14 - [AAMVA Generator Accessibility & Contrast]
**Learning:** In highly customized Streamlit themes (like 'Liquid Glass'), default notification styles and label contrasts often fall below WCAG standards. Icon-only buttons in the header lack accessible names without explicit tooltips.
**Action:** Always use the `help` parameter for Streamlit icon buttons to provide ARIA-equivalent labels. Use targeted CSS (`div[data-testid="stNotification"] *`) to override internal Streamlit notification text colors for guaranteed high contrast.
