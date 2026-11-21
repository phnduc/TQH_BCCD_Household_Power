---
id: T006
title: Giảm chiều PCA và xếp hạng thuộc tính
phase: P2
checklist: 2.3
owner: duy
status: todo
due: 05/12/2026
files: src/reduce.py
depends: T002
---
# T006 — Giảm chiều PCA và xếp hạng thuộc tính

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Cài đặt PCA giữ phương sai tích lũy tối thiểu (khớp trên train), xếp hạng độ quan trọng của các thuộc tính phụ tải đối với công suất tiêu thụ điện.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DUY.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Xong khi
- Hàm `pca_reduce` và `rank_features` chạy đúng giao diện và xuất kết quả xếp hạng.

## Kết quả (người làm điền)
