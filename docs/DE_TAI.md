# ĐỀ TÀI — Phân tích và dự báo phụ tải điện hộ gia đình

Tài liệu tóm lược yêu cầu nghiệp vụ và kỹ thuật của đề tài.

## 1. Tổng quan đề tài
- **Tên đề tài:** Phân tích và dự báo phụ tải điện hộ gia đình (Household Electric Power Load Analysis & Forecasting).
- **Học phần:** Phân tích và trực quan hóa dữ liệu (004759), 3 tín chỉ.
- **Tập dữ liệu:** UCI Individual Household Electric Power Consumption.
- **Quy mô:** ~2.075.259 bản ghi đo từng phút trong gần 4 năm (12/2006 đến 11/2010), được tổng hợp và phân tích theo chu kỳ 15 phút (~35.040 bản ghi/năm hoặc tổng hợp toàn chu kỳ).
- **Công cụ:** Python, NumPy, Pandas, Matplotlib, scikit-learn, mlxtend, statsmodels.

## 2. Các yêu cầu cốt lõi theo khối nghiệp vụ
- **Khối A (Bài toán & Quy trình):**
  - Đặt bài toán trong bối cảnh quản lý nhu cầu phụ tải (DSM - Demand Side Management) và lưới điện thông minh (Smart Grid).
  - Xác định người hưởng lợi: Công ty điện lực (dự báo công suất, điều độ) và chủ hộ gia đình (tiết kiệm điện năng, tối ưu chi phí).
  - Đặt ra ít nhất 3 câu hỏi phân tích:
    1. Xu hướng tiêu thụ phụ tải điện biến động như thế nào theo khung giờ trong ngày, ngày làm việc so với ngày cuối tuần, và các mùa trong năm?
    2. Các phân hệ thiết bị trong nhà (bếp, giặt là, điều hòa/nóng lạnh) đóng góp ra sao vào công suất đỉnh (Peak Load), và có những luật kết hợp nào giữa hành vi sử dụng thiết bị với phụ tải cao điểm?
    3. Các mô hình học máy đạt độ chính xác dự báo công suất tác dụng (kW) và khả năng nhận diện chế độ phụ tải (Thấp, Bình thường, Cao điểm) ở mức độ nào?
- **Khối B (Dữ liệu & Tiền xử lý):**
  - Xử lý giá trị khuyết thiếu ký hiệu '?' trong dữ liệu gốc.
  - Kiểm tra và xử lý các giá trị vi phạm vật lý (điện áp ngoài dải 200–260V, công suất âm).
  - Tách các đặc trưng thời gian: Giờ, tháng, thứ trong tuần, cờ ngày cuối tuần.
  - Tính toán năng lượng tiêu thụ không đo đếm riêng `Sub_metering_remainder`.
  - Kiểm tra rò rỉ dữ liệu giữa `Global_intensity` và `Global_active_power`.
  - Phân chia tập huấn luyện và kiểm tra theo trình tự thời gian.
  - Giảm chiều dữ liệu bằng PCA và xếp hạng thuộc tính.
- **Khối C (Trực quan hóa EDA & Kết quả):**
  - Tối thiểu 8 biểu đồ thuộc 4 loại: Phân bố, so sánh theo nhóm/thời gian, quan hệ tương quan, kết quả mô hình.
  - Heatmap phụ tải theo Giờ x Thứ; Tán xạ công suất phản kháng và tác dụng; Phân bố phụ tải theo chế độ; Ma trận nhầm lẫn và độ quan trọng thuộc tính.
- **Khối D (Mẫu thường xuyên & Luật kết hợp):**
  - Rời rạc hóa thời gian và trạng thái thiết bị thành dạng giao dịch.
  - Áp dụng Apriori / FP-growth tìm các luật kết hợp dẫn đến phụ tải cao điểm.
  - Diễn giải ý nghĩa thực tế của ≥ 5 luật.
- **Khối E (Mô hình học máy):**
  - Bài toán 1: Phân lớp mức phụ tải (`Low_Load`, `Normal_Load`, `Peak_Load`) với Decision Tree, k-NN, Logistic Regression.
  - Bài toán 2: Hồi quy dự báo công suất tác dụng (`Global_active_power`) với Linear Regression, Decision Tree Regressor.
  - Tinh chỉnh siêu tham số với GridSearchCV và kiểm định chéo phân tầng K-Fold.
  - So sánh mô hình có và không có giảm chiều PCA.
- **Khối F (Phân cụm):**
  - Áp dụng k-means phân cụm hồ sơ tiêu thụ điện hàng ngày.
  - Chọn số cụm k dựa trên phương pháp Elbow và hệ số Silhouette.
  - Đối chiếu cụm với mức phụ tải thực tế để hiểu hành vi tiêu thụ điện.
- **Khối G (Đánh giá & Phân tích lỗi):**
  - Đánh giá bằng Accuracy, Precision, Recall, F1 macro, MAE, RMSE, R².
  - Bảng ca kiểm thử phần mềm (Phụ lục D).
  - Phân tích lỗi dự báo theo giờ và ngày, thử nghiệm đặc trưng trễ (lags) để cải thiện.
- **Khối H (Quản lý dự án):**
  - Hồ sơ làm việc nhóm đầy đủ (Phiếu đăng ký, kế hoạch tuần, bảng rủi ro, tự đánh giá đóng góp cá nhân).
  - Báo cáo thuyết minh 20–30 trang, slide 10–12 trang.
