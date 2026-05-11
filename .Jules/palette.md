## 2025-05-15 - [AAMVA Interface Accessibility and Guidance]
**Learning:** Technical fields using cryptic acronyms (DCG, DAC, etc.) are non-intuitive. Form labels in dark 'Liquid Glass' themes need high contrast (rgba(255, 255, 255, 0.9) vs 0.6) for readability. Also, Streamlit selectboxes must have non-empty labels for a11y, even when visually collapsed.
**Action:** Always provide descriptive tooltips for technical fields using the 'help' parameter and ensure labels have sufficient color contrast in custom CSS blocks.
