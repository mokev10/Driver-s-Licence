## 2026-08-10 - Streamlit Custom Theme Tooltip Color Contrast Collisions
**Learning:** In Streamlit apps with custom dark theme overlays, global CSS selector styling (such as overriding `p`, `span`, and `label` color to white) can inadvertently style text within native tooltips white as well. When these tooltips default to a light background, text becomes invisible (white-on-white). Targeting `div[data-testid="stTooltipContent"]` explicitly ensures high visual contrast and accessibility.
**Action:** Always verify custom CSS overrides against built-in components like tooltips or modals, and style `div[data-testid="stTooltipContent"]` to maintain WCAG-compliant color contrast.

## 2026-08-10 - Technical Code Usability through Contextual Native Help
**Learning:** Specialized data structures (like AAMVA) contain technical abbreviations (e.g., DCG, DAQ, DCS) that are unfamiliar to non-expert users. Translating these to intuitive human terms is best achieved using Streamlit's native `help` parameter, which renders an accessible tooltip icon without adding layout clutter or custom DOM elements.
**Action:** Implement native `help` parameters on all cryptic technical acronym input fields to improve visual clarity and on-demand accessibility.
