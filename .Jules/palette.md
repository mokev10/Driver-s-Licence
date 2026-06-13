## 2025-05-14 - [Technical Tooltips for Industry Standards]
**Learning:** For forms involving specialized industry standards (like AAMVA), providing localized tooltips for technical acronyms significantly improves accessibility for non-expert users without cluttering the UI.
**Action:** Always check for industry-specific jargon and provide clear, localized explanations via tooltips or helper text.

## 2025-05-14 - [Aria Labels for Collapsed Controls]
**Learning:** Providing a non-empty string to the `label` parameter of `st.selectbox` in Streamlit, even when `label_visibility='collapsed'`, ensures the component generates a valid `aria-label` for the underlying input element, maintaining accessibility for screen readers while achieving a minimalist UI.
**Action:** Never use empty strings for labels even if they are collapsed; use descriptive localized labels to ensure ARIA compliance.
