## 2025-05-22 - Localized Technical Acronym Clarity
**Learning:** Providing localized tooltips for industry-specific technical acronyms (AAMVA codes like DCG, DAC) significantly lowers the cognitive barrier for non-expert users while keeping the UI clean. Streamlit's `help` parameter is an effective way to implement this without requiring custom popovers.
**Action:** Always check for technical shorthand in forms and provide descriptive tooltips using the `help` parameter, ensuring they are included in the app's localization dictionary.
