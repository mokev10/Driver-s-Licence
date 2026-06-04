## 2025-05-22 - Providing Context for Specialized Standards

**Learning:** For forms involving specialized industry standards (like AAMVA), providing localized tooltips for technical acronyms significantly improves accessibility for non-expert users without cluttering the UI. Users often know the data they need to enter (e.g., "Given Names") but may not recognize the corresponding technical code ("DAC").

**Action:** Always pair technical acronyms or industry-specific codes with descriptive, localized tooltips using the `help` parameter in Streamlit or ARIA descriptions in web frameworks.

## 2025-05-22 - Accessible Icon-Only Controls

**Learning:** Icon-only buttons (like theme toggles) are visually clean but inaccessible to screen readers and potentially confusing to new users without clear labels. Adding a `help` parameter in Streamlit not only provides a tooltip but also acts as an accessible label.

**Action:** Ensure all icon-only interactive elements have localized tooltips or ARIA labels to maintain both visual minimalism and accessibility.
