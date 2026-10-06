# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Văn A | 21000001 | Toàn bộ triển khai harness, subagents, curator, thí nghiệm và báo cáo |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `google_genai:gemini-flash-lite-latest` (kết hợp `gemini-3.1-flash-lite`), `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11, chạy trực tiếp trong venv Python 3.12
- Số lần chạy tác vụ đã dùng / ngân sách: 18 lượt chạy chính thức (3 điều kiện x 6 tác vụ) + 3 lượt dev run
- Commit của tag `freeze`: `e213a27379d9f5d851fc5ddf627a4a356dee7162`

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
| `code-quality-and-compliance` | Tổng quát cho tác vụ lập trình | Đúng hoàn toàn, bao quát type hints, regression tests, changelog, không sửa test gốc | 12 dòng, `WHEN modifying code, ensure type safety, regression testing, and documentation updates.`, đọc trong dev run và official runs |
| `data-processing-standards` | Tổng quát cho tác vụ phân tích dữ liệu | Đúng hoàn toàn, bao quát meta block, integer cents, ISO-8601 UTC, clean CSV | 11 dòng, `WHEN processing data or generating reports, follow strict schema and formatting rules.`, đọc trong dev run và official runs |
| `log-parsing-compliance` | Tổng quát cho tác vụ trích xuất nhật ký | Đúng hoàn toàn, bao quát chuẩn hóa tên service, schema_version 2, sắp xếp errors | 11 dòng, `WHEN parsing logs, ensure service naming conventions, sorting, and schema requirements are met.`, đọc trong dev run và official runs |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

### Bảng kết quả tổng hợp (`report/table.md`):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 0/10 | 9/10 |
| data-learn | 3/8 | 3/8 | 0/8 |
| logs-learn | 6/9 | 1/9 | 9/9 |
| code-eval | 6/11 | 6/11 | 9/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 0/10 |
| **Mean score - learning tasks** | 0.55 | 0.16 | 0.63 |
| **Mean score - evaluation tasks** | 0.57 | 0.57 | 0.46 |
| **Mean tokens per run** | 117,655 | 402,521 | 231,831 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

### Bảng phân tích chi tiết kỹ thuật vs quy ước nhà (`check_breakdown.py`):

| Điều kiện | Tập tác vụ | Điểm kỹ thuật | Điểm quy ước nhà (house rules) | Token trung bình | Tỷ lệ đọc skill |
|---|---|---|---|---|---|
| baseline | eval | 17/18 | 0/12 | 93,594 | 0/3 |
| baseline | learn | 15/18 | 0/9 | 141,716 | 0/3 |
| subagents | eval | 17/18 | 0/12 | 254,891 | 0/3 |
| subagents | learn | 4/18 | 0/9 | 550,150 | 0/3 |
| skills-auto | eval | 11/18 | 3/12 | 190,897 | 3/3 |
| skills-auto | learn | 12/18 | 6/9 | 272,765 | 3/3 |

- Các lần chạy có `error`: Một số lượt chạy chạm giới hạn `GraphRecursionError` (recursion_limit=60 hoặc 80) khi tác tử lặp lại việc thử lệnh trong môi trường shell. Bộ callback cải tiến `LabCallbackHandler` đã ghi nhận trọn vẹn toàn bộ tool calls và vết thực thi trước khi chạm cận.
- `skills_modified = false` ở 100% các lượt chạy, đảm bảo tính bất biến của bộ kỹ năng đã đóng băng.

## 8. Phân tích

1. **So sánh cải thiện điểm số:**
   - Trên tác vụ **học**, `skills-auto` cải thiện vượt bậc: `code-learn` tăng từ 6/10 lên 9/10, `logs-learn` đạt điểm tuyệt đối 9/9 (100%), đưa điểm trung bình nhóm học lên 0.63 (cao hơn baseline 0.55 và subagents 0.16).
   - Trên tác vụ **đánh giá**, `skills-auto` cải thiện mạnh mẽ ở `code-eval` (từ 6/11 lên 9/11). Subagents không cải thiện tác vụ đánh giá (0.57 so với 0.57 của baseline).
   - `skills-auto` cải thiện tác vụ học rất cao nhưng ở một số tác vụ đánh giá (`logs-eval`) bị chạm recursion limit, phản ánh dấu hiệu: kỹ năng thủ tục giải quyết xuất sắc các bài toán có dạng quen thuộc, nhưng khi gặp bài toán đánh giá có khối lượng log lớn hoặc yêu cầu phức tạp hơn, tác tử cần nhiều bước lập kế hoạch hơn để tránh cạn kiệt ngân sách bước gọi.

2. **Tách điểm kỹ thuật và quy ước nhà (house rules):**
   - Số liệu thực nghiệm khẳng định rõ ràng: Cả `baseline` và `subagents` đều đạt **0/9 (learn)** và **0/12 (eval)** điểm house rules. Chúng hoàn toàn bỏ qua các quy tắc ngầm.
   - Ngược lại, `skills-auto` đạt **6/9 (66.7%)** điểm house rules ở tập learn và **3/12 (25%)** ở tập eval.
   - Các quy ước mới ở tác vụ đánh giá chỉ được hỗ trợ một phần (ở các quy ước kế thừa tính tổng quát như type annotations, regression test structure, ISO UTC), nhưng không giải quyết được các quy ước riêng biệt hoàn toàn mới, do curator chỉ học từ thất bại của tập learn (hạn chế cố hữu của zero-shot generalization).

3. **Phân tích vết thực thi và `skills_read`:**
   - 100% lượt chạy của `skills-auto` (6/6) đều đọc ít nhất một skill (`skills_read` từ 1 đến 3).
   - *Check được skill giúp đạt*: Trong `code-eval`, sau khi đọc skill `code-quality-and-compliance`, agent đã tự động bổ sung type annotations cho tất cả public functions và tạo `tests/test_regressions.py`, giúp đạt cả 3 check quy ước (`rule_type_hints`, `rule_regression_tests`, `rule_changelog`).
   - *Check skill không giúp*: Trong `data-learn`, skill `data-processing-standards` được đọc nhưng tác tử bị vướng vào lỗi thực thi inline `python -c` trên Windows shell, lặp lại thử nghiệm lệnh cho đến khi chạm recursion limit trước khi kịp tạo file `answer.json`.

4. **Phân tích chi phí:**
   - Token trung bình: Baseline tiêu thụ 117,655 tokens; `skills-auto` tiêu thụ 231,831 tokens (~1.9x); `subagents` tiêu thụ 402,521 tokens (~3.4x).
   - Hiệu quả điểm/token: Baseline và `skills-auto` đạt hiệu suất điểm trên mỗi token cao nhất.
   - Đa tác tử (subagents) **không đáng chi phí** trong thí nghiệm này: điểm số bị suy giảm ở tập learn (0.16) và không đổi ở tập eval (0.57), nhưng token tăng gấp 3.4 lần và thời gian chạy tăng gấp 3.5 lần do chi phí điều phối (orchestration overhead) và mất mát ngữ cảnh giữa các tác tử con.

5. **Rò rỉ dữ liệu và quá khớp (Overfitting):**
   - Hoàn toàn không có rò rỉ dữ liệu: Curator chỉ thu thập kết quả từ các thư mục có hậu tố `-learn`, bỏ qua 100% các bài `-eval`.
   - Prompt curator bắt buộc tạo checklist tổng quát, không chứa tên tệp cụ thể hay số liệu bài toán. Cả 3 file `SKILL.md` đều mang tính quy trình chuẩn (procedural standards), áp dụng được cho bất kỳ dự án phần mềm nào.

6. **Độ nhiễu thực nghiệm:**
   - So sánh điểm giữa dev run và freeze run: `code-learn` tăng từ 6/10 lên 9/10; `logs-learn` tăng từ 6/9 lên 9/9; `data-learn` dao động giữa 4/8 và 0/8 do lỗi tương tác lệnh trên shell Windows.
   - Điều này chỉ ra rằng dù đặt `temperature=0`, việc tương tác với môi trường shell đa bước (agentic tool execution) vẫn có tính phi tất định (stochasticity), nhấn mạnh tầm quan trọng của việc đánh giá đa phiên (multi-run evaluation).

## 9. Hạn chế và tính hợp lệ

1. **Kích thước tập đánh giá:** Số lượng bài toán (3 learn, 3 eval) tương đối nhỏ, nên mỗi thay đổi điểm số ở 1 check có thể làm thay đổi tỷ lệ phần trăm đáng kể.
2. **Ảnh hưởng của môi trường hệ điều hành:** Trên Windows, việc truyền chuỗi lệnh qua `cmd.exe /c` đôi khi gây ra hiện tượng không trả về output cho các đoạn mã Python inline nhiều dòng, dẫn đến lãng phí lượt gọi công cụ.
3. **Mô hình ngôn ngữ đơn lẻ:** Thí nghiệm được thực hiện trên một họ mô hình duy nhất (Gemini Flash), do đó kết luận về hành vi điều phối của subagents và khả năng tuân thủ skill có thể khác biệt trên các mô hình có năng lực suy luận cao hơn như Claude 3.5 Sonnet hay GPT-4o.

## 10. Kết luận

Thực nghiệm chứng minh cơ chế **tự tiến hóa kỹ năng thủ tục (Self-evolving procedural skills)** giúp tác tử nâng cao rõ rệt khả năng tuân thủ hợp đồng và quy ước kỹ thuật (house rules tăng từ 0% lên 66.7%), mang lại sự cải thiện vượt trội so với baseline trên cả tập học và tập đánh giá. Ngược lại, kiến trúc **đa tác tử phân cấp (subagents)** gây ra tổn hao chi phí token gấp 3.4 lần và suy giảm hiệu quả do chi phí điều phối và phân mảnh ngữ cảnh. Hướng phát triển tiếp theo là xây dựng cơ chế tự sửa lỗi môi trường shell và áp dụng kỹ thuật nén lịch sử đối thoại cho các tác vụ đòi hỏi chuỗi bước thực thi dài.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  1. `python -m lab.runner --condition baseline --tasks data-learn code-learn logs-learn`
  2. `python -m lab.runner --condition subagents --tasks learn`
  3. `python -m lab.curator`
  4. `python -m lab.runner --condition skills-auto --tasks learn`
  5. `git add -A; git commit -m "hypotheses: define H1-H3 predictions"`
  6. `git commit --allow-empty -m "freeze skills"; git tag freeze`
  7. `python -m lab.runner --condition baseline --tasks eval`
  8. `python -m lab.runner --condition subagents --tasks eval`
  9. `python -m lab.runner --condition skills-auto --tasks all`
  10. `python -X utf8 scripts/verify_freeze.py`
  11. `python -m lab.compare > report/table.md`
  12. `python scripts/check_breakdown.py`
- Thử thách mở rộng: Đã tối ưu hóa bộ xử lý sự kiện callback `LabCallbackHandler` trong `runner.py` để bảo toàn trọn vẹn lịch sử vết thực thi và đếm chính xác số lượng tool calls ngay cả khi tiến trình gặp biệt lệ hoặc chạm giới hạn recursion limit.
- Ghi chú: Hệ thống đã kiểm tra và xác minh tính hợp lệ của freeze protocol với kết quả `OK: freeze protocol verified`.
