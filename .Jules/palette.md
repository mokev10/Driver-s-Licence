## 2026-08-21 - Accessible Selectbox Labels in Streamlit
**Learning:** Streamlit selectboxes initialized with empty string `""` labels lack accessible names for screen readers even when `label_visibility="collapsed"`. Passing a localized string label with `label_visibility="collapsed"` creates proper HTML `<label>` markup for assistive technologies without disrupting the visual layout.
**Action:** Always provide descriptive localized labels to Streamlit input controls when using `label_visibility="collapsed"`.
