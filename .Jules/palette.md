## 2025-05-15 - Tooltip Clarity for Technical Acronyms
**Learning:** Technical AAMVA codes like DCG, DAC, and DBB are cryptic for non-expert users. Using Streamlit's native `help` parameter to provide localized tooltips significantly improves the clarity of the interface without adding visual noise or violating CSS constraints.
**Action:** Prioritize providing tooltips for all industry-specific technical codes in forms to ensure the UI remains accessible to a broader audience.

## 2025-05-15 - Strict CSS Boundaries in Liquid Glass Theme
**Learning:** Custom CSS to fix tooltip visibility in the Liquid Glass theme was explicitly rejected in previous iterations. Accessibility must be achieved through native component features like `help` and `label` rather than custom style overrides.
**Action:** Stick to native Streamlit parameters (`help`, `label`, `label_visibility`) for accessibility improvements and avoid injecting custom CSS for component-level styling.
