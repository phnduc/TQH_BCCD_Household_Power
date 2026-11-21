# BẢN NHÁP CHƯƠNG 5 VÀ 6 BÁO CÁO (Chủ: DA)

## Chương 5. Đánh giá kết quả thực nghiệm và phân tích lỗi
### 5.1 Đánh giá kết quả phân lớp mức phụ tải
- Báo cáo chỉ số Precision, Recall, F1 macro chi tiết của 3 mô hình Decision Tree, k-NN, Logistic Regression (trích xuất từ `results/tables/g_01_phan_lop_tung_lop.csv`).
- Phân tích ma trận nhầm lẫn và các trường hợp nhầm lẫn phổ biến nhất giữa `Normal_Load` và `Peak_Load`.

### 5.2 Đánh giá kết quả hồi quy dự báo công suất tác dụng
- So sánh sai số MAE, RMSE, R² trên tập kiểm tra độc lập giữa Linear Regression và Decision Tree Regressor (`results/tables/g_03_hoi_quy_kiem_tra.csv`).
- Đánh giá mức độ cải thiện khi bổ sung đặc trưng trễ (Lag features): Sai số RMSE giảm đáng kể do tính quán tính của phụ tải điện.

### 5.3 Phân tích lỗi theo khung giờ và loại ngày
- Tỉ lệ lỗi tập trung cao nhất vào các khung giờ chuyển tiếp sinh hoạt (18h–20h) khi các thiết bị công suất lớn được bật đồng thời.

## Chương 6. Kết luận và khuyến nghị quản lý năng lượng
### 6.1 Kết luận
- Dự án đã giải quyết trọn vẹn 3 câu hỏi phân tích ban đầu, làm rõ quy luật biến động phụ tải hộ gia đình theo giờ, ngày và phân hệ thiết bị.
### 6.2 Khuyến nghị
- Khuyến nghị hộ gia đình dịch chuyển giờ vận hành của máy giặt/máy sấy (`Sub_metering_2`) và điều hòa/nóng lạnh (`Sub_metering_3`) sang khung giờ thấp điểm đêm để tiết kiệm chi phí và san bằng biểu đồ phụ tải.
