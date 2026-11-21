"""Kiểm tra môi trường làm việc (Đề tài Phân tích và dự báo phụ tải điện hộ gia đình).

Chạy: python scripts/doctor.py
Mức import đầu file chỉ dùng thư viện chuẩn. Thoát mã 1 nếu có LỖI; CẢNH BÁO không làm thoát lỗi.
"""
from __future__ import annotations

import hashlib
import importlib
import os
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Bảng phân công 4 thành viên và nhánh tương ứng (TEAM.md mục 1)
BRANCH_USER = {
    "duc-lead-data-models": "Phan Duc",
    "son-viz-testcases": "Nguyen Hoang Son",
    "duy-assoc-reduce": "Tran Khac Duy",
    "da-cluster-models-eval": "Dang Duc Anh",
}

IMPORT_NAMES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "scikit-learn": "sklearn",
    "mlxtend": "mlxtend",
    "statsmodels": "statsmodels",
    "networkx": "networkx",
    "pytest": "pytest",
}


class Doctor:
    def __init__(self) -> None:
        self.passes = self.warnings = self.errors = 0

    def ok(self, msg: str) -> None:
        self.passes += 1
        print(f"[ĐẠT] {msg}")

    def warn(self, msg: str, hint: str) -> None:
        self.warnings += 1
        print(f"[CẢNH BÁO] {msg} -> {hint}")

    def error(self, msg: str, hint: str) -> None:
        self.errors += 1
        print(f"[LỖI] {msg} -> {hint}")


def git(*args: str) -> str | None:
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:  # noqa: BLE001
        return None


def check_python(d: Doctor) -> None:
    v = sys.version_info
    if (v.major, v.minor) == (3, 12):
        d.ok(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        d.warn(f"Python {v.major}.{v.minor}.{v.micro}, khuyến nghị dùng 3.12", "cài Python 3.12 để đảm bảo đồng nhất")


def check_venv(d: Doctor) -> None:
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        d.ok("Đang chạy trong môi trường ảo (.venv)")
    else:
        d.warn("Không ở trong .venv", "kích hoạt môi trường ảo trước khi chạy")
    if os.environ.get("PYTHONUTF8") == "1":
        d.ok("PYTHONUTF8=1")
    else:
        d.warn("PYTHONUTF8 chưa đặt", "Linux/Mac: export PYTHONUTF8=1, Windows: $env:PYTHONUTF8=1")


def check_dependencies(d: Doctor) -> None:
    req = ROOT / "requirements.txt"
    if not req.exists():
        d.error("Thiếu requirements.txt", "tạo tệp requirements.txt")
        return
    pinned: dict[str, str] = {}
    for line in req.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "==" in line:
            name, ver = line.split("==", 1)
            pinned[name.strip().lower()] = ver.strip()

    for pkg, ver in pinned.items():
        mod = IMPORT_NAMES.get(pkg, pkg.replace("-", "_"))
        try:
            m = importlib.import_module(mod)
            got = getattr(m, "__version__", "?")
            d.ok(f"Thư viện {pkg}: phiên bản cài {got}")
        except ImportError:
            d.error(f"Thiếu thư viện {pkg}", "chạy: pip install -r requirements.txt")


def check_git(d: Doctor) -> None:
    br = git("branch", "--show-current")
    if not br:
        d.warn("Không phát hiện repo git hoặc đang detached HEAD", "kiểm tra git status")
        return
    d.ok(f"Nhánh hiện tại: {br}")
    user = git("config", "user.name")
    if not user:
        d.warn("Chưa cấu hình git user.name", 'chạy: git config user.name "Họ và Tên"')
    else:
        d.ok(f"Git user.name: {user}")
        if br in BRANCH_USER and BRANCH_USER[br].lower() != user.lower():
            d.warn(f"Nhánh {br} nhưng user.name là {user} (kỳ vọng {BRANCH_USER[br]})", "đối chiếu TEAM.md")


def check_data(d: Doctor) -> None:
    from src import config
    raw = config.RAW_DIR / config.DATA_LOCAL_NAME
    if raw.exists():
        d.ok(f"Đã có tệp dữ liệu thô: {raw.name} ({raw.stat().st_size} bytes)")
    else:
        d.warn(f"Chưa có {raw.name}", "chạy: python data/download_data.py")


def main() -> int:
    print("=== KIỂM TRA MÔI TRƯỜNG DỰ ÁN (DOCTOR) ===")
    d = Doctor()
    check_python(d)
    check_venv(d)
    check_dependencies(d)
    check_git(d)
    check_data(d)
    print(f"\nTổng kết: {d.passes} ĐẠT, {d.warnings} CẢNH BÁO, {d.errors} LỖI.")
    return 1 if d.errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
