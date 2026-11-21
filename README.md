# TQH_BCCD_Household_Power — Phân tích và dự báo phụ tải điện hộ gia đình

Báo cáo chuyên đề học phần **Phân tích và trực quan hóa dữ liệu (004759)**, Trường Đại học Điện lực.
Lớp D18CNPM1, Nhóm gồm 4 thành viên: Đức (Trưởng nhóm), Sơn, Duy, DA.
Dữ liệu: UCI Individual Household Electric Power Consumption (~2.075.259 bản ghi đo từng phút từ 12/2006 đến 11/2010 tại Sceaux, Pháp).

> **Làm việc nhóm: đọc [`TEAM.md`](TEAM.md) trước.**
> Mọi thông số cố định ở [`src/config.py`](src/config.py). Quy ước chung ở [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md).

## Môi trường
Python 3.12, trong `.venv`, thư viện ở `requirements.txt` (ghim `==`).

```bash
python -m venv .venv
source .venv/bin/activate    # Trên Windows PowerShell: .\.venv\Scripts\Activate.ps1
export PYTHONUTF8=1          # Trên Windows PowerShell: $env:PYTHONUTF8=1
pip install -r requirements.txt
python scripts/doctor.py
```

## Tải dữ liệu
Nguồn: UCI Machine Learning Repository, Individual Household Electric Power Consumption.
Dữ liệu thô không nằm trong git (`data/raw/`); chỉ có script tải.

```bash
python data/download_data.py
```

URL, kích thước và SHA-256 được quy định trong `src/config.py`. Nếu tải tự động lỗi, tải tệp nén từ UCI, giải nén và đặt `household_power_consumption.txt` vào `data/raw/`.

## Chạy lại kết quả
```bash
python run_all.py          # Chạy tiền xử lý dữ liệu (Khối B) + mô hình, đánh giá (E, G)
python -m pytest           # Kiểm tra cấu trúc repo, cấu hình, giao diện hàm, số ma thuật, công cụ task
```

## Thống nhất cách làm việc, cấu hình, môi trường
Mục tiêu: Bốn người, bốn môi trường vẫn cho ra cùng một con số nhất quán.
Quy tắc đầy đủ: [`TEAM.md`](TEAM.md), [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md).

### Mỗi loại thông tin chỉ có một chỗ
| Loại | Nơi duy nhất | Ai sửa |
|---|---|---|
| Thông số (SEED, ngưỡng, tên cột, nguồn dữ liệu) | [`src/config.py`](src/config.py) | Chỉ Đức |
| Quy ước, định nghĩa, tên tệp hình/bảng | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) | Chỉ Đức |
| Quyết định đổi thông số hoặc quy ước | [`docs/decisions/`](docs/decisions/README.md) | Chỉ Đức |
| Checklist theo phase (khớp rubric của đề) | [`docs/CHECKLIST.md`](docs/CHECKLIST.md) | Chỉ Đức |
| Task linh động | [`tasks/`](tasks/README.md) | Đức tạo; người nhận cập nhật trạng thái |
| Hồ sơ nhóm (phiếu đăng ký, kế hoạch, rủi ro, tự đánh giá) | [`docs/PROJECT_RECORDS.md`](docs/PROJECT_RECORDS.md) | Đức |
| Luật cho AI | `TEAM.md`, `AGENTS.md` | Chỉ Đức |

### Nhánh, commit, PR
- Chỉ **5 nhánh**: `main` (chỉ nhận PR, chỉ Đức merge, merge commit) và 4 nhánh cá nhân. Không tạo nhánh tự do.

| Người | `git config user.name` | Nhánh duy nhất | Nhiệm vụ chính |
|---|---|---|---|
| Phan Đức (Trưởng nhóm) | `Phan Duc` | `duc-lead-data-models` | Điều phối, tiền xử lý, cấu hình, đóng gói |
| Nguyễn Hoàng Sơn | `Nguyen Hoang Son` | `son-viz-testcases` | Trực quan hóa EDA, từ điển dữ liệu, ca kiểm thử, slide |
| Trần Khắc Duy | `Tran Khac Duy` | `duy-assoc-reduce` | Luật kết hợp, giảm chiều PCA, tương quan, Chương 3 |
| Đặng Đức Anh (DA) | `Dang Duc Anh` | `da-cluster-models-eval` | Phân cụm k-means, phân lớp, hồi quy dự báo phụ tải, Chương 5 & 6 |

- Mỗi người một PR thường trực `<nhánh> → main`; đã có thì chỉ push thêm.
- Commit: `T004 feat(c): them bieu do phan bo phu tai` (mã task; Đức dùng `LEAD`; loại `feat|fix|test|docs|chore`).
- Cấm: `push --force`, `reset --hard`, `rebase`, `add .`, push lên nhánh người khác.

### Checklist theo phase
Tóm tắt từ [`docs/CHECKLIST.md`](docs/CHECKLIST.md) (mã khớp Rubric R3, tổng 10,0). Task hằng ngày ở [`tasks/`](tasks/README.md).

| Phase | Mốc | Việc chính |
|---|---|---|
| P1 | Hết tuần 1 | Khối A (1.1), phiếu đăng ký và kế hoạch, tải và khảo sát dữ liệu phụ tải |
| P2 | Hết tuần 2 | Khối B, C, D: làm sạch dữ liệu, xử lý thiếu `?`, từ điển, EDA trực quan, luật kết hợp |
| P3 | Hết tuần 3 | Khối E, F, G: phân lớp mức phụ tải, hồi quy dự báo công suất, phân cụm hồ sơ ngày, ca kiểm thử |
| P4 | Hết tuần 4 | Hoàn thiện báo cáo 20–30 trang, slide thuyết trình 10–12 trang, đóng gói tệp nén |
| P5 | Buổi thi | Thuyết trình 10 phút và vấn đáp |

## Cấu trúc thư mục
```
TEAM.md  README.md  AGENTS.md  CLAUDE.md  GEMINI.md
src/        config, data_prep, reduce, viz, assoc, models, clustering, evaluate
data/       download_data.py (data/raw/ không vào git; data/clean/ lưu dữ liệu sạch)
notebooks/  duc_*, son_*, duy_*, da_*  (xóa output trước khi commit)
results/    figures/, tables/  (do mã sinh ra)
docs/       CHECKLIST, CONVENTIONS, DE_TAI, BAOCAO_DAN_Y, DUC/SON/DUY/DA, PROJECT_RECORDS, TESTCASES, DATA_DICTIONARY, decisions/
tasks/      Txxx-*.md  (scripts/tasks.py)
scripts/    doctor.py, tasks.py
tests/      pytest
```
