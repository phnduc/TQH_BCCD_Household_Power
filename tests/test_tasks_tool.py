"""Kiểm công cụ scripts/tasks.py trên thư mục tạm (không chạm tasks/ thật)."""
import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tasks_tool", ROOT / "scripts" / "tasks.py")
tt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tt)


def _setup(tmp_path):
    shutil.copy(ROOT / "tasks" / "_TEMPLATE.md", tmp_path / "_TEMPLATE.md")
    return str(tmp_path)


def _new(d, who, files, title="Cài đặt thử", depends="-"):
    return tt.main(["--dir", d, "new", "--who", who, "--phase", "P2", "--check", "B3.1",
                    "--due", "25/11/2026", "--files", files, "--depends", depends, title])


def test_new_and_ids(tmp_path):
    d = _setup(tmp_path)
    assert _new(d, "son", "src/viz.py") == 0
    assert _new(d, "duy", "src/assoc.py") == 0
    assert _new(d, "da", "src/clustering.py") == 0
    names = sorted(p.name for p in tmp_path.glob("T*.md"))
    assert names == ["T001-son-cai-dat-thu.md", "T002-duy-cai-dat-thu.md", "T003-da-cai-dat-thu.md"]
    assert tt.main(["--dir", d, "check"]) == 0


def test_set_status_and_list(tmp_path, capsys):
    d = _setup(tmp_path)
    _new(d, "son", "src/viz.py")
    assert tt.main(["--dir", d, "set", "T001", "status", "doing"]) == 0
    assert "status: doing" in (tmp_path / "T001-son-cai-dat-thu.md").read_text(encoding="utf-8")
    assert tt.main(["--dir", d, "set", "T001", "status", "xong"]) == 1
    capsys.readouterr()
    tt.main(["--dir", d, "list", "--status", "doing"])
    assert "T001" in capsys.readouterr().out
    tt.main(["--dir", d, "list", "--owner", "duy"])
    assert "T001" not in capsys.readouterr().out


def test_check_rejects_foreign_file(tmp_path, capsys):
    d = _setup(tmp_path)
    _new(d, "son", "src/assoc.py")
    assert tt.main(["--dir", d, "check"]) == 1
    assert "assoc.py" in capsys.readouterr().out
