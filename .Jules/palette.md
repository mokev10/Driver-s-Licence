## 2026-10-14 - Streamlit Selectbox Accessible Names with Collapsed Labels
**Learning:** Setting `label_visibility="collapsed"` on a Streamlit `st.selectbox` visually hides the widget label, but passing a non-empty string label (e.g. `Language`) ensures Streamlit auto-generates `aria-label="Language"` on the underlying HTML combobox input for screen readers. Leaving the string empty (`""`) leaves screen reader users without an accessible name.
**Action:** Always provide a non-empty, localized string label to `st.selectbox` even when `label_visibility="collapsed"`.
