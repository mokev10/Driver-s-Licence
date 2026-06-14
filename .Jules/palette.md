## 2025-05-15 - Improving Accessibility in Specialized Data Tools
**Learning:** For specialized forms (like AAMVA standards), technical codes are confusing for non-expert users. Localized tooltips (`help` in Streamlit) significantly improve UX without cluttering the UI. Providing a non-empty label to `st.selectbox` even if `label_visibility="collapsed"` ensures it has a valid aria-label for screen readers.
**Action:** Always provide technical explanations for industry-specific acronyms and ensure accessibility labels are present on all interactive controls.
