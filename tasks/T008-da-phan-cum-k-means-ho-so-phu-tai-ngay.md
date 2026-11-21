---
id: T008
title: Phân cụm k-means hồ sơ phụ tải ngày
phase: P3
checklist: 4.3
owner: da
status: todo
due: 12/12/2026
files: src/clustering.py
depends: T002
---
# T008 — Phân cụm k-means hồ sơ phụ tải ngày

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Áp dụng k-means gom cụm các hồ sơ tiêu thụ điện hàng ngày, sử dụng phương pháp khuỷu tay và hệ số Silhouette để lựa chọn số cụm tối ưu, đối chiếu cụm với mức phụ tải thực tế.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DA.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Xong khi
- Sinh bảng chọn k và bảng chéo đối chiếu nhãn cụm với mức phụ tải.

## Kết quả (người làm điền)
