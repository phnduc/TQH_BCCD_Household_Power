---
id: T007
title: Mô hình phân lớp và hồi quy dự báo phụ tải
phase: P3
checklist: 4.2, 4.4
owner: da
status: todo
due: 12/12/2026
files: src/models.py
depends: T002
---
# T007 — Mô hình phân lớp và hồi quy dự báo phụ tải

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Cài đặt và huấn luyện ≥ 3 mô hình phân lớp mức phụ tải (`DecisionTree`, `k-NN`, `LogisticRegression`) và 2 mô hình hồi quy dự báo công suất (`LinearRegression`, `DecisionTreeRegressor`), tinh chỉnh siêu tham số với `GridSearchCV`.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DA.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Xong khi
- Huấn luyện thành công, lưu kết quả CV và các mô hình tốt nhất vào `results/tables/`.

## Kết quả (người làm điền)
