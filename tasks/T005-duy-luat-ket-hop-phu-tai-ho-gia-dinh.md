---
id: T005
title: Khai phá luật kết hợp phụ tải hộ gia đình
phase: P2
checklist: 4.1
owner: duy
status: todo
due: 05/12/2026
files: src/assoc.py
depends: T002
---
# T005 — Khai phá luật kết hợp phụ tải hộ gia đình

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Rời rạc hóa khung giờ và trạng thái thiết bị tiêu thụ, áp dụng Apriori tìm các luật kết hợp dẫn đến phụ tải cao điểm (`Peak_Load`), diễn giải ý nghĩa nghiệp vụ của ≥ 5 luật.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DUY.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Xong khi
- Sinh ra bảng luật kết hợp lọc theo lift và confidence; diễn giải được ý nghĩa trong báo cáo.

## Kết quả (người làm điền)
