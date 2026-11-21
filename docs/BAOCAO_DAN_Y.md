# DÀN Ý CHI TIẾT BÁO CÁO THUYẾT MINH

Đề tài: **Phân tích và dự báo phụ tải điện hộ gia đình**
Học phần: Phân tích và trực quan hóa dữ liệu (004759).
Độ dài: 20–30 trang (không kể phụ lục). Trình bày font Times New Roman 13, giãn dòng 1.3, khổ giấy A4.
Toàn bộ số liệu và đồ thị phải trích xuất trực tiếp từ mã nguồn thực thi trong `results/`.

---

## Bố cục ngân sách trang (Mục tiêu 26–28 trang)
| Chương | Nội dung chính | Số trang | Người phụ trách chính |
|---|---|---|---|
| Chương 1 | Mở đầu: Bối cảnh, mục tiêu, câu hỏi phân tích, cấu trúc báo cáo | 3–4 trang | Phan Đức |
| Chương 2 | Khảo sát bài toán và dữ liệu tiêu thụ điện hộ gia đình | 3–4 trang | Nguyễn Hoàng Sơn |
| Chương 3 | Thiết kế sơ bộ: Quy trình CRISP-DM, phương pháp và độ đo | 3–4 trang | Trần Khắc Duy |
| Chương 4 | Cài đặt thực nghiệm: Tiền xử lý, EDA, Luật kết hợp, Mô hình | 9–10 trang | Cả nhóm (Đức, Sơn, Duy, DA) |
| Chương 5 | Đánh giá kết quả, kiểm thử và phân tích lỗi mô hình | 4–5 trang | Đặng Đức Anh (DA), Sơn |
| Chương 6 | Kết luận, khuyến nghị quản lý năng lượng và hướng phát triển | 2 trang | Đặng Đức Anh (DA) |
| Chương 7 | Quản lý công việc nhóm, phân công và kiểm soát rủi ro | 2 trang | Phan Đức |
| Phụ lục | Phụ lục A (Đăng ký), B (Kế hoạch), C (Đóng góp), D (Kiểm thử), E (Khai báo AI) | Ngoài số trang | Cả nhóm |

---

## Chi tiết từng chương

### Chương 1. Mở đầu (3 trang) — Phan Đức
- 1.1 Bối cảnh đề tài: Xu thế chuyển dịch năng lượng, lưới điện thông minh (Smart Grid) và quản lý nhu cầu phụ tải hộ gia đình (Home Energy Management System - HEMS).
- 1.2 Người hưởng lợi từ kết quả phân tích: Công ty điện lực (dự báo nhu cầu, giảm áp lực giờ cao điểm) và người dân (tiết kiệm chi phí hóa đơn điện).
- 1.3 Mục tiêu và 3 câu hỏi phân tích trọng tâm.
- 1.4 Phạm vi và giới hạn của nghiên cứu.
- 1.5 Cấu trúc tổng thể của báo cáo thuyết minh.

### Chương 2. Khảo sát bài toán và dữ liệu (4 trang) — Nguyễn Hoàng Sơn
- 2.1 Yêu cầu nghiệp vụ phân tích và dự báo phụ tải.
- 2.2 Nguồn gốc dữ liệu: Bộ dữ liệu đo đếm thực tế UCI Individual Household Electric Power Consumption.
- 2.3 Từ điển dữ liệu: Chi tiết ý nghĩa các biến đo lường công suất, điện áp và 3 phân hệ Sub_metering (Bếp, Giặt là, Điều hòa/Nóng lạnh).
- 2.4 Thống kê mô tả: Bảng giá trị trung bình, độ lệch chuẩn, khoảng phân vị của các biến.
- 2.5 Phân loại thuộc tính: Biến số học, biến phân loại, biến chuỗi thời gian, và biến mục tiêu.

### Chương 3. Thiết kế sơ bộ giải pháp (3 trang) — Trần Khắc Duy
- 3.1 Quy trình phân tích dữ liệu: Áp dụng quy trình chuẩn CRISP-DM gồm 6 giai đoạn.
- 3.2 Thiết kế luồng tiền xử lý dữ liệu: Kỹ thuật xử lý khuyết thiếu, phát hiện ngoại lai, chia tập thời gian không gây rò rỉ.
- 3.3 Danh mục các loại biểu đồ trực quan hóa dự kiến (Heatmap, Scatter, Histogram, Confusion Matrix).
- 3.4 Lựa chọn các thuật toán học máy: Apriori/FP-growth (luật kết hợp), k-means (phân cụm), Decision Tree, k-NN, Logistic Regression (phân lớp), Linear Regression (hồi quy).
- 3.5 Các độ đo đánh giá định lượng: Accuracy, F1 macro, MAE, RMSE, R², Silhouette.

### Chương 4. Cài đặt thực nghiệm (9 trang) — Cả nhóm
- 4.1 Tiền xử lý dữ liệu (Đức): Báo cáo chất lượng trước và sau làm sạch; phát hiện và loại bỏ rò rỉ dữ liệu `Global_intensity`; sinh đặc trưng thời gian và phân hệ còn lại; lưu dữ liệu sạch.
- 4.2 Trực quan hóa dữ liệu khám phá EDA (Sơn): Heatmap giờ x thứ; phân bố phụ tải theo ngày; tán xạ công suất phản kháng và tác dụng; ma trận tương quan giữa các đại lượng đo.
- 4.3 Khai phá mẫu thường xuyên và luật kết hợp (Duy): Rời rạc hóa giao dịch; kết quả khai phá luật Apriori; diễn giải ý nghĩa thực tế của ≥ 5 luật tiêu biểu liên quan đến giờ cao điểm.
- 4.4 Giảm chiều và xếp hạng thuộc tính (Duy): Phân tích thành phần chính PCA; xếp hạng mức độ ảnh hưởng của các thuộc tính đến công suất tiêu thụ.
- 4.5 Huấn luyện mô hình học máy (DA): Phân lớp mức phụ tải (3 mô hình); hồi quy dự báo công suất; tối ưu hóa siêu tham số bằng GridSearchCV; thử nghiệm bổ sung đặc trưng trễ (lags).
- 4.6 Phân cụm hồ sơ phụ tải ngày (DA): Gom cụm k-means các kiểu ngày tiêu thụ; biểu đồ Elbow và Silhouette; đối chiếu cụm với chế độ phụ tải.

### Chương 5. Đánh giá và kiểm thử (4 trang) — DA & Sơn
- 5.1 Bảng ca kiểm thử phần mềm (Sơn): Đánh giá 5 ca kiểm thử chức năng và mô hình (KT01..KT05).
- 5.2 Bảng so sánh hiệu năng các mô hình (DA): So sánh độ đo phân lớp và hồi quy trên tập kiểm tra độc lập; so sánh hiệu quả khi có và không có giảm chiều PCA.
- 5.3 Phân tích lỗi và thử nghiệm cải thiện (DA): Ma trận nhầm lẫn; phân tích các khung giờ và thứ trong tuần dễ gây sai số lớn; đánh giá hiệu quả của đặc trưng trễ.

### Chương 6. Kết luận và Khuyến nghị (2 trang) — Đặng Đức Anh (DA)
- 6.1 Tóm tắt các kết quả đạt được đối với 3 câu hỏi phân tích ban đầu.
- 6.2 Khuyến nghị chính sách sử dụng điện thông minh: Dịch chuyển giờ sử dụng các thiết bị công suất lớn (máy giặt, bình nóng lạnh) khỏi khung giờ cao điểm tối.
- 6.3 Hạn chế của nghiên cứu và định hướng mở rộng (mô hình học sâu LSTM/Transformer cho chuỗi thời gian).

### Chương 7. Quản lý công việc nhóm (2 trang) — Phan Đức
- 7.1 Kế hoạch tiến độ thực tế so với dự kiến.
- 7.2 Quản lý rủi ro và giải quyết phát sinh.
- 7.3 Đánh giá mức độ hoàn thành nhiệm vụ và đóng góp của 4 thành viên.
