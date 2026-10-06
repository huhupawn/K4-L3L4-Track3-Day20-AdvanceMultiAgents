---
name: log-parsing-compliance
description: WHEN parsing logs, ensure service naming conventions, sorting, and schema requirements are met.
---
- Normalize all service names to lowercase and replace hyphens with underscores (e.g., `payment-service` becomes `payment_service`).
- Ensure the final output object contains `"schema_version": 2` and `"generated_by": "log-triage"`.
- Sort the `errors` list primarily by `service` (alphabetical) and secondarily by `timestamp_utc` (ascending).
- When parsing timestamps, handle both 'Z' suffixes and numeric offsets by converting all entries to UTC.
- Aggregate repeat counts correctly by tracking the lines following a log entry that indicate repetition.
- Validate the final JSON structure against the required schema before finalizing the task.
