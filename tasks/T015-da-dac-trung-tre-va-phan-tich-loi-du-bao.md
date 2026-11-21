---
id: T015
title: Đặc trưng trễ và phân tích lỗi dự báo
phase: P3
checklist: 5.3
owner: da
status: todo
due: 12/12/2026
files: src/evaluate.py
depends: T007
---
# T015 — Đặc trưng trễ và phân tích lỗi dự báo

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Phân tích lỗi dự báo theo các khung giờ và loại ngày; đánh giá mức độ cải thiện khi đưa thêm các đặc trưng trễ (lag features 15p, 30p, 1h, 24h) vào bài toán hồi quy công suất.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DA.md`, `src/config.py`

## Xong khi
- Sinh bảng lỗi phân lớp theo giờ (`g_05`), theo ngày (`g_06`) và kết quả hồi quy kèm lags (`g_04`).

## Kết quả (người làm điền)
