# Palette Journal

## 2025-05-18 - Streamlit Header Control Accessibility and Tooltip Contrast
**Learning:** In Streamlit apps with custom dark theme CSS overrides (`p, span, label { color: var(--text-primary) !important; }`), native tooltips (`stTooltipContent`) inherit white text on an un-themed white tooltip background, making tooltip contents invisible. Furthermore, passing an empty label `""` to `st.selectbox` creates an unlabeled combobox accessible tree entry, while narrow column ratios (e.g. `[8, 1, 1]`) cause the 2-letter language code to be clipped ("E ˅").
**Action:** Always provide an explicit localized label when using `label_visibility="collapsed"` so assistive technologies receive an accessible name, give compact header selectboxes adequate column allocation (at least 1.8 ratio), and explicitly scope `div[data-testid="stTooltipContent"]` text color to dark to avoid white-on-white contrast regressions.
