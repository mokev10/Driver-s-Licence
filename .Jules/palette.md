# Palette's Journal - UX & Accessibility Learnings

## 2026-10-13 - Accessible Selectbox Labels with Collapsed Visibility
**Learning:** Streamlit selectbox components with visually collapsed labels (`label_visibility="collapsed"`) still require a valid, non-empty localized string as their first parameter. Providing empty strings `""` prevents screen readers from computing a valid accessible name for the field.
**Action:** Always provide a descriptive, localized label parameter (e.g., `"Language / Langue"`) even when `label_visibility="collapsed"` is enabled.
