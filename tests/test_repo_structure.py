"""Cấu trúc nộp bài theo đề tài: thiếu thành phần nào thì test đỏ."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "TEAM.md",
    "requirements.txt",
    "run_all.py",
    "data/download_data.py",
    "src/config.py",
    "src/data_prep.py",
    "src/reduce.py",
    "src/viz.py",
    "src/assoc.py",
    "src/models.py",
    "src/clustering.py",
    "src/evaluate.py",
    "docs/CONVENTIONS.md",
    "docs/CHECKLIST.md",
]
REQUIRED_DIRS = ["notebooks", "results/figures", "results/tables", "tasks", "docs/decisions"]


def test_required_files_exist():
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    assert not missing, f"Thiếu tệp: {missing}"


def test_required_dirs_exist():
    missing = [p for p in REQUIRED_DIRS if not (ROOT / p).is_dir()]
    assert not missing, f"Thiếu thư mục: {missing}"


def test_raw_data_is_not_tracked():
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/raw/" in gi


def test_ai_entry_files_point_to_team():
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "TEAM.md" in text, f"{name} phải trỏ về TEAM.md"
        assert len(text.splitlines()) <= 20, f"{name} chỉ nên là con trỏ ngắn"
