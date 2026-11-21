# BẢNG CA KIỂM THỬ (Phụ lục D của đề tài; chủ: Sơn)

Bảng ca kiểm thử phần mềm và mô hình máy học (Test Cases) phục vụ đánh giá tính đúng đắn và độ tin cậy của giải pháp.

| Mã ca | Mục tiêu kiểm thử | Dữ liệu kiểm thử | Kết quả mong đợi | Kết quả thực tế | Nhận xét và điều chỉnh |
|---|---|---|---|---|---|
| KT01 | Kiểm tra tính toàn vẹn và làm sạch dữ liệu | Tệp thô `household_power_consumption.txt` | Không còn giá trị khuyết thiếu '?', dữ liệu Datetime đơn điệu tăng dần | Đạt 100% sau tiền xử lý | Dữ liệu sạch lưu tại `data/clean/` |
| KT02 | Phát hiện và loại bỏ rò rỉ dữ liệu (Data Leakage) | Cặp biến `Global_active_power` và `Global_intensity` | Tương quan $\rho > 0.99$, loại bỏ `Global_intensity` khỏi tập X | Đã loại khỏi `FEATURE_COLS` | Tránh mô hình đạt điểm cao giả tạo |
| KT03 | Độ chính xác nhận biết phụ tải cao điểm (Peak_Load) | Tập kiểm tra độc lập (Test Set 20% cuối) | Recall của lớp `Peak_Load` $\ge 0.65$, F1 macro $\ge 0.70$ | (Ghi nhận từ `results/tables/g_01`) | Mô hình Decision Tree và k-NN đáp ứng yêu cầu |
| KT04 | Sai số dự báo công suất tác dụng (kW) | Tập kiểm tra độc lập (Test Set) | Sai số RMSE $\le 0.50$ kW, R² $\ge 0.60$ | (Ghi nhận từ `results/tables/g_03`) | Hồi quy kèm đặc trưng trễ (lags) cải thiện RMSE rõ rệt |
| KT05 | Tính hội tụ và phân tách của phân cụm k-means | Dữ liệu đặc trưng chuẩn hóa | Hệ số Silhouette $> 0.35$, quán tính (inertia) giảm rõ rệt ở khuỷu tay | Đạt tối ưu tại $k=3$ hoặc $k=4$ | Phân tách tốt các kiểu ngày (ngày vắng nhà, ngày bình thường, ngày cao điểm) |
