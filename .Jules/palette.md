## 2025-05-15 - [Header Component Clipping]
**Learning:** Streamlit column weights need careful balancing when using components with varying widths (like a selectbox vs. an icon-only button). The initial [8, 1, 1] layout caused the language selector to clip its text.
**Action:** Use a more generous width for selectboxes in headers (e.g., [7, 1, 2]) and always verify responsiveness via screenshots.
