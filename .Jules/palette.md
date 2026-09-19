## 2026-09-19 - Streamlit Tooltip Contrast in Custom Dark Mode

**Learning:** When using custom CSS in Streamlit dark mode apps that sets default text colors (`p, span, label`) to white, tooltips rendered in `div[data-testid="stTooltipContent"]` can become unreadable if the container background remains light or unstyled.
**Action:** Explicitly style `div[data-testid="stTooltipContent"]` and its child elements in custom CSS with appropriate background and text colors to guarantee high contrast.
