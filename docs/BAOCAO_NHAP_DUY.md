# BẢN NHÁP CHƯƠNG 3 BÁO CÁO (Chủ: Duy)

## Chương 3. Thiết kế sơ bộ giải pháp
### 3.1 Lựa chọn quy trình chuẩn CRISP-DM
Nghiên cứu áp dụng quy trình chuẩn công nghiệp CRISP-DM (Cross-Industry Standard Process for Data Mining) bao gồm 6 giai đoạn:
1. Thấu hiểu bài toán nghiệp vụ (Business Understanding): Phân tích nhu cầu phụ tải điện hộ gia đình.
2. Thấu hiểu dữ liệu (Data Understanding): Khảo sát tập dữ liệu UCI Household Electric Power Consumption.
3. Chuẩn bị dữ liệu (Data Preparation): Làm sạch, xử lý missing value '?', loại bỏ rò rỉ dữ liệu `Global_intensity`, tạo đặc trưng thời gian và trễ.
4. Xây dựng mô hình (Modeling): Phân cụm k-means, khai phá luật kết hợp Apriori, phân lớp mức phụ tải và hồi quy dự báo công suất.
5. Đánh giá (Evaluation): Đánh giá qua các độ đo định lượng F1 macro, RMSE, MAE, R², ma trận nhầm lẫn và bảng ca kiểm thử.
6. Triển khai (Deployment): Đóng gói script tự động hóa `run_all.py` và đề xuất giải pháp quản lý năng lượng.

### 3.2 Thiết kế luồng xử lý dữ liệu và kiểm định tránh rò rỉ
- Chia tập theo trình tự thời gian 80% train / 20% test.
- Khớp (fit) chuẩn hóa StandardScaler và PCA hoàn toàn trên tập train.

### 3.3 Danh mục thuật toán và độ đo đánh giá
- Phân lớp: Decision Tree, k-NN, Logistic Regression (Độ đo: F1 macro, Accuracy).
- Hồi quy: Linear Regression, Decision Tree Regressor (Độ đo: RMSE, MAE, R²).
- Luật kết hợp: Apriori (Độ đo: Support, Confidence, Lift).
- Phân cụm: k-means (Độ đo: Inertia, Silhouette score).
