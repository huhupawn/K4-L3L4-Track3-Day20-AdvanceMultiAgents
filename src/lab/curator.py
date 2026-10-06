"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import json
import re
from pathlib import Path

from .tasks import ROOT, eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    if out_dir is None:
        out_dir = ROOT / "skills" / "auto"
    out_dir = Path(out_dir)

    results_path = Path(results_dir) / source_condition
    runs = []
    for run_file in sorted(results_path.glob("*/run.json")):
        r = json.loads(run_file.read_text(encoding="utf-8"))
        if r.get("role") != "learn":
            continue

        failed_checks = []
        for c in r.get("checks", []):
            if not c.get("passed", False):
                failed_checks.append((c.get("name", ""), c.get("detail", "")))

        if not failed_checks:
            continue

        trace_file = run_file.parent / "trace.md"
        trace_text = ""
        if trace_file.exists():
            full_trace = trace_file.read_text(encoding="utf-8")
            trace_text = full_trace[-6000:]

        runs.append({
            "task": r.get("task", run_file.parent.name),
            "failed": failed_checks,
            "trace": trace_text,
        })

    if not runs:
        print("Warning: no failed checks in learning tasks.")
        return []

    prompt_lines = [
        "You write SKILL documentation for a software engineering and data analysis agent.",
        "Below are the failed checks (check name and review bot feedback) and execution traces from previous learning runs.",
        f"Identify the common procedural patterns and write up to {max_skills} concise skills to prevent these failures on NEW tasks of similar types.",
        "",
        "Rules:",
        "- Skills must be general: do not mention specific task IDs, task-specific file names, answers, or exact numbers.",
        "- Each skill must have YAML frontmatter with `name` (lowercase, numbers, hyphens only, max 64 chars) and `description` (one sentence: WHEN to use it), followed by up to 40 lines of imperative instructions (checklists work best).",
        "- Exact output format:",
        "=== SKILL: <name> ===",
        "---",
        "name: <name>",
        "description: <when to use>",
        "---",
        "<content>",
        "=== END ===",
        "",
        "Previous learning task failures and traces:",
    ]
    for run in runs:
        prompt_lines.append(f"\nTask: {run['task']}")
        prompt_lines.append("Failed checks:")
        for name, detail in run["failed"]:
            prompt_lines.append(f"  - Check: {name}")
            if detail:
                prompt_lines.append(f"    Feedback: {detail}")
        if run["trace"]:
            prompt_lines.append(f"Trace summary:\n{run['trace']}")

    prompt = "\n".join(prompt_lines)

    if model is None:
        from .model import make_model
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

    reply_content = model.invoke(prompt).content
    if isinstance(reply_content, list):
        reply_str = "".join(
            (part.get("text", "") if isinstance(part, dict) else str(part))
            for part in reply_content
        )
    else:
        reply_str = str(reply_content)
    blocks = parse_skill_blocks(reply_str)

    written = []
    for name, text in blocks:
        if len(written) >= max_skills:
            break
        problems = validate_skill(text, expected_name=name)
        if problems:
            continue
        skill_file = out_dir / name / "SKILL.md"
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(text.strip() + "\n", encoding="utf-8")
        written.append(skill_file)

    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
