
## 2025-05-22 - [AAMVA Tooltips & Header Accessibility]
**Learning:** In technical domains like AAMVA identity generation, localized tooltips significantly improve accessibility for non-expert users without cluttering the UI. Always ensure header controls have valid ARIA labels, especially when using collapsed labels in Streamlit.
**Action:** Use the `help` parameter in Streamlit components to provide context for technical acronyms and ensure `label_visibility='collapsed'` components still have descriptive label text for screen readers.
