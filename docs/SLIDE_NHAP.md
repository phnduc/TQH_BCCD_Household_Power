# DÀN Ý SLIDE VÀ KỊCH BẢN THUYẾT TRÌNH (Chủ: Sơn)

Tổng số trang slide: 11 trang. Thời lượng trình bày: 10 phút.

| Slide | Tiêu đề slide | Nội dung tóm tắt | Thành viên trình bày |
|---|---|---|---|
| 1 | Trang bìa | Tên đề tài: Phân tích & dự báo phụ tải điện hộ gia đình, Lớp D18CNPM1, 4 thành viên | Phan Đức (Lead) |
| 2 | Bối cảnh & Mục tiêu | Smart Grid, bài toán phụ tải điện sinh hoạt, 3 câu hỏi phân tích | Phan Đức |
| 3 | Khảo sát dữ liệu & EDA | Dữ liệu UCI Household Power, các biến đo, xử lý thiếu '?' và rò rỉ | Nguyễn Hoàng Sơn |
| 4 | Trực quan hóa phụ tải | Heatmap Giờ x Thứ, phân bố công suất theo chế độ, ma trận tương quan | Nguyễn Hoàng Sơn |
| 5 | Quy trình & Giảm chiều | Áp dụng CRISP-DM, phân tích thành phần chính PCA | Trần Khắc Duy |
| 6 | Khai phá luật kết hợp | Kết quả thuật toán Apriori, diễn giải 5 luật tiêu biểu liên quan Peak Load | Trần Khắc Duy |
| 7 | Phân cụm hồ sơ phụ tải | Gom cụm k-means, phân tích Elbow và Silhouette, phân loại kiểu ngày | Đặng Đức Anh (DA) |
| 8 | Mô hình máy học & Dự báo | Kết quả phân lớp (F1 macro) và hồi quy công suất (RMSE, R²) | Đặng Đức Anh (DA) |
| 9 | Phân tích lỗi & Cải thiện | Phân tích lỗi theo khung giờ, hiệu quả của đặc trưng trễ (lags) | Đặng Đức Anh (DA) |
| 10 | Kết luận & Khuyến nghị | Đề xuất dịch chuyển phụ tải, giải pháp quản lý năng lượng thông minh | Phan Đức |
| 11 | Hỏi đáp (Q&A) | Lời cảm ơn và sẵn sàng trả lời câu hỏi vấn đáp | Cả nhóm |

## Kịch bản demo chạy mã nguồn tự động
1. Mở terminal, kích hoạt môi trường `.venv`.
2. Chạy `python scripts/doctor.py` để chứng minh môi trường đạt chuẩn.
3. Chạy `python -m pytest` chứng minh toàn bộ các test kiểm thử đều xanh.
4. Chạy `python run_all.py` trình chiếu toàn bộ luồng tiền xử lý, huấn luyện và xuất bảng kết quả tự động.
