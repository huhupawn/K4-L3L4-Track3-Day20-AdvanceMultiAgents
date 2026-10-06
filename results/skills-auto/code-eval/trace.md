### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: read_file
{"file_path": "skills/code-quality-and-compliance/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-11 of 11 @@
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

### Tool call: glob
{"pattern": "**/*", "path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-312.pyc', '/workspace/bookings/__pycache__/billing.cpython-312.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-312.pyc', '/workspace/bookings/__pycache__/schedule.cpython-312.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-312.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "pytest workspace/tests"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\tmpvo_rhstz\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\..\OneDrive\Desktop\VinAI\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.21s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest workspace/tests"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\tmpvo_rhstz\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\..\OneDrive\Desktop\VinAI\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.21s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest workspace"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\tmpvo_rhstz\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\..\OneDrive\Desktop\VinAI\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.22s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest --import-mode=importlib workspace"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\tmpvo_rhstz\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\..\..\OneDrive\Desktop\VinAI\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.22s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest workspace/tests -o pythonpath=workspace"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace\tests\test_bookings.py FF.                                     [100%]

================================== FAILURES ===================================
______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..\..\..\..\OneDrive\Desktop\VinAI\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
workspace\bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
   

### Tool call: read_file
{"limit": 100, "file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: read_file
{"limit": 100, "file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 100}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 100}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: read_file
{"limit": 100, "file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 100}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: read_file
{"limit": 100, "file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: read_file
{"file_path": "skills/code-quality-and-compliance/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-11 of 11 @@
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

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\nfrom typing import Union\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n    # Check \"1h30m\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    \n    # Check \"2h\"\n    m = re.fullmatch(r\"(\\d+)h\", text)\n    if m:\n        return int(m.group(1)) * 60\n    \n    # Check \"45m\"\n    m = re.fullmatch(r\"(\\d+)m\", text)\n    if m:\n        return int(m.group(1))\n    \n    # Check \"1:30\"\n    m = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    \n    # Check bare number \"45\"\n    m = re.fullmatch(r\"(\\d+)\", text)\n    if m:\n        return int(m.group(1))\n    \n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: write_file
{"content": "\"\"\"Billing rules.\"\"\"\nfrom typing import Union\n\n\ndef billable_blocks(minutes: Union[int, float], block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if minutes == 0:\n        return 0\n    import math\n    return math.ceil(minutes / block)\n", "file_path": "workspace/bookings/billing.py"}

### Tool result
Updated file /workspace/bookings/billing.py

### Tool call: write_file
{"content": "\"\"\"Schedule helpers.\"\"\"\nfrom typing import List, Optional\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: List[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: str, slots: Optional[List[str]] = None) -> List[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        new_slots = []\n    else:\n        new_slots = list(slots)\n    new_slots.append(slot)\n    return new_slots\n", "file_path": "workspace/bookings/schedule.py"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: write_file
{"file_path": "workspace/bookings/calendar_export.py", "content": "\"\"\"Calendar export.\"\"\"\nfrom typing import Union\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n"}

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: write_file
{"file_path": "workspace/tests/test_regressions.py", "content": "\"\"\"Regression tests for bookings package.\"\"\"\nimport pytest\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot\nfrom bookings.timeutil import parse_duration\n\n\ndef test_parse_duration_all_formats():\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n    with pytest.raises(ValueError):\n        parse_duration(\"invalid\")\n\n\ndef test_billable_blocks_negative():\n    with pytest.raises(ValueError):\n        billable_blocks(-5)\n    assert billable_blocks(0) == 0\n    assert billable_blocks(16) == 2\n\n\ndef test_add_slot_no_shared_state():\n    res1 = add_slot(\"a\")\n    assert res1 == [\"a\"]\n    res2 = add_slot(\"b\")\n    assert res2 == [\"b\"]\n    assert add_slot(\"c\", [\"x\"]) == [\"x\", \"c\"]\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: edit_file
{"new_string": "## Unreleased\n- fix(parse_duration): support all documented duration formats (\"2h\", \"45m\", \"1:30\", \"45\") in addition to \"1h30m\"\n- fix(billable_blocks): correctly round up partial blocks and validate negative minutes with ValueError\n- fix(add_slot): prevent mutable default argument state sharing across function calls and add type annotations", "old_string": "## Unreleased", "file_path": "workspace/CHANGELOG.md"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "python -m pytest workspace/tests -o pythonpath=workspace"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\tmpvo_rhstz
plugins: anyio-4.15.1, langsmith-0.14.4
collected 6 items

workspace\tests\test_bookings.py ...                                     [ 50%]
workspace\tests\test_regressions.py ...                                  [100%]

============================== 6 passed in 0.05s ==============================

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'I have successfully fixed the issues in the `bookings` package so that all tests pass, docstring specifications are fully implemented, explicit type annotations are added for all public functions, and Acme\'s review bot conventions are followed.\n\n### Summary of Changes:\n- **`workspace/bookings/timeutil.py`**: Updated `parse_duration` to support all documented formats (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, `"45"`), handling whitespace and raising `ValueError` on invalid formats. Added type annotations.\n- **`workspace/bookings/billing.py`**: Fixed `billable_blocks` to correctly round up partial blocks using `math.ceil` and validate that negative minutes raise a `ValueError`. Added type annotations.\n- **`workspace/bookings/schedule.py`**: Fixed `add_slot` to avoid mutable default argument state sharing across separate calls and added type annotations.\n- **`workspace/bookings/calendar_export.py`**: Added explicit type annotations to `slot_end`.\n- **`workspace/tests/test_regressions.py`**: Created a new regression test file covering all fixed bugs without modifying existing test files.\n- **`workspace/CHANGELOG.md`**: Updated the changelog under `## Unreleased` with the required bullet points.', 'extras': {'signature': 'EmAKXgFpFH0TkyokNgvi26RvNNW19vSHFjURDtY2AfqgKsitSIuPsq4KTWjPR031NVn7ffg7WEEHUibZaB4VCoi/OaIIac34gkOCURTZnRU7HKYMR/mGbxQmC5iwvTB4WMY='}}]