# TỪ ĐIỂN DỮ LIỆU (Chủ: Sơn)

Tập dữ liệu: UCI Individual Household Electric Power Consumption.
Đo đếm điện năng tiêu thụ thực tế tại hộ gia đình (Sceaux, ngoại ô Paris, Pháp).

| Tên cột | Ý nghĩa nghiệp vụ | Kiểu dữ liệu | Đơn vị | Khoảng giá trị | Vai trò |
|---|---|---|---|---|---|
| `Date` | Ngày đo đếm điện năng | Chuỗi (dd/mm/yyyy) | Ngày | 16/12/2006 – 26/11/2010 | Định danh thời gian |
| `Time` | Giờ phút giây đo đếm | Chuỗi (hh:mm:ss) | Giờ:Phút:Giây | 00:00:00 – 23:59:00 | Định danh thời gian |
| `Global_active_power` | Tổng công suất tác dụng trung bình mỗi phút toàn hộ | Số thực (float) | Kilowatt (kW) | 0.076 – 11.122 | **Đích hồi quy** (dự báo công suất) |
| `Global_reactive_power` | Tổng công suất phản kháng trung bình mỗi phút | Số thực (float) | Kilowatt (kW) | 0.000 – 1.390 | Đặc trưng đầu vào |
| `Voltage` | Điện áp lưới điện trung bình mỗi phút | Số thực (float) | Volt (V) | 223.2 – 254.15 (chuẩn ~230V) | Đặc trưng đầu vào |
| `Global_intensity` | Cường độ dòng điện trung bình mỗi phút | Số thực (float) | Ampere (A) | 0.2 – 48.4 | **Rò rỉ (Leaky)** -> LOẠI KHỎI MÔ HÌNH |
| `Sub_metering_1` | Điện năng tiêu thụ tại bếp (máy rửa bát, lò vi sóng) | Số thực (float) | Watt-giờ (Wh) | 0 – 88 | Đặc trưng đầu vào |
| `Sub_metering_2` | Điện năng phòng giặt (máy giặt, máy sấy, tủ lạnh) | Số thực (float) | Watt-giờ (Wh) | 0 – 80 | Đặc trưng đầu vào |
| `Sub_metering_3` | Điện năng bình nước nóng và điều hòa không khí | Số thực (float) | Watt-giờ (Wh) | 0 – 31 | Đặc trưng đầu vào |
| `Sub_metering_remainder` | Năng lượng tiêu thụ khác ngoài 3 phân hệ đo (tính toán) | Số thực (float) | Watt-giờ (Wh) | 0 – 120 | Đặc trưng đầu vào (tự sinh) |
| `hour` | Giờ trong ngày (0 đến 23) | Số nguyên (int) | Giờ | 0 – 23 | Đặc trưng thời gian |
| `month` | Tháng trong năm (1 đến 12) | Số nguyên (int) | Tháng | 1 – 12 | Đặc trưng thời gian |
| `day_of_week` | Thứ trong tuần (Monday .. Sunday) | Chuỗi (str) | Thứ | 7 ngày | Đặc trưng phân loại |
| `is_weekend` | Cờ nhận biết ngày cuối tuần (1: Thứ 7/CN, 0: Ngày thường) | Số nguyên (int) | Nhị phân | 0 hoặc 1 | Đặc trưng phân loại |
| `Load_Level` | Mức phụ tải tiêu thụ điện | Chuỗi (str) | Phân loại | Low_Load, Normal_Load, Peak_Load | **Đích phân lớp** |
| `is_outlier` | Cờ phát hiện bất thường/ngoại lai theo IQR | Logic (bool) | Boolean | True / False | Cờ kiểm tra chất lượng |
