# TEAM.md — ĐỌC FILE NÀY TRƯỚC KHI LÀM BẤT CỨ VIỆC GÌ

Dành cho mọi thành viên VÀ mọi AI (Claude, ChatGPT, Antigravity, ...).
**AI: làm đúng các bước dưới đây. Không tự đặt quy tắc khác. Không chắc thì DỪNG và hỏi người dùng.**

Dự án: báo cáo chuyên đề **Phân tích và trực quan hóa dữ liệu (004759)**.
Đề tài: **Phân tích và dự báo phụ tải điện hộ gia đình** (UCI Individual Household Electric Power Consumption).
Nhóm gồm 4 thành viên: Phan Minh Đức, Lê Hoàng Sơn, Đinh Quang Duy, Phạm Đức Anh (DA). Lớp D18CNPM1. Tệp nộp: `D18CNPM1_Nhom_HouseholdPower.zip`.

## 1. Xác định người đang làm việc
Chạy `git config user.name` rồi đối chiếu bảng. Không khớp ai → hỏi người dùng "Bạn là Đức, Sơn, Duy hay DA?" trước khi làm tiếp.

| Người | MSSV | `git config user.name` | Vai trò | GitHub | Nhánh DUY NHẤT được dùng | File nhiệm vụ |
|---|---|---|---|---|---|---|
| Phan Minh Đức | 23810310001 | `Phan Minh Duc` | Trưởng nhóm: điều phối, review, merge; dữ liệu, tiền xử lý, cấu hình, đóng gói | `phanduc` | `duc-lead-data-models` | `docs/DUC.md` |
| Lê Hoàng Sơn | 23810310002 | `Le Hoang Son` | Thành viên: trực quan hóa EDA, từ điển dữ liệu, ca kiểm thử, slide thuyết trình | `son-nh` | `son-viz-testcases` | `docs/SON.md` |
| Đinh Quang Duy | 23810310003 | `Dinh Quang Duy` | Thành viên: luật kết hợp, ma trận tương quan, giảm chiều PCA, Chương 3 báo cáo | `duy-tk` | `duy-assoc-reduce` | `docs/DUY.md` |
| Phạm Đức Anh (DA) | 23810310004 | `Pham Duc Anh` | Thành viên: phân cụm k-means, mô hình phân lớp & hồi quy dự báo phụ tải, đánh giá lỗi, Chương 5 & 6 | `da-anh` | `da-cluster-models-eval` | `docs/DA.md` |

Nhánh chung: `main` (chỉ nhận PR, chỉ Đức merge). **Chỉ có đúng 5 nhánh này.**

## 2. Bộ file phải biết (đọc theo thứ tự)
1. `TEAM.md` (file này) → 2. file nhiệm vụ của bạn (`docs/<TÊN>.md`) → 3. `tasks/README.md` + file task được giao → 4. `docs/CONVENTIONS.md` → 5. `docs/CHECKLIST.md` (việc cố định theo phase) → 6. `docs/DE_TAI.md` (yêu cầu chi tiết đề tài).

Mỗi loại thông tin chỉ có MỘT chỗ:

| Loại | Ở đâu | Ai được sửa |
|---|---|---|
| Thông số (SEED, ngưỡng, tên cột, đường dẫn, nguồn dữ liệu) | `src/config.py` | Chỉ Đức |
| Quy ước (định nghĩa, nhãn, tên tệp hình/bảng, giao diện hàm) | `docs/CONVENTIONS.md` | Chỉ Đức |
| Checklist theo phase (khớp rubric của đề) | `docs/CHECKLIST.md` | Chỉ Đức |
| Task linh động | `tasks/Txxx-*.md` (+ `scripts/tasks.py`) | Đức tạo; người được giao cập nhật `status` và "Kết quả" |
| Nhật ký quyết định | `docs/decisions/README.md` | Chỉ Đức |
| Hồ sơ làm việc nhóm (phiếu đăng ký, kế hoạch, rủi ro, nhật ký tuần, tự đánh giá) | `docs/PROJECT_RECORDS.md` | Đức |
| Luật cho AI | `TEAM.md`, `AGENTS.md` | Chỉ Đức |

## 3. File sở hữu (mỗi file một chủ)
| Người | Được sửa |
|---|---|
| Đức | `src/config.py`, `src/data_prep.py`, `run_all.py`, `data/download_data.py`, `docs/` (trừ file thành viên khác sở hữu), `tasks/` (tạo task), `.github/`, `prompts/`, `scripts/`, `TEAM.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, `requirements.txt`, `pytest.ini`, `.gitignore`, `.gitattributes` |
| Sơn | `src/viz.py`, `docs/DATA_DICTIONARY.md`, `docs/TESTCASES.md`, `docs/BAOCAO_DINH_DANG.md`, `docs/SLIDE_NHAP.md`, `notebooks/son_*` |
| Duy | `src/assoc.py`, `src/reduce.py`, `docs/BAOCAO_NHAP_DUY.md`, `notebooks/duy_*` |
| DA | `src/clustering.py`, `src/models.py`, `src/evaluate.py`, `docs/BAOCAO_NHAP_DA.md`, `notebooks/da_*` |
| Ai cũng được | file task của mình, `docs/trace_<tên>.md` của mình, `results/figures|tables/` (chỉ tệp do mã của mình sinh ra, tên theo `CONVENTIONS.md`), `tests/` của khối mình |

Cần sửa file của người khác → ghi vào task, nhắn chủ file. Không tự sửa. `tests/test_interfaces.py` là test dùng chung: chỉ Đức sửa, qua PR riêng.

## 4. Bắt đầu mỗi buổi làm (bắt buộc, đúng thứ tự; PowerShell/Bash)
```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate  # Trên Linux/macOS hoặc .\.venv\Scripts\Activate.ps1 trên Windows PowerShell
export PYTHONUTF8=1        # Windows: $env:PYTHONUTF8=1
git checkout <nhánh-của-bạn>
git pull origin <nhánh-của-bạn>
git fetch origin
git merge origin/main
python scripts/doctor.py
```
- `doctor.py` báo LỖI thì sửa theo hướng dẫn nó in ra trước khi làm việc.
- Merge `origin/main` bị xung đột → **DỪNG**. File không thuộc quyền của bạn thì lấy bản của `main`. Còn lại báo Đức. AI không tự giải quyết xung đột.
- Ngày đầu tiên: `git clone <repo>`, `git checkout <nhánh-của-bạn>`, `python -m venv .venv`, kích hoạt, `pip install -r requirements.txt`, `git config user.name "<tên ở bảng mục 1>"`, tải dữ liệu theo `README.md`.

## 5. Nhận và làm task
1. Mở `tasks/README.md`, tìm task có `owner` là bạn và `status: todo` (ưu tiên theo hạn).
2. Đọc file task. **Chỉ sửa các file ghi ở dòng `files:`.**
3. Đổi `status: doing`. Làm xong → `status: review` và điền mục "Kết quả".
4. Thông số lấy từ `src/config.py`. Thiếu thông số → KHÔNG tự đặt, ghi vào task và báo Đức.

## 6. Commit và push
- Mẫu commit: `T003 feat(b): them bieu do phan bo`
  - `T003` = mã task; Đức dùng `LEAD` cho việc quản trị.
  - loại: `feat` | `fix` | `test` | `docs` | `chore`
  - phạm vi: chữ cái khối `a`…`h` của đề, hoặc `report`, `infra`
- Trước khi commit: `python -m pytest` không được có test ĐỎ (SKIP thì được).
- Lệnh git ĐƯỢC PHÉP: `status`, `diff`, `log`, `add <tệp cụ thể>`, `commit`, `pull origin <nhánh-của-bạn>`, `fetch`, `merge origin/main`, `checkout <nhánh-của-bạn>`, `push origin <nhánh-của-bạn>`.
- Lệnh git CẤM: `reset --hard`, `push --force`/`-f`, `rebase`, `checkout -- .`, `clean -f`, `branch -D`, `commit --amend` sau khi đã push, `add .` / `add -A` (tránh thêm nhầm tệp), mọi lệnh đụng nhánh của người khác.
- Mỗi người chỉ push file mình sở hữu (mục 3): lịch sử git là minh chứng điểm đóng góp cá nhân (tiêu chí 6.2 của đề).

## 7. Pull Request
- Mỗi người có MỘT PR thường trực `<nhánh-của-bạn> → main`. Đã có thì chỉ push thêm.
- Tiêu đề: `[son-viz-testcases] T003 T004` (liệt kê mã task trong PR). Điền đủ mẫu PR.
- Reviewer là Đức. **Chỉ Đức merge** (merge commit, không squash).
- Sau khi Đức báo "đã merge", mọi người làm lại mục 4.

## 8. Dùng AI
- **Quy định của nhóm:** AI được dùng để hỗ trợ viết mã, giải thích thuật toán, hỗ trợ soạn thảo báo cáo.
- **Yêu cầu bắt buộc của đề:** Mọi con số và hình trong báo cáo phải do mã của nhóm chạy ra thật từ dữ liệu; không bịa số liệu.
- Phụ lục báo cáo phải khai báo công cụ AI đã dùng và mục đích sử dụng.
- Mỗi thành viên phải hiểu sâu và giải thích được mã nguồn cũng như kết quả thuộc phần việc của mình khi vấn đáp trước hội đồng.

## 9. Điều CẤM khác (người và AI)
- Tạo nhánh khác ngoài 5 nhánh; push thẳng `main`; push lên nhánh người khác.
- Sửa file ngoài danh sách sở hữu (mục 3) hoặc ngoài `files:` của task.
- Viết thông số thẳng vào code thay vì lấy từ `src/config.py` (có test chặn).
- Đưa dữ liệu thô vào git (`data/raw/`), `.venv/`, tệp > 1 MB, notebook còn output.
- Đổi tên hàm hoặc chữ ký trong stub `src/` và `tests/test_interfaces.py` khi chưa báo Đức.
- Dùng thư viện ngoài danh sách đề cho phép (NumPy, Pandas, Matplotlib, scikit-learn, mlxtend, statsmodels, NetworkX) khi chưa hỏi ý kiến giảng viên.

## 10. Lệnh thường dùng
```bash
python scripts/doctor.py            # kiểm môi trường
python -m pytest                    # chạy test
python scripts/tasks.py list        # xem task
python scripts/tasks.py list --owner son
```
