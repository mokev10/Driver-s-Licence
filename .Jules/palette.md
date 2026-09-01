## 2026-09-01 - Accessible name for collapsed Streamlit selects
**Learning:** Streamlit selectboxes with visually collapsed labels (`label_visibility="collapsed"`) still rely on `label` for generating the screen-reader accessible name. Leaving `label=""` produces empty accessible names.
**Action:** Always provide a localized label string even when `label_visibility="collapsed"` is used.
