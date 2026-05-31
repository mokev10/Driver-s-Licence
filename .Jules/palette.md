## 2025-05-31 - [Adding Tooltips for Technical AAMVA Fields]
**Learning:** For specialized industry tools (like AAMVA barcode generators), technical acronyms (DCG, DAC, etc.) can be opaque to non-expert users. Adding localized tooltips using Streamlit's `help` parameter significantly improves accessibility and self-documentation without cluttering the UI.
**Action:** Always provide descriptive tooltips for technical field codes in form-heavy interfaces.

## 2025-05-31 - [Streamlit Button Tooltips as Accessible Labels]
**Learning:** In Streamlit, icon-only buttons (like theme toggles) benefit from the `help` parameter not just as a tooltip for mouse users, but also as an accessible label that can be picked up by screen readers and testing tools (accessible via `aria-label` in the DOM).
**Action:** Use `help` on all icon-only or ambiguous buttons to ensure both visual and programmatic clarity.
