---
id: T001
title: Tải dữ liệu và đối chiếu tên cột
phase: P1
checklist: 1.1
owner: duc
status: todo
due: 28/11/2026
files: data/download_data.py, src/config.py
depends: -
---
# T001 — Tải dữ liệu và đối chiếu tên cột

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Tải dữ liệu UCI Individual Household Electric Power Consumption vào `data/raw/`, kiểm tra số cột, tên cột, và cập nhật SHA-256 vào `src/config.py`.

## Đầu vào cần đọc
- `TEAM.md`, `docs/DUC.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Không được làm
- Không đẩy tệp dữ liệu thô > 100 MB lên git.
- Không tự đổi tên cột chuẩn của dữ liệu.

## Xong khi
- Tệp `data/raw/household_power_consumption.txt` tồn tại và đọc được.
- `python -m pytest tests/test_repo_structure.py` xanh.

## Kết quả (người làm điền)
