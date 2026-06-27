## 2026-06-27 - Streamlit Tooltip Accessibility & Verification
**Learning:** In Streamlit, adding a `help` parameter to components like `st.text_input` or `st.button` doesn't just add a hover title; it renders a separate help icon button with an `aria-label` like "Help for [Label Text]". This button triggers the `stTooltipContent` div.
**Action:** When verifying tooltips in Playwright for Streamlit apps, target these help buttons specifically using `page.locator('button[aria-label^="Help for"]')` to trigger and verify tooltip visibility.
