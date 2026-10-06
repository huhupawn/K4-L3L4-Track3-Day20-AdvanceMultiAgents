# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Văn A | 21000001 | Toàn bộ triển khai harness, subagents, curator, thí nghiệm và báo cáo |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `google_genai:gemini-3.1-flash-lite`, `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11, chạy trực tiếp trong venv Python 3.12
- Số lần chạy tác vụ đã dùng / ngân sách: 18 lượt chạy chính thức (3 điều kiện x 6 tác vụ)
- Commit của tag `freeze`: (Sẽ cập nhật sau khi gắn tag freeze)

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Subagents không đạt điểm cao hơn baseline trên tác vụ đánh giá (thậm chí thấp hơn hoặc hòa), nhưng tiêu tốn token gấp 3-5 lần và có nguy cơ chạm recursion limit do chi phí điều phối (orchestration overhead) và mất mát ngữ cảnh giữa các subagent.
- H2 (skills-auto so với baseline): Skills-auto đạt điểm số cao hơn rõ rệt so với baseline trên cả 3 tác vụ học (+15% đến +30%), đặc biệt giải quyết triệt để các lỗi vi phạm hợp đồng (rule_*) nhờ các hướng dẫn thủ tục dạng checklist được curator trích xuất.
- H3 (tác vụ học so với tác vụ đánh giá): Skills-auto có khả năng khái quát hóa (generalization) một phần trên tác vụ đánh giá: cải thiện đáng kể ở các quy ước định dạng chung (ISO-8601 UTC, kiểu cents, type hints, chuẩn hóa tên service), nhưng sẽ không giải quyết được các quy ước riêng biệt hoặc logic nghiệp vụ hoàn toàn mới của tác vụ đánh giá.

## 3. Làm quen Deep Agents (Phần 0.3)

1. `LocalShellBackend` thiết lập môi trường thực thi cách ly trong thư mục sandbox ảo với `inherit_env=False`, chỉ chuyển các biến môi trường thiết yếu tối thiểu, ngăn chặn hoàn toàn việc rò rỉ khóa API hoặc can thiệp ra ngoài hệ thống chủ.
2. Thư mục `skills/` nạp qua tham số `skills=` vào Deep Agents tạo prompt chỉ dẫn và danh sách kỹ năng cho agent đọc khi cần qua tool `read_file`. Khi tác tử nhận nhiệm vụ, nó đọc danh sách tệp `SKILL.md` để áp dụng quy trình chuẩn trước khi hành động.
3. Subagents được kích hoạt thông qua công cụ `task`, cho phép tác tử chính phân rã bài toán và ủy quyền cho các tác tử chuyên biệt (`explorer`, `implementer`, `reviewer`) hoạt động với prompt hệ thống độc lập.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| data-learn | north_q1_revenue | C | `north_q1_revenue: wrong value (got 2186.13)` do parse sai timezone offset hoặc lọc Q1 |
| data-learn | north_q1_orders | C | `north_q1_orders: wrong value (got 5)` do lọc sai số lượng đơn hàng quý 1 |
| data-learn | rule_money_in_cents | B, D | `RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)` |
| data-learn | rule_meta_block | B | `RULE: answer.json has an object meta = {"source": ..., "rows_in": ..., "rows_used": ...}` |
| data-learn | rule_clean_csv | B | `RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents...` |
| code-learn | tests_not_modified | E, A | `the original files in tests/ must not be modified (new test files are allowed)` |
| code-learn | rule_type_hints | B | `RULE: every public function... has type annotations on all parameters and on the return value` |
| code-learn | rule_regression_tests | B | `RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3)` |
| code-learn | rule_changelog | B | `RULE: record each fix in CHANGELOG.md under ## Unreleased as bullet - fix(<function>): <desc>` |
| logs-learn | rule_service_names | B, D | `RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service)` |
| logs-learn | rule_sorted_errors | B | `RULE: errors is sorted by service, then by timestamp_utc, ascending` |
| logs-learn | rule_schema_header | B | `RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage"` |

Nhận xét: Nhóm lỗi B (Quên quy tắc ngầm / hợp đồng) chiếm đa số tuyệt đối (8/12 lỗi, ~67%), theo sau là nhóm C (Xử lý ngoại lệ / corner case) và D (Định dạng kiểu dữ liệu). Skill dạng procedural checklist hoàn toàn có thể phòng ngừa triệt để nhóm B và D vì các quy tắc này có thể kiểm tra từng bước theo danh sách trước khi nộp kết quả.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa:
  - `explorer`: Khám phá cấu trúc tệp, phân tích README, đọc hiểu dữ liệu ban đầu.
  - `implementer`: Lập trình, sửa mã nguồn, viết kịch bản biến đổi dữ liệu.
  - `reviewer`: Chạy kiểm thử pytest, kiểm tra sự tuân thủ các quy tắc và định dạng đầu ra.
- `subagent_calls` ở từng tác vụ và nhận xét:
  - `logs-learn`: `subagent_calls = 1`, hoàn thành và đạt 1/9 check.
  - `data-learn` và `code-learn`: Các subagent trao đổi nhiều lượt, đạt điểm tương đương hoặc thấp hơn baseline nhưng chạm giới hạn `recursion_limit` 60.
- Thông tin thiếu hoặc thừa khi giao việc: Tác tử chính truyền lại toàn bộ chỉ dẫn nhưng subagent thiếu ngữ cảnh đầy đủ về toàn bộ các quy tắc hợp đồng ngầm, dẫn đến việc subagent tập trung giải quyết logic cơ bản mà bỏ quên kiểm tra quy ước.
- Ảnh hưởng đến token và thời gian: Token tiêu thụ tăng vọt gấp 3-5 lần (data-learn: 204k lên 1.19M tokens; logs-learn: 52k lên 283k tokens). Thời gian chạy tăng 2-4 lần do chi phí gọi LLM đa tầng và đồng bộ kết quả.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator: 1 lần. Số skill bị xóa: 0 (cả 3 skill đều vượt qua `validate_skill()` ngay lần đầu).

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-quality-and-compliance` | Tổng quát cho tác vụ lập trình | Đúng hoàn toàn, bao quát type hints, regression tests, changelog, không sửa test gốc | 12 dòng, `WHEN modifying code, ensure type safety, regression testing, and documentation updates.`, đọc trong dev run |
| `data-processing-standards` | Tổng quát cho tác vụ phân tích dữ liệu | Đúng hoàn toàn, bao quát meta block, integer cents, ISO-8601 UTC, clean CSV | 11 dòng, `WHEN processing data or generating reports, follow strict schema and formatting rules.`, đọc trong dev run |
| `log-parsing-compliance` | Tổng quát cho tác vụ trích xuất nhật ký | Đúng hoàn toàn, bao quát chuẩn hóa tên service, schema_version 2, sắp xếp errors | 11 dòng, `WHEN parsing logs, ensure service naming conventions, sorting, and schema requirements are met.`, đọc trong dev run |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

(Sẽ cập nhật sau khi hoàn thành đánh giá ở Bước 4.2)

## 8. Phân tích

(Sẽ hoàn thiện sau khi có bảng tổng hợp kết quả)

## 9. Hạn chế và tính hợp lệ

1. Số lượng tác vụ hạn chế (3 learn, 3 eval) khiến các chỉ số thống kê có độ lệch chuẩn nhất định.
2. Mỗi tác vụ chỉ chạy 1 lần duy nhất trên mỗi điều kiện để tiết kiệm chi phí, có thể chịu ảnh hưởng bởi tính ngẫu nhiên của LLM dù nhiệt độ đã đặt về 0.
3. Các quy ước hợp đồng do người thiết kế bài kiểm tra đặt ra có tính nhân tạo, dù mô phỏng sát các quy chuẩn kỹ thuật trong các dự án phần mềm thực tế.

## 10. Kết luận

(Sẽ hoàn thiện sau khi có bảng tổng hợp kết quả)

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  - `python -m lab.runner --condition baseline --tasks data-learn code-learn logs-learn`
  - `python -m lab.runner --condition subagents --tasks learn`
  - `python -m lab.curator`
  - `python -m lab.runner --condition skills-auto --tasks learn`
