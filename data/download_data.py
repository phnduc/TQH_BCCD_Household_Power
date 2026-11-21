"""Tải bộ dữ liệu UCI Individual Household Electric Power Consumption vào data/raw/ (chủ: Đức).

Chạy: python data/download_data.py
URL và kích thước được lấy từ src/config.py.
Nếu tải tự động gặp sự cố mạng, có thể tải thủ công từ link UCI rồi giải nén
và đặt tệp household_power_consumption.txt vào thư mục data/raw/.
"""
from __future__ import annotations

import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import config  # noqa: E402


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    dest = config.RAW_DIR / config.DATA_LOCAL_NAME
    if not dest.exists():
        print(f"Đang tải dữ liệu từ {config.DATA_URL}...")
        try:
            req = urllib.request.Request(
                config.DATA_URL,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                payload = r.read()
            with zipfile.ZipFile(io.BytesIO(payload)) as z:
                names = [n for n in z.namelist() if n.lower().endswith((".txt", ".csv"))]
                if not names:
                    print("Không thấy tệp dữ liệu trong gói zip:", z.namelist())
                    return 1
                dest.write_bytes(z.read(names[0]))
            print(f"Tải và giải nén thành công: {dest}")
        except Exception as exc:  # noqa: BLE001
            print(f"Tải tự động lỗi: {exc}")
            print(f"Vui lòng tải thủ công từ: {config.DATA_URL}")
            print(f"Giải nén và đặt tệp '{config.DATA_LOCAL_NAME}' vào thư mục '{config.RAW_DIR}'.")
            return 1

    size, digest = dest.stat().st_size, sha256_of(dest)
    print(f"{dest.name}: {size} bytes, sha256 = {digest}")
    if config.DATA_SHA256 is None:
        print("Ghi chú: Đức cập nhật DATA_SHA256 trong src/config.py sau khi xác thực.")
        return 0
    if digest != config.DATA_SHA256:
        print("CẢNH BÁO: SHA-256 không khớp với src/config.py")
        return 1
    print("Xác thực dữ liệu thành công.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
