"""Kiểm tra không có hằng số 'ma thuật' trong src/.

Quét AST của các file Python trong src/ (trừ config.py), báo lỗi nếu có hằng số ma thuật.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

MAGIC_NUMBERS = {4759, 1.5, 0.2}
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}")

ROOT = Path(__file__).resolve().parents[1]


def find_magic(source: str) -> list[tuple[int, str]]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent

    docstring_node_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr):
                expr = node.body[0]
                if isinstance(expr.value, ast.Constant) and isinstance(expr.value.value, str):
                    docstring_node_ids.add(id(expr.value))

    def is_in_print_fstring(node: ast.AST) -> bool:
        curr = node
        in_joined_str = False
        while hasattr(curr, "parent"):
            curr = curr.parent
            if isinstance(curr, ast.JoinedStr):
                in_joined_str = True
            elif in_joined_str and isinstance(curr, ast.Call):
                func = curr.func
                if isinstance(func, ast.Name) and func.id == "print":
                    return True
                if isinstance(func, ast.Attribute) and func.attr in (
                    "write", "debug", "info", "warning", "error", "critical", "log"
                ):
                    return True
        return False

    violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue
        if id(node) in docstring_node_ids:
            continue
        if is_in_print_fstring(node):
            continue

        val = node.value
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            is_magic = False
            if val in MAGIC_NUMBERS:
                is_magic = True
            elif isinstance(val, float) and any(abs(val - m) < 1e-9 for m in (0.2, 1.5)):
                is_magic = True
            if is_magic:
                violations.append((node.lineno, f"Phát hiện số ma thuật {val} tại dòng {node.lineno}: lấy từ src/config.py"))
        elif isinstance(val, str) and DATE_REGEX.match(val):
            violations.append((node.lineno, f"Phát hiện chuỗi ngày {val} tại dòng {node.lineno}: lấy từ src/config.py"))

    return violations


def test_no_magic_numbers_in_src():
    src_dir = ROOT / "src"
    all_violations = {}
    for p in src_dir.glob("*.py"):
        if p.name in ("config.py", "__init__.py"):
            continue
        violations = find_magic(p.read_text(encoding="utf-8"))
        if violations:
            all_violations[p.name] = violations
    assert not all_violations, f"Vi phạm số ma thuật: {all_violations}"
