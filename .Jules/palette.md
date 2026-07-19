## 2026-07-19 - Technical Field Clarity via Native Parameters
**Learning:** Technical field clarity in complex interfaces (like AAMVA) is best achieved using Streamlit's native `help` parameter rather than custom HTML tooltips. This maintains keyboard accessibility, screen reader compatibility, and consistent theme overrides without custom CSS hacks.
**Action:** Always use native Streamlit component parameters (such as `help` and non-empty `label` with `label_visibility="collapsed"`) to provide accessible names and helpful context.
