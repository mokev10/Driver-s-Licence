## 2025-05-15 - Technical Acronym Clarity via Tooltips
**Learning:** Users often struggle with cryptic AAMVA technical acronyms (DCG, DAC, DAQ) in forensic data synthesis tools. Streamlit's native `help` parameter provides a non-intrusive way to offer context without cluttering the UI.
**Action:** Always include localized tooltips for technical identifiers and use `format_func` in selectboxes to map technical values to human-readable labels.

## 2025-05-15 - Accessibility for Collapsed Labels
**Learning:** In Streamlit, setting `label_visibility="collapsed"` hides the label visually but the component still needs a non-empty `label` string to generate a valid `aria-label` for screen readers.
**Action:** Provide localized descriptive labels even when `label_visibility` is collapsed.
