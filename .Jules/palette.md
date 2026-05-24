## 2025-05-22 - [Localized Tooltips for Technical Acronyms]
**Learning:** For forms involving specialized industry standards (like AAMVA), provide localized tooltips for technical acronyms to significantly improve accessibility for non-expert users without cluttering the UI.
**Action:** Always check for technical jargon in forms and implement the `help` parameter in Streamlit components to provide on-demand explanations.

## 2025-05-22 - [Build Artifact Hygiene]
**Learning:** Streamlit and Python execution can generate `__pycache__` and other build artifacts that may not be covered by a default `.gitignore`.
**Action:** Be extremely vigilant about unstaged/untracked files before committing. Explicitly exclude binary/compiled files from the PR to maintain repository health.
