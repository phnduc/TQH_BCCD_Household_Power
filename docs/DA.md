# DA — Đặng Đức Anh

Nhánh: `da-cluster-models-eval`. Đọc `TEAM.md` trước.

## Phần của bạn
- **Khối F Phân cụm hồ sơ phụ tải (`src/clustering.py`):**
  - Cài đặt thuật toán k-means gom cụm các hồ sơ tiêu thụ điện hàng ngày.
  - Đánh giá quán tính (Elbow) và hệ số Silhouette để lựa chọn số cụm k tối ưu.
  - Lập bảng chéo đối chiếu giữa cụm phân cụm và mức phụ tải thực tế; viết mục 4.6 báo cáo.
- **Khối E Mô hình học máy (`src/models.py`):**
  - Cài đặt $\ge 3$ mô hình phân lớp mức phụ tải (`Low_Load`, `Normal_Load`, `Peak_Load`): Decision Tree, k-NN, Logistic Regression.
  - Cài đặt mô hình hồi quy dự báo công suất tác dụng: Linear Regression, Decision Tree Regressor.
  - Tinh chỉnh siêu tham số với GridSearchCV và kiểm định chéo phân tầng K-Fold trên tập huấn luyện; viết mục 4.5 báo cáo.
- **Khối G Đánh giá & Phân tích lỗi (`src/evaluate.py`):**
  - Báo cáo chi tiết các độ đo: Accuracy, Precision, Recall, F1 macro từng lớp, MAE, RMSE, R².
  - Phân tích lỗi dự báo theo giờ và ngày; thử nghiệm bổ sung đặc trưng trễ (lags); viết Chương 5 và Chương 6 báo cáo.

## Tiêu chí chấm chính
4.2, 4.3, 4.4, 5.2, 5.3, Chương 5, Chương 6.
