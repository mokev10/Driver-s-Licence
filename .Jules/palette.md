## 2026-05-17 - [AAMVA Technical Acronym Accessibility]
**Learning:** For specialized industry standard forms (like AAMVA), users may find technical acronyms (DCG, DAC, etc.) cryptic. Providing localized tooltips via the `help` parameter in Streamlit significantly improves accessibility and UX for non-expert users.
**Action:** Always look for technical or cryptic labels in specialized interfaces and suggest adding descriptive tooltips to bridge the knowledge gap.

## 2026-05-17 - [Streamlit Tooltip Customization]
**Learning:** Streamlit tooltip icons and content require specific CSS overrides (targeting `button[aria-label^="Help for"]` and `div[data-testid="stTooltipContent"]`) to maintain high contrast and readability in custom dark themes like 'Liquid Glass'.
**Action:** When implementing custom themes in Streamlit, explicitly style tooltips to ensure they don't inherit poor contrast from the base theme.
