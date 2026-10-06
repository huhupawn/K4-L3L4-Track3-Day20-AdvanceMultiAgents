"""GUIDE Phần 1 - Dựng tác tử (agent) bằng Deep Agents.

Pseudo-code: guides/pseudocode/01_agent.md
Kiểm tra:    pytest tests/test_02_agent.py
"""
import os
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend

from .model import make_model
from .subagents import get_subagents

# ---- CÓ SẴN, KHÔNG SỬA: system prompt dùng chung cho mọi sinh viên (để đường cơ sở so sánh được) ----
PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)
# --------------------------------------------------------------------------------------------------


def make_backend(sandbox: Path):
    """Tạo backend (môi trường thực thi) cho tác tử.

    Yêu cầu:
      - Thư mục gốc (root_dir) là `sandbox`; đường dẫn tương đối `workspace/...` và `skills/...`
        phải dùng được ở CẢ công cụ tệp lẫn shell (shell chạy với thư mục làm việc = `sandbox`).
      - Tác tử chạy được lệnh shell và gọi được `python` (cần đặt PATH).
      - KHÔNG chuyển biến môi trường của bạn vào shell của tác tử (khóa API không được lộ).
    """
    py_dir = str(Path(sys.executable).parent)
    if sys.platform == "win32":
        path_parts = [py_dir]
        for d in [
            r"C:\Program Files\Git\usr\bin",
            r"C:\Program Files\Git\bin",
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32"),
        ]:
            if Path(d).exists():
                path_parts.append(d)
        env = {
            "PATH": ";".join(path_parts),
            "HOME": str(sandbox),
            "PYTHONDONTWRITEBYTECODE": "1",
            "SystemRoot": os.environ.get("SystemRoot", r"C:\Windows"),
            "SystemDrive": os.environ.get("SystemDrive", "C:"),
            "ALLUSERSPROFILE": os.environ.get("ALLUSERSPROFILE", r"C:\ProgramData"),
            "ProgramData": os.environ.get("ProgramData", r"C:\ProgramData"),
            "TEMP": os.environ.get("TEMP", r"C:\Windows\Temp"),
            "TMP": os.environ.get("TMP", r"C:\Windows\Temp"),
        }
        if "COMSPEC" in os.environ:
            env["COMSPEC"] = os.environ["COMSPEC"]
        if "PATHEXT" in os.environ:
            env["PATHEXT"] = os.environ["PATHEXT"]
    else:
        env = {
            "PATH": f"{py_dir}:/usr/local/bin:/usr/bin:/bin",
            "HOME": str(sandbox),
            "PYTHONDONTWRITEBYTECODE": "1",
        }

    return LocalShellBackend(
        root_dir=sandbox,
        virtual_mode=True,
        inherit_env=False,
        env=env,
        timeout=120,
    )


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Tạo tác tử Deep Agents.

    Tham số:
      sandbox:    thư mục chứa `workspace/` (và `skills/` nếu có).
      mode:       "single"    -> tác tử mặc định (có subagent `general-purpose` sẵn của Deep Agents)
                  "subagents" -> thêm các subagent từ `get_subagents()` (nối PATHS_NOTE vào `system_prompt` của MỖI subagent,
                                 vì subagent không nhận BASE_PROMPT) và thêm SUBAGENTS_NOTE vào prompt chính
      use_skills: True -> nạp thư mục "/skills/" qua tham số `skills=` của create_deep_agent
                  và thêm SKILLS_NOTE vào prompt.
      model:      mô hình ngôn ngữ; None -> dùng `make_model()`.
    mode không hợp lệ -> ném ValueError.
    Trả về: đồ thị (graph) đã biên dịch, gọi bằng `.invoke({"messages": [...]})`.
    """
    if mode not in {"single", "subagents"}:
        raise ValueError(f"Unknown mode: {mode}")

    kwargs = {}
    prompt = BASE_PROMPT

    if mode == "subagents":
        kwargs["subagents"] = [
            {**sub, "system_prompt": sub["system_prompt"] + " " + PATHS_NOTE}
            for sub in get_subagents()
        ]
        prompt = prompt + SUBAGENTS_NOTE

    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt = prompt + SKILLS_NOTE

    if model is None:
        model = make_model()
        if hasattr(model, "_generate"):
            orig_generate = model._generate

            def safe_generate(*args, **kwargs):
                for attempt in range(6):
                    try:
                        return orig_generate(*args, **kwargs)
                    except Exception as exc:
                        err = str(exc)
                        if any(k in err for k in ("429", "RESOURCE_EXHAUSTED", "RateLimit", "503", "UNAVAILABLE", "high demand")):
                            import time
                            wait_s = 15 * (attempt + 1)
                            print(f"[Retry {err[:30]}] Waiting {wait_s}s before attempt {attempt + 2}...", flush=True)
                            time.sleep(wait_s)
                        else:
                            raise
                return orig_generate(*args, **kwargs)

            model._generate = safe_generate

    return create_deep_agent(
        model=model,
        system_prompt=prompt,
        backend=make_backend(sandbox),
        **kwargs,
    )
