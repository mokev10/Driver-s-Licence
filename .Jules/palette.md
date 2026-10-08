## 2026-10-08 - Explicit Tooltip Styling for Streamlit Dark Themes
**Learning:** Global CSS rules targeting generic inline/text elements (`p, span, label`) in custom Streamlit themes can inadvertently override hover tooltip text color inside `div[data-testid="stTooltipContent"]`, resulting in unreadable white-on-white tooltip text.
**Action:** Always explicitly define dark theme styling for `div[data-testid="stTooltipContent"]` in custom Streamlit CSS templates, taking care to double all curly braces (`{{` and `}}`) inside Python f-strings.
