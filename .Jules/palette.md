# Palette's UX Journal

## 2026-08-09 - Accessible Streamlit Selectboxes with Collapsed Labels
**Learning:** In Streamlit, setting `label_visibility="collapsed"` hides the label from the visual layout but still uses the label text to generate correct accessible names and descriptions for assistive technologies (screen readers). Visually empty labels (like `""`) result in elements without proper ARIA/accessible names.
**Action:** Always provide a descriptive, localized title string as the label for selectboxes, even when `label_visibility` is configured as `"collapsed"`.

## 2026-08-09 - Contrast Consistency for Custom Streamlit Tooltips
**Learning:** Custom UI overrides (such as styling global text/paragragh colors) can render default tooltips unreadable if they have transparent or mismatched backgrounds. Explicitly targeting `div[data-testid="stTooltipContent"]` with specific background and border parameters guarantees high-contrast tooltip readability under any theme.
**Action:** Always pair custom component overrides with explicit `div[data-testid="stTooltipContent"]` CSS specifications, ensuring all curly braces are properly doubled inside Python f-string templates.
