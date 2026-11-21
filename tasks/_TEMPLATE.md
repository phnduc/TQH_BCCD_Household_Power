---
id: T000
title: Tiêu đề ngắn của task
phase: P1
checklist: 1.1
owner: duc
status: todo
due: TBD
files: src/ten_file.py
depends: -
---
# T000 — Tiêu đề ngắn của task

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
(1–3 dòng: task này tạo ra cái gì, phục vụ mục checklist nào.)

## Đầu vào cần đọc
- `TEAM.md`, `docs/<TÊN>.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Không được làm
- Không sửa file ngoài `files:`.
- Không tự đặt thông số ngoài `src/config.py`; thiếu thông số thì ghi vào task và báo Đức.

## Xong khi
- Hoàn thành đầy đủ yêu cầu kiểm tra được.
- `python -m pytest` không có test đỏ.

## Kết quả (người làm điền)
(Đã làm gì, lệnh đã chạy, kết quả test/số liệu, chỗ còn dở hoặc không chắc.)
