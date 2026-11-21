---
id: T002
title: Làm sạch, xử lý thiếu, kiểm rò rỉ và chia tập
phase: P2
checklist: 2.2, 2.3
owner: duc
status: todo
due: 05/12/2026
files: src/data_prep.py
depends: T001
---
# T002 — Làm sạch, xử lý thiếu, kiểm rò rỉ và chia tập

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Xử lý các ký tự khuyết thiếu '?', điền giá trị khuyết thiếu cho chuỗi thời gian, tạo đặc trưng thời gian và `Sub_metering_remainder`, kiểm tra rò rỉ thông tin của `Global_intensity`, chia tập train/test theo thời gian và lưu `data/clean/household_power_clean.csv`.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DUC.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Không được làm
- Không chia tập ngẫu nhiên làm rò rỉ tương quan thời gian.
- Không đưa `Global_intensity` vào tập đặc trưng huấn luyện.

## Xong khi
- Tạo thành công bảng chất lượng dữ liệu trước/sau và bảng kiểm tra rò rỉ.
- `python -m pytest tests/test_duc_modules.py` xanh.

## Kết quả (người làm điền)
