# Palette's Journal

## 2025-05-15 - Accessible Alt Text for Dynamic Jurisdiction Flag
**Learning:** In Streamlit custom HTML components rendered via `st.markdown(..., unsafe_allow_html=True)`, dynamic imagery like jurisdiction flag icons often omit the `alt` attribute. This leaves screen-reader users without context for visual country indicators.
**Action:** Always provide descriptive and dynamic `alt` attributes (e.g. `alt="{country_choice} flag"`) on custom rendered `<img>` elements within Streamlit cards.
