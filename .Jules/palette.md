## 2026-09-02 - Streamlit Collapsed Selectbox Accessible Names
**Learning:** Streamlit `st.selectbox` components with `label_visibility="collapsed"` still rely on a non-empty string label parameter to construct the accessible name (`aria-label` / `label`) for screen readers. Passing `""` results in an unlabelled form control.
**Action:** Always provide localized descriptive label text to `st.selectbox` even when `label_visibility="collapsed"` is used.
