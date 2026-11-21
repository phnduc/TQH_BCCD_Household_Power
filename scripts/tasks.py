"""Công cụ quản lý task: list | new | set | readme | check (chỉ dùng thư viện chuẩn)."""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"

KEYS = ["id", "title", "phase", "checklist", "owner", "status", "due", "files", "depends"]
OWNERS = ["duc", "son", "duy", "da"]
STATUSES = ["todo", "doing", "review", "done"]
PHASES = ["P1", "P2", "P3", "P4", "P5"]

OWNED = {
    "duc": [
        "src/config.py", "src/data_prep.py", "run_all.py",
        "data/download_data.py", "docs/", "tasks/", ".github/", "prompts/", "scripts/",
        "TEAM.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "requirements.txt",
        "pytest.ini", ".gitignore", ".gitattributes"
    ],
    "son": [
        "src/viz.py", "docs/DATA_DICTIONARY.md", "docs/TESTCASES.md",
        "docs/BAOCAO_DINH_DANG.md", "docs/SLIDE_NHAP.md", "notebooks/son_*"
    ],
    "duy": [
        "src/assoc.py", "src/reduce.py", "docs/BAOCAO_NHAP_DUY.md", "notebooks/duy_*"
    ],
    "da": [
        "src/clustering.py", "src/models.py", "src/evaluate.py",
        "docs/BAOCAO_NHAP_DA.md", "notebooks/da_*"
    ],
}

COMMON = [
    "docs/trace_{owner}.md", "results/figures", "results/figures/",
    "results/tables", "results/tables/", "tests/", "tasks/"
]
FORBIDDEN_ALL = ["tests/test_interfaces.py"]


def _match(path: str, pats: list) -> bool:
    for p in pats:
        if p.endswith("/"):
            if path.startswith(p) or path == p.rstrip("/"):
                return True
        elif fnmatch(path, p):
            return True
    return False


def path_allowed(owner: str, path: str):
    path = path.strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    if path in FORBIDDEN_ALL:
        return False, "là test dùng chung, không ai được sửa"
    common = [c.format(owner=owner) for c in COMMON]
    if _match(path, common) or _match(path, OWNED.get(owner, [])):
        return True, ""
    if any(_match(path, OWNED[o]) for o in OWNED if o != owner):
        return False, "thuộc quyền sở hữu của người khác"
    return False, "không nằm trong danh sách sở hữu (TEAM.md mục 3)"


def slugify(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40].strip("-") or "task"


def split_front(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            meta = {}
            for ln in lines[1:i]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    meta[k.strip()] = v.strip()
            return meta, "\n".join(lines[i + 1:])
    return None, text


def read_tasks(tdir: Path):
    out = []
    for p in sorted(tdir.glob("T[0-9]*.md")):
        meta, _ = split_front(p.read_text(encoding="utf-8"))
        out.append((p, meta))
    return out


def parse_due(s: str):
    if s.strip().upper() == "TBD":
        return datetime.max
    try:
        return datetime.strptime(s.strip(), "%d/%m/%Y")
    except ValueError:
        return datetime.max


def cmd_list(args):
    tdir = Path(args.dir) if args.dir else TASKS_DIR
    tasks = read_tasks(tdir)
    if args.owner:
        tasks = [t for t in tasks if t[1] and t[1].get("owner") == args.owner]
    if args.status:
        tasks = [t for t in tasks if t[1] and t[1].get("status") == args.status]
    if args.phase:
        tasks = [t for t in tasks if t[1] and t[1].get("phase") == args.phase]

    for p, meta in tasks:
        if not meta:
            print(f"LỖI cú pháp frontmatter: {p.name}")
            continue
        print(f"[{meta.get('id', '?')}] ({meta.get('owner', '?')} | {meta.get('status', '?')}) {meta.get('title', '')} (due: {meta.get('due', 'TBD')})")
    return 0


def cmd_set(args):
    tdir = Path(args.dir) if args.dir else TASKS_DIR
    target = None
    for p in tdir.glob(f"{args.task_id}*.md"):
        target = p
        break
    if not target:
        print(f"Không tìm thấy task {args.task_id}")
        return 1

    content = target.read_text(encoding="utf-8")
    meta, body = split_front(content)
    if not meta:
        print(f"Không đọc được frontmatter của {target.name}")
        return 1

    field = args.field.lower()
    if field == "status" and args.value not in STATUSES:
        print(f"Giá trị status '{args.value}' không hợp lệ. Phải là một trong: {STATUSES}")
        return 1

    meta[field] = args.value
    front = "---\n" + "\n".join(f"{k}: {meta.get(k, '')}" for k in KEYS if k in meta) + "\n---\n"
    target.write_text(front + body, encoding="utf-8")
    print(f"Đã cập nhật {field}={args.value} cho {target.name}")
    return 0


def cmd_check(args):
    tdir = Path(args.dir) if args.dir else TASKS_DIR
    tasks = read_tasks(tdir)
    errors = 0
    for p, meta in tasks:
        if not meta:
            print(f"[LỖI] {p.name}: Không đọc được frontmatter")
            errors += 1
            continue
        owner = meta.get("owner")
        if owner not in OWNERS:
            print(f"[LỖI] {p.name}: owner '{owner}' không hợp lệ")
            errors += 1
        files = [f.strip() for f in meta.get("files", "").split(",") if f.strip()]
        for f in files:
            ok, reason = path_allowed(owner, f)
            if not ok:
                print(f"[LỖI] {p.name}: File '{f}' không hợp lệ đối với {owner} ({reason})")
                errors += 1
    if errors == 0:
        print(f"Tất cả {len(tasks)} task đều hợp lệ!")
    return 0 if errors == 0 else 1


def cmd_readme(args):
    tdir = Path(args.dir) if args.dir else TASKS_DIR
    tasks = read_tasks(tdir)
    lines = [
        "# Task của nhóm",
        "",
        "1. Task do Đức tạo; thành viên không tự ý đổi nội dung giao việc.",
        "2. Tìm task có `owner` là bạn và `status: todo`, ưu tiên theo hạn (`due`).",
        "3. Chỉ sửa các file ghi ở dòng `files:` của task; thông số lấy từ `src/config.py`.",
        "4. Thành viên đổi `status` (todo → doing → review) và điền mục 'Kết quả'; Đức đặt `done` sau khi merge.",
        "5. Commit theo mẫu `T003 feat(b): ...`.",
        "",
    ]
    for ph in PHASES:
        ph_tasks = [t for t in tasks if t[1] and t[1].get("phase") == ph]
        if not ph_tasks:
            continue
        lines.append(f"## {ph}\n")
        lines.append("| id | owner | status | due | checklist | tiêu đề |")
        lines.append("|---|---|---|---|---|---|")
        for p, meta in ph_tasks:
            tid = meta.get("id", "")
            title = meta.get("title", "")
            lines.append(f"| {tid} | {meta.get('owner', '')} | {meta.get('status', '')} | {meta.get('due', 'TBD')} | {meta.get('checklist', '')} | [{title}]({p.name}) |")
        lines.append("")

    (tdir / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Đã cập nhật {tdir / 'README.md'}")
    return 0


def cmd_new(args):
    tdir = Path(args.dir) if args.dir else TASKS_DIR
    existing = [int(p.stem[1:4]) for p in tdir.glob("T[0-9][0-9][0-9]*.md") if p.stem[1:4].isdigit()]
    next_id = max(existing, default=0) + 1
    tid = f"T{next_id:03d}"
    slug = slugify(args.title)
    fname = f"{tid}-{args.who}-{slug}.md"
    fpath = tdir / fname

    content = f"""---
id: {tid}
title: {args.title}
phase: {args.phase}
checklist: {args.check}
owner: {args.who}
status: todo
due: {args.due}
files: {args.files}
depends: {args.depends}
---
# {tid} — {args.title}

> Đức tạo task. Người làm chỉ đổi `status` và điền mục "Kết quả". Chỉ sửa các file ghi ở `files:` ở trên.

## Mục tiêu
Task này cài đặt và thực hiện: {args.title}.

## Đầu vào cần đọc
- `TEAM.md`, `docs/{args.who.upper()}.md`, `docs/CONVENTIONS.md`, `src/config.py`

## Không được làm
- Không sửa file ngoài `files:`.
- Không tự đặt thông số ngoài `src/config.py`.

## Xong khi
- Hoàn thành đầy đủ các yêu cầu trong mục tiêu.
- `python -m pytest` không có test đỏ.

## Kết quả (người làm điền)
"""
    fpath.write_text(content, encoding="utf-8")
    print(f"Đã tạo task mới: {fpath.name}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Quản lý task dự án")
    parser.add_argument("--dir", help="Thư mục chứa tasks (mặc định: tasks/)")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list")
    p_list.add_argument("--owner", help="Lọc theo owner")
    p_list.add_argument("--status", help="Lọc theo status")
    p_list.add_argument("--phase", help="Lọc theo phase")

    p_set = sub.add_parser("set")
    p_set.add_argument("task_id", help="Mã task (ví dụ: T001)")
    p_set.add_argument("field", help="Tên trường (ví dụ: status)")
    p_set.add_argument("value", help="Giá trị mới")

    p_new = sub.add_parser("new")
    p_new.add_argument("--who", required=True, choices=OWNERS, help="Người làm")
    p_new.add_argument("--phase", required=True, choices=PHASES, help="Phase thực hiện")
    p_new.add_argument("--check", required=True, help="Mã checklist liên quan")
    p_new.add_argument("--due", default="TBD", help="Hạn hoàn thành (dd/mm/yyyy)")
    p_new.add_argument("--files", required=True, help="Danh sách file được sửa (phân cách bằng dấu phẩy)")
    p_new.add_argument("--depends", default="-", help="Phụ thuộc vào task nào")
    p_new.add_argument("title", help="Tiêu đề task")

    sub.add_parser("check")
    sub.add_parser("readme")

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0

    dispatch = {
        "list": cmd_list,
        "set": cmd_set,
        "check": cmd_check,
        "readme": cmd_readme,
        "new": cmd_new,
    }
    return dispatch[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
