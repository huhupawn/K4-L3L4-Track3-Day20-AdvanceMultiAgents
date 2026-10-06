"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when you need to inspect or explore the workspace, understand the project structure, "
                "read documentation, schema, log files, or data samples without modifying anything. "
                "The explorer investigates and reports facts."
            ),
            "system_prompt": (
                "You are an exploration and analysis subagent. Your role is to examine files, read logs, "
                "schemas, docstrings, or data samples in the workspace and provide a clear, factual report. "
                "Do NOT make changes to any files; only read and report your findings."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when you need to implement changes: writing or editing source code, creating scripts, "
                "transforming data files, or running tests and shell commands to accomplish the required tasks."
            ),
            "system_prompt": (
                "You are an implementation subagent. Your role is to write or edit code, run test scripts, "
                "process data according to specific instructions, and report the results and any errors encountered."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when you need an independent verification of completed work, checking output files, "
                "test passes, schemas, formatting rules, and edge cases against instructions before finishing."
            ),
            "system_prompt": (
                "You are a reviewer subagent. Your role is to independently verify that generated or modified "
                "files strictly satisfy all instructions, tests, and formatting conventions. "
                "Do NOT edit files; check the workspace thoroughly and report whether requirements are met."
            ),
        },
    ]
