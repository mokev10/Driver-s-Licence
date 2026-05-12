## 2025-05-12 - Improving AAMVA field clarity with tooltips

**Learning:** Technical acronyms (DCG, DAC, etc.) are often cryptic for general users. Using Streamlit's `help` parameter provides an accessible way to offer definitions without cluttering the UI.
**Action:** Always check for technical shorthand in forms and provide user-friendly tooltips using `help` in Streamlit or ARIA-labels in React.

## 2025-05-12 - Accessibility for icon-only buttons

**Learning:** Icon-only buttons lack inherent descriptive text for screen readers. The `help` parameter in Streamlit acts as an accessible label.
**Action:** Use the `help` parameter for all icon-only buttons to ensure they are accessible and provide context on hover.
