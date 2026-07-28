# Palette's UX Journal

## 2026-07-28 - Visually Collapsed Labels & Icon-Only Controls in Streamlit
**Learning:** Streamlit components with visually collapsed labels (e.g., `label_visibility="collapsed"`) still generate accessible labels for assistive technologies if a non-empty `label` string is provided. For icon-only button elements like a theme toggle, `help` tooltips serve as a robust accessible name fallback in Streamlit's rendering layer.
**Action:** Always provide descriptive, localized text for `label` parameters even when visually hidden, and add `help` tooltips to icon-only buttons to ensure keyboard and screen-reader accessibility.
