# CONVENTIONS — Quy ước chung (chỉ Đức sửa)

Mục tiêu: Bốn thành viên và mọi AI hỗ trợ đều thống nhất về định nghĩa, giao diện hàm và kết quả.
Thông số số học đặt ở `src/config.py`; file này giữ **định nghĩa và quy ước học thuật**.

## 1. Dữ liệu và nhãn
- **Nguồn:** UCI Individual Household Electric Power Consumption (~2.075.259 bản ghi đo từng phút trong 47 tháng từ 12/2006 đến 11/2010 tại Sceaux, Pháp).
- **Mục tiêu hồi quy:** `Global_active_power` (công suất tác dụng toàn hộ gia đình, đơn vị kW).
- **Mục tiêu phân lớp:** `Load_Level` (3 mức phụ tải: `Low_Load`, `Normal_Load`, `Peak_Load` dựa trên tam phân vị của tập huấn luyện).
- **Kiểm tra rò rỉ dữ liệu (Data Leakage):**
  - Biến `Global_intensity` là cường độ dòng điện (A) đo đồng thời với công suất. Theo định luật Ohm và công suất xoay chiều $P \approx V \cdot I \cdot \cos\varphi / 1000$, `Global_intensity` có tương quan $> 0.999$ với `Global_active_power`. Việc đưa `Global_intensity` vào dự báo công suất sẽ gây rò rỉ trực tiếp (mô hình học thuộc lòng công thức đo lường thay vì học quy luật phụ tải). Do đó `Global_intensity` bị đưa vào `config.LEAKY_COLS` và bị loại bỏ khỏi đặc trưng huấn luyện.
- Dữ liệu sạch lưu ở `data/clean/household_power_clean.csv`; dữ liệu thô không đưa vào git.

## 2. Chia tập và kiểm định tránh rò rỉ
- Chia tập theo **thứ tự thời gian** (`config.SPLIT_MODE = "time"`, `TEST_FRACTION = 0.2`): 80% thời gian đầu dùng làm tập huấn luyện (train), 20% thời gian cuối dùng làm tập kiểm tra độc lập (test).
- Tuyệt đối không chia ngẫu nhiên (random split) đối với dữ liệu chuỗi thời gian phụ tải vì các mốc thời gian liền kề có độ tự tương quan cao.
- Mọi phép biến đổi (StandardScaler, PCA, tính tam phân vị mức phụ tải) **chỉ khớp (fit) trên tập huấn luyện**, sau đó áp dụng (transform) sang tập kiểm tra.
- Kiểm định chéo K-Fold (5 folds) chỉ thực hiện trên tập huấn luyện.
- Hạt giống ngẫu nhiên: Mọi `random_state` lấy cố định từ `config.SEED = 4759`.

## 3. Chỉ số đánh giá
- **Phân lớp:** Báo cáo Accuracy, Precision, Recall, F1-score chi tiết theo từng lớp (`Low_Load`, `Normal_Load`, `Peak_Load`) và F1 macro trung bình; phân tích ma trận nhầm lẫn.
- **Hồi quy dự báo:** MAE (kW), RMSE (kW), R² score.
- **Luật kết hợp:** Support, Confidence, Lift; diễn giải nghiệp vụ tối thiểu 5 luật tiêu biểu liên quan đến giờ cao điểm hoặc phân hệ thiết bị.
- **Phân cụm k-means:** Đánh giá bằng phương pháp quán tính (Elbow / Inertia) và hệ số Silhouette để chọn số cụm k tối ưu.
- **So sánh giảm chiều:** Đánh giá hiệu năng mô hình khi có và không có PCA trên cùng tập dữ liệu kiểm tra.

## 4. Biểu đồ và hình ảnh
- Tối thiểu 8 biểu đồ thuộc 4 nhóm loại hình (phân bố, quan hệ tương quan, so sánh theo thời gian/nhóm, kết quả mô hình).
- Mỗi biểu đồ bắt buộc có: Tiêu đề rõ ràng, nhãn các trục tọa độ, đơn vị đo, và ít nhất một nhận xét rút ra từ dữ liệu.
- Quy ước đặt tên: `results/figures/<khối>_<số>_<mô_tả>.png`; bảng: `results/tables/<khối>_<số>_<mô_tả>.csv`.
- Mỗi hình/bảng được ghi nhận vào `docs/trace_<tên>.md` của người thực hiện.

## 5. Quyết định đã chốt
- Hạt giống: `SEED = 4759`.
- Chia tập: `SPLIT_MODE = "time"`, `TEST_FRACTION = 0.2`.
- Độ đo chính: `f1_macro` cho phân lớp và `rmse` cho hồi quy dự báo công suất.
- Mô hình phân lớp: Decision Tree, k-NN, Logistic Regression.
- Mô hình hồi quy: Linear Regression, Decision Tree Regressor.
