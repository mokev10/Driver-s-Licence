## 2026-09-03 - Accessible Labels & Column Ratios for Header Controls
**Learning:** In Streamlit, selectboxes with `label_visibility="collapsed"` still require a valid localized text label to generate correct screen-reader accessible names. Additionally, tight header column weights (e.g. `[8, 1, 1]`) can clip selectbox text on standard viewports.
**Action:** Always provide a descriptive localized label even when collapsing it visually, and ensure column allocations account for selectbox chevrons (e.g. `1.7` minimum weight).
