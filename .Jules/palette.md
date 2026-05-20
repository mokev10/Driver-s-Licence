## 2024-05-20 - [AAMVA Tooltips Accessibility]
**Learning:** For forms involving specialized industry standards (like AAMVA), provide localized tooltips for technical acronyms to significantly improve accessibility for non-expert users without cluttering the UI.
**Action:** Always include technical field explanations in tooltips for domain-specific applications.

## 2024-05-20 - [Liquid Glass Tooltip Styling]
**Learning:** In the 'Liquid Glass' theme, Streamlit tooltip icons may have low visibility/contrast and require specific CSS overrides targeting `button[aria-label^="Help for"]` and `div[data-testid="stTooltipContent"]` for better accessibility and theme consistency.
**Action:** Use targeted CSS selectors to style Streamlit's built-in help icons and tooltip containers when working with custom dark themes.
