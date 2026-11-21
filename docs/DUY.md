# DUY — Trần Khắc Duy

Nhánh: `duy-assoc-reduce`. Đọc `TEAM.md` trước.

## Phần của bạn
- **Khối D Mẫu thường xuyên & Luật kết hợp (`src/assoc.py`):**
  - Rời rạc hóa các đại lượng đo lường phụ tải và trạng thái thiết bị thành dạng giao dịch.
  - Cài đặt thuật toán Apriori hoặc FP-growth, khai phá các luật có vế phải liên quan đến mức phụ tải cao điểm.
  - Diễn giải ý nghĩa thực tế của $\ge 5$ luật tiêu biểu; viết mục 4.3 báo cáo.
- **Giảm chiều dữ liệu & Xếp hạng thuộc tính (`src/reduce.py`):**
  - Cài đặt PCA giảm chiều dữ liệu (khớp trên train).
  - Xếp hạng độ quan trọng của các thuộc tính phụ tải đối với mức tiêu thụ điện năng; viết mục 4.4 báo cáo.
  - Thực hiện thử nghiệm so sánh hiệu năng mô hình có và không có PCA.
- **Báo cáo:** Viết Chương 3 báo cáo (Thiết kế sơ bộ quy trình CRISP-DM, kiến trúc và độ đo).

## Tiêu chí chấm chính
1.1 (Chương 3), 2.3 (giảm chiều), 4.1 (luật kết hợp), 4.2 (so sánh PCA).
