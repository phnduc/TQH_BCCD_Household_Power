# CHECKLIST — Tiến độ công việc theo Phase (chỉ Đức sửa)

Mã công việc khớp với Rubric chấm điểm học phần Phân tích và trực quan hóa dữ liệu (004759), tổng 10,0 điểm (nhóm 8,5 điểm + cá nhân 1,5 điểm).
Nhóm gồm 4 thành viên: Đức, Sơn, Duy, DA.

## P1 — Hết tuần 1: Thành lập nhóm, khảo sát dữ liệu phụ tải (Khối A)
| Mã | Việc | Điểm | Người chính | Trạng thái |
|---|---|---|---|---|
| 1.1 | Bối cảnh lưới điện thông minh, bài toán dự báo phụ tải hộ gia đình, ≥ 3 câu hỏi phân tích; lựa chọn quy trình CRISP-DM/KDD | 0,5 | Đức, Duy | ☐ |
| — | Phiếu đăng ký (Phụ lục A), kế hoạch và phân tích rủi ro (Phụ lục B) vào `docs/PROJECT_RECORDS.md` | (6.1) | Đức | ☐ |
| — | Tải dữ liệu UCI Household Power, kiểm tra cấu trúc cột, điền SHA-256 vào `src/config.py` | — | Đức | ☐ |

## P2 — Hết tuần 2: Tiền xử lý, EDA và khai phá luật kết hợp (Khối B, C, D)
| Mã | Việc | Điểm | Người chính | Trạng thái |
|---|---|---|---|---|
| 2.1 | Từ điển dữ liệu, thống kê mô tả các biến đo công suất và phân hệ Sub_metering | 0,25 | Sơn | ☐ |
| 2.2 | Làm sạch dữ liệu, xử lý giá trị thiếu '?', lọc giá trị vô lý, kiểm tra rò rỉ giữa Global_intensity và Global_active_power, báo cáo trước/sau | 0,5 | Đức | ☐ |
| 2.3 | Tạo đặc trưng thời gian (giờ, thứ, ngày nghỉ), tính Sub_metering_remainder, giảm chiều PCA và xếp hạng thuộc tính, lưu dữ liệu sạch | 0,25 | Đức, Duy | ☐ |
| 3.1 | Biểu đồ phân bố công suất theo mức phụ tải, heatmap phụ tải Giờ x Thứ trong tuần | 0,5 | Sơn | ☐ |
| 3.2 | Biểu đồ tán xạ quan hệ giữa các phân hệ điện năng, ma trận tương quan giữa các biến | 0,5 | Sơn, Duy | ☐ |
| 4.1 | Khối D: Khai phá luật kết hợp Apriori/FP-growth, lọc luật có vế phải là Load_Level, diễn giải ≥ 5 luật | 0,5 | Duy | ☐ |

## P3 — Hết tuần 3: Mô hình học máy, phân cụm và kiểm thử (Khối E, F, G)
| Mã | Việc | Điểm | Người chính | Trạng thái |
|---|---|---|---|---|
| 4.2 | Khối E: Phân lớp mức phụ tải ≥ 3 mô hình; hồi quy dự báo công suất; kiểm định chéo K-Fold; so sánh có/không có PCA | 0,5 | DA, Duy | ☐ |
| 4.3 | Khối F: Phân cụm k-means hồ sơ phụ tải ngày, chọn k bằng Elbow và Silhouette, đối chiếu cụm với mức phụ tải | 0,5 | DA | ☐ |
| 4.4 | Chia tập theo thời gian tránh rò rỉ, tinh chỉnh siêu tham số mô hình với GridSearchCV | 0,5 | Đức, DA | ☐ |
| 3.3 | Trực quan hóa kết quả mô hình: Ma trận nhầm lẫn, biểu đồ cụm phụ tải, độ quan trọng thuộc tính | 0,5 | Sơn | ☐ |
| 5.1 | Xây dựng bảng ca kiểm thử phần mềm (Phụ lục D: mã ca KT01..KT05, mục tiêu, kết quả mong đợi/thực tế) | 0,5 | Sơn | ☐ |
| 5.2 | Đánh giá độ đo phù hợp: Accuracy, Precision, Recall, F1 macro; MAE, RMSE, R² và bảng so sánh mô hình | 0,5 | DA | ☐ |
| 5.3 | Phân tích lỗi dự báo theo khung giờ và loại ngày; thử nghiệm bổ sung đặc trưng trễ (lags); trả lời câu hỏi phân tích | 0,5 | DA, Đức | ☐ |

## P4 — Hết tuần 4: Hoàn thiện báo cáo, slide và đóng gói sản phẩm
| Mã | Việc | Điểm | Người chính | Trạng thái |
|---|---|---|---|---|
| 3.4 | Toàn bộ biểu đồ (≥ 8 hình, ≥ 4 loại) có đầy đủ tiêu đề, nhãn trục, đơn vị, nhận xét sâu sắc | 0,5 | Sơn | ☐ |
| 6.1 | Kế hoạch làm việc nhóm, phân công nhiệm vụ, nhật ký tuần, bảng quản lý rủi ro | 0,75 | Đức | ☐ |
| 6.2 | Bảng tự đánh giá mức độ đóng góp cá nhân (Phụ lục C); lịch sử commit git phân định rõ người | 0,75 (cá nhân) | Cả nhóm | ☐ |
| 7.1 | Báo cáo thuyết minh hoàn chỉnh 20–30 trang (Times New Roman 13, giãn 1,3), trích dẫn tài liệu chuẩn APA/IEEE | 0,5 | Cả nhóm | ☐ |
| 7.2 | Slide thuyết trình 10–12 trang; kịch bản thuyết trình và kịch bản demo chạy mã nguồn tự động `run_all.py` | 0,25 | Sơn, Cả nhóm | ☐ |
| — | Đóng gói sản phẩm nộp `D18CNPM1_Nhom_HouseholdPower.zip` (báo cáo, slide, mã nguồn, dữ liệu sạch, hồ sơ nhóm) | — | Đức | ☐ |

## P5 — Buổi thi và vấn đáp
| Mã | Việc | Điểm | Phụ trách | Trạng thái |
|---|---|---|---|---|
| 7.3 | Vấn đáp cá nhân: Mỗi thành viên trả lời độc lập các câu hỏi về phần việc của mình và bài toán chung | 0,75 (cá nhân) | Mỗi người | ☐ |
