# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-18 - Accessible Names for Streamlit Header Controls
**Learning:** Icon-only buttons (`st.button`) and visually-collapsed selectboxes (`st.selectbox` with `label_visibility="collapsed"`) in Streamlit require `help` text and valid localized labels respectively to provide screen readers with accessible names.
**Action:** Always provide localized `help` tooltips on icon-only buttons and non-empty `label` strings even when `label_visibility="collapsed"`.
