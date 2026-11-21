# HỒ SƠ LÀM VIỆC NHÓM (Phụ lục A, B, C; chủ: Đức)

Hồ sơ quản lý dự án học phần Phân tích và trực quan hóa dữ liệu (004759).

## Phụ lục A — Phiếu đăng ký đề tài
| Mục | Thông tin chi tiết |
|---|---|
| Lớp và tên nhóm | Lớp D18CNPM1 — Nhóm gồm 4 thành viên: Đức, Sơn, Duy, DA |
| Tên đề tài | **Phân tích và dự báo phụ tải điện hộ gia đình** |
| Dữ liệu và nguồn | UCI Individual Household Electric Power Consumption, đo đếm theo phút trong 47 tháng tại Pháp |
| Câu hỏi phân tích 1 | Xu hướng tiêu thụ phụ tải điện biến động như thế nào theo khung giờ trong ngày, ngày làm việc so với ngày cuối tuần, và các mùa trong năm? |
| Câu hỏi phân tích 2 | Các phân hệ thiết bị trong nhà (bếp, giặt là, điều hòa/nóng lạnh) đóng góp ra sao vào công suất đỉnh (Peak Load), và có những luật kết hợp nào giữa hành vi sử dụng thiết bị với phụ tải cao điểm? |
| Câu hỏi phân tích 3 | Các mô hình học máy đạt độ chính xác dự báo công suất tác dụng (kW) và khả năng nhận diện chế độ phụ tải (Thấp, Bình thường, Cao điểm) ở mức độ nào? |

### Danh sách thành viên và phân công vai trò
| STT | Họ và tên | Mã sinh viên | Vai trò | Trách nhiệm chính |
|---|---|---|---|---|
| 1 | Phan Đức | 23810310001 | Trưởng nhóm | Điều phối, tiền xử lý dữ liệu, cấu hình hệ thống, pipeline `run_all.py`, Chương 1, 4.1, 7 |
| 2 | Nguyễn Hoàng Sơn | 23810310002 | Thành viên | Trực quan hóa EDA (Khối C), từ điển dữ liệu, bảng kiểm thử (Phụ lục D), slide thuyết trình |
| 3 | Trần Khắc Duy | 23810310003 | Thành viên | Khai phá luật kết hợp (Khối D), giảm chiều PCA và xếp hạng thuộc tính, Chương 3 báo cáo |
| 4 | Đặng Đức Anh (DA) | 23810310004 | Thành viên | Phân cụm k-means (Khối F), mô hình phân lớp & hồi quy dự báo phụ tải (Khối E), đánh giá lỗi (Khối G), Chương 5 & 6 |

## Phụ lục B — Kế hoạch tiến độ và quản lý rủi ro
Kế hoạch triển khai trong 4 tuần:

| Mốc | Thời gian | Nhiệm vụ hoàn thành | Sản phẩm đầu ra |
|---|---|---|---|
| M1 | Hết tuần 1 | Khởi tạo repo, tải và đối chiếu dữ liệu, hoàn thành Khối A, Phụ lục A & B | Dữ liệu thô tải thành công, `config.py` và `test_repo_structure` xanh |
| M2 | Hết tuần 2 | Hoàn thành Khối B, C, D: Làm sạch dữ liệu, xử lý thiếu, vẽ biểu đồ EDA, khai phá luật Apriori | Báo cáo tiến độ 1, dữ liệu sạch `data/clean/`, hình ảnh EDA |
| M3 | Hết tuần 3 | Hoàn thành Khối E, F, G: Huấn luyện mô hình phân lớp & hồi quy, phân cụm k-means, bảng kiểm thử | Báo cáo tiến độ 2, bảng số liệu kết quả mô hình trong `results/tables/` |
| M4 | Hết tuần 4 | Ghép toàn bộ báo cáo 20–30 trang, thiết kế slide 10–12 trang, chạy thử nghiệm `run_all.py` | Báo cáo PDF & DOCX, Slide PowerPoint/PDF, tệp nén nộp bài |

### Bảng quản lý rủi ro
| Rủi ro tiềm ẩn | Khả năng | Mức ảnh hưởng | Giải pháp phòng ngừa & xử lý | Người theo dõi |
|---|---|---|---|---|
| Rò rỉ dữ liệu làm sai lệch kết quả mô hình | Cao | Nghiêm trọng | Loại bỏ `Global_intensity` (tương quan $>0.99$), chia tập train/test theo thứ tự thời gian | Đức |
| Dữ liệu có nhiều giá trị thiếu '?' | Đã xác định | Trung bình | Sử dụng kỹ thuật forward-fill kết hợp backward-fill cho chuỗi thời gian | Đức |
| Lỗi lệch nhãn phân lớp mức phụ tải | Trung bình | Trung bình | Chia tam phân vị cân bằng (mỗi lớp ~33.3%), dùng độ đo F1 macro | DA |
| Trùng lặp mã nguồn hoặc xung đột git | Thấp | Cao | Phân chia file sở hữu độc lập (TEAM.md mục 3), chỉ merge qua PR có review | Đức |

## Phụ lục C — Bảng tự đánh giá mức độ đóng góp cá nhân
(Cả 4 thành viên xác nhận trước khi nộp bài chính thức)

| STT | Họ và tên | Phần việc đã đảm nhiệm | Tỷ lệ đóng góp (%) | Chữ ký xác nhận |
|---|---|---|---|---|
| 1 | Phan Đức | Điều phối chung, Tiền xử lý dữ liệu, Quản lý cấu hình, Pipeline | 25% | Đã ký |
| 2 | Nguyễn Hoàng Sơn | Trực quan hóa dữ liệu EDA, Bảng ca kiểm thử, Thiết kế Slide | 25% | Đã ký |
| 3 | Trần Khắc Duy | Khai phá luật kết hợp, Giảm chiều PCA, Soạn Chương 3 | 25% | Đã ký |
| 4 | Đặng Đức Anh (DA) | Phân cụm k-means, Huấn luyện mô hình, Đánh giá phân tích lỗi, Chương 5-6 | 25% | Đã ký |
| **Tổng cộng** | | | **100%** | |
