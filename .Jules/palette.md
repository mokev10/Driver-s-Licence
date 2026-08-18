## 2026-08-18 - Streamlit Header Control Ratios and Selectbox Accessible Names
**Learning:** Streamlit `st.columns` default ratios can cause tight layout clipping of selectbox options on medium viewports (e.g. truncating "EN" to "E"), and `label_visibility="collapsed"` requires a valid string label to properly generate accessible names for screen readers.
**Action:** Always allocate sufficient column width (e.g., at least 1.5-1.7 ratio units) for header controls and supply localized `label` and `help` parameters even when `label_visibility="collapsed"`.
