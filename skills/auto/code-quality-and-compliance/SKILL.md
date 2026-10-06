---
name: code-quality-and-compliance
description: WHEN modifying code, ensure type safety, regression testing, and documentation updates.
---
- Before modifying existing code, verify if the task requires adding regression tests.
- If regression tests are required, create a new file `tests/test_regressions.py` and add at least one test function per bug fixed.
- Ensure all public functions (those not starting with `_`) have explicit type annotations for all parameters and return values.
- After completing fixes, update `CHANGELOG.md` under the `## Unreleased` heading.
- Add at least 3 bullet points in the format: `- fix(<function_name>): <short description>`.
- Never modify existing files in the `tests/` directory; only add new test files.
- Run the full test suite after changes to ensure no regressions were introduced.
