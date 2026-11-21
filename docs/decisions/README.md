# NHẬT KÝ QUYẾT ĐỊNH THIẾT KẾ (Chỉ Đức thêm dòng)

Ghi nhận mọi quyết định thay đổi về thông số kỹ thuật (`src/config.py`), quy ước nghiệp vụ (`docs/CONVENTIONS.md`) hoặc phân công nhóm.

| Ngày | Quyết định đã chốt | Lý do kỹ thuật / nghiệp vụ | Ảnh hưởng đến mã nguồn |
|---|---|---|---|
| 21/11/2026 | Nhóm thành lập gồm 4 thành viên: Đức (Lead), Sơn, Duy, DA | Đáp ứng yêu cầu đề tài môn học 004759, lớp D18CNPM1 | `TEAM.md`, `PROJECT_RECORDS.md` |
| 21/11/2026 | Chọn đề tài: Phân tích và dự báo phụ tải điện hộ gia đình (UCI Household Power) | Đề tài mang tính thực tiễn cao trong quản lý năng lượng thông minh | Toàn bộ repo |
| 21/11/2026 | Cố định hạt giống ngẫu nhiên `SEED = 4759` (mã học phần) | Đảm bảo tính tái lập 100% của mọi phép chia tập, k-means và mô hình | `src/config.py` |
| 21/11/2026 | Chia tập huấn luyện / kiểm tra theo thời gian (`SPLIT_MODE = "time"`, 80/20) | Dữ liệu phụ tải là chuỗi thời gian, chia ngẫu nhiên gây rò rỉ thông tin tương lai | `src/data_prep.py` |
| 21/11/2026 | Loại bỏ biến `Global_intensity` khỏi tập đặc trưng huấn luyện | Cường độ dòng điện $I$ có tương quan $>0.999$ với công suất $P$ ($P \approx V \cdot I$), gây rò rỉ đo đếm | `config.LEAKY_COLS`, `src/data_prep.py` |
| 21/11/2026 | Gán nhãn phân lớp `Load_Level` gồm 3 mức: `Low_Load`, `Normal_Load`, `Peak_Load` | Dựa trên tam phân vị (33.3%, 66.7%) của tập huấn luyện | `src/config.py`, `src/data_prep.py` |
| 21/11/2026 | Phân cụm k-means sử dụng phương pháp Elbow và Silhouette để chọn k | Lựa chọn số cụm khách quan, có cơ sở khoa học | `src/clustering.py` |
| 21/11/2026 | Bổ sung thử nghiệm đặc trưng trễ (`LAG_STEPS = [1, 2, 4, 96]`) cho hồi quy | Tận dụng quán tính tiêu thụ phụ tải của các chu kỳ trước đó để cải thiện RMSE | `src/config.py`, `run_all.py` |
