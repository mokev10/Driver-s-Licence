## 2025-05-15 - Improving Technical Field Clarity with Tooltips
**Learning:** In technical applications like AAMVA generators, standard acronyms (DCG, DAC, etc.) can be cryptic for non-expert users. Using Streamlit's native 'help' parameter provides a non-intrusive way to offer context without cluttering the UI.
**Action:** Always provide descriptive tooltips for industry-specific technical codes to ensure the interface remains accessible to a broader audience.

## 2025-05-15 - Enhancing Gender Selector Usability
**Learning:** While backend systems often require technical codes (e.g., '1' for Male, '2' for Female), displaying these directly in the UI is poor UX. Streamlit's 'format_func' allows mapping technical values to localized, human-readable labels.
**Action:** Use 'format_func' to localize and clarify selectbox options while preserving the required underlying technical data format.
