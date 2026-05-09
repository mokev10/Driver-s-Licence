## 2025-05-14 - [Tooltip Accessibility in Custom Themes]
**Learning:** In Streamlit applications with custom CSS-injected themes (like "Liquid Glass"), default tooltips (`help` parameter) can suffer from poor contrast, appearing as illegible blocks if the background and text colors are not explicitly synchronized.
**Action:** Always apply high-contrast CSS overrides for `div[data-testid="stTooltipContent"]` when implementing tooltips in custom-themed Streamlit apps to ensure legibility across all color schemes.

## 2025-05-14 - [Clean Workspace Management]
**Learning:** Hybrid environments (Python/Streamlit + Node/Vite) are prone to including unintended build artifacts like `__pycache__` and `pnpm-lock.yaml` in PRs if the `.gitignore` is not strictly maintained.
**Action:** Explicitly exclude `__pycache__/`, `*.py[cod]`, and `*$py.class` in `.gitignore` and perform a manual cleanup of lock files before submission if the project scope is purely Python-focused.
