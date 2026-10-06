---
name: data-processing-standards
description: WHEN processing data or generating reports, follow strict schema and formatting rules.
---
- If the task involves generating an `answer.json`, ensure it includes a `meta` block: `{"source": <filename>, "rows_in": <total_input_rows>, "rows_used": <processed_rows>}`.
- Convert all monetary values to integer cents (e.g., $10.50 -> 1050) before writing to JSON or CSV.
- When writing CSV files, ensure headers match the requested schema exactly.
- Format all timestamps as ISO-8601 UTC strings (`YYYY-MM-DDTHH:MM:SSZ`).
- Standardize categorical data (e.g., regions) to canonical spellings (e.g., "North", "South", "East", "West") by stripping whitespace and normalizing case.
- Verify that all calculations (revenue, counts) are performed on cleaned, unique data rows.
