"""Validate that unresolved markers in release-critical files are registered."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

TODO_DIR = Path("docs/todo")
REGISTER_NAME = "unresolved_item_register.csv"
ALLOWLIST_NAME = "todo_allowlist.yaml"

# Markers that require registration when found outside docs/todo/.
# Do not treat stable register IDs (TODO-MAN-001, TODO-SRC-001, …) as open TODOs.
# TODO/FIXME/XXX are case-sensitive (uppercase) so paths like docs/todo/ do not match.
MARKER_RE = re.compile(
    r"(?P<m>"
    r"\\todo\{[^}]+\}|"
    r"(?<![\w-])TODO(?!-[A-Z]+-\d+)(?![\w/])|"
    r"(?<![\w-])FIXME(?![\w/])|"
    r"(?<![\w-])XXX(?![\w/])|"
    r"(?i:CITATION NEEDED)|"
    r"(?i:SOURCE NEEDED)|"
    r"(?i:DECISION NEEDED)|"
    r"\[VERIFY[^\]]*\]|"
    r"\[INSERT[^\]]*\]|"
    r"\[CONFIRM[^\]]*\]|"
    r"(?i:RESULTS PLACEHOLDER)|"
    r"(?i:DISCUSSION PLACEHOLDER)|"
    r"(?i:CONCLUSION PLACEHOLDER)"
    r")"
)

# Legitimate scientific vocabulary — do not fail solely on these words
BENIGN_RE = re.compile(
    r"\b(pending|provisional|incomplete|blocked|hold|no_go|not yet)\b",
    re.IGNORECASE,
)


def _load_allowlist(root: Path) -> dict:
    path = root / TODO_DIR / ALLOWLIST_NAME
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_register(root: Path) -> list[dict[str, str]]:
    path = root / TODO_DIR / REGISTER_NAME
    if not path.exists():
        return []
    return read_csv(path)


def _path_allowed(rel: str, entry_paths: list[str]) -> bool:
    rel_n = rel.replace("\\", "/")
    for p in entry_paths:
        p_n = p.replace("\\", "/").rstrip("/")
        if rel_n == p_n or rel_n.startswith(p_n + "/"):
            return True
    return False


def _is_excluded(rel: str, exclude_globs: list[str]) -> bool:
    from fnmatch import fnmatch

    rel_n = rel.replace("\\", "/")
    for g in exclude_globs:
        g_n = g.replace("\\", "/")
        if fnmatch(rel_n, g_n) or fnmatch(rel_n, g_n.rstrip("/**") + "/**"):
            return True
        # prefix directory exclude
        if g_n.endswith("/**") and rel_n.startswith(g_n[:-3]):
            return True
        if g_n.endswith("/**") is False and (
            rel_n == g_n or rel_n.startswith(g_n.rstrip("*").rstrip("/"))
        ):
            if "*" not in g_n and (rel_n == g_n or rel_n.startswith(g_n + "/")):
                return True
    # Always exclude the todo register itself
    if rel_n.startswith("docs/todo/"):
        return True
    return False


def _match_allowlisted(
    rel: str, marker: str, allow_entries: list[dict]
) -> str | None:
    """Return todo_id if marker is allowlisted for this path."""
    for entry in allow_entries:
        if entry.get("status") == "resolved_documented":
            continue
        paths = entry.get("paths") or []
        if not _path_allowed(rel, paths):
            continue
        markers = entry.get("markers") or []
        if not markers:
            continue
        for m in markers:
            if m.lower() in marker.lower() or marker.lower() in m.lower():
                return str(entry.get("todo_id", "unknown"))
    return None


def _iter_release_critical(root: Path, globs: list[str]) -> list[Path]:
    from fnmatch import fnmatch

    files: list[Path] = []
    skip_parts = {".git", ".venv", "__pycache__", "node_modules", "_generated", "local_sources"}
    text_suffixes = {
        ".md",
        ".csv",
        ".txt",
        ".yaml",
        ".yml",
        ".py",
        ".cff",
        ".tex",
        ".json",
    }
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix.lower() not in text_suffixes and path.name != "CITATION.cff":
            continue
        rel = path.relative_to(root).as_posix()
        if globs and not any(fnmatch(rel, g) for g in globs):
            continue
        files.append(path)
    return files


def validate_register_schema(root: Path, report: ValidationReport) -> None:
    rows = _load_register(root)
    if not rows:
        report.add(f"missing or empty {TODO_DIR / REGISTER_NAME}")
        return
    required = {
        "todo_id",
        "category",
        "priority",
        "current_status",
        "blocking_gate",
        "release_blocking",
        "manuscript_blocking",
    }
    missing = required - set(rows[0].keys())
    if missing:
        report.add(f"register missing columns: {sorted(missing)}")
    ids = [r.get("todo_id", "") for r in rows]
    if len(ids) != len(set(ids)):
        report.add("register contains duplicate todo_id values")
    # P0 items must not be silently marked resolved without resolution text
    for i, row in enumerate(rows, start=2):
        if row.get("priority") == "P0" and row.get("current_status") == "resolved":
            if not (row.get("resolution") or "").strip():
                report.add(f"register:{i}: P0 resolved without resolution text")


def validate_forbidden_patterns(
    root: Path, report: ValidationReport, allow: dict
) -> None:
    patterns = [re.compile(p, re.I) for p in (allow.get("forbidden_patterns") or [])]
    if not patterns:
        return
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {
            ".md",
            ".csv",
            ".txt",
            ".yaml",
            ".yml",
            ".py",
            ".cff",
            ".tex",
        }:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith("docs/todo/"):
            continue
        if any(p in path.parts for p in (".git", ".venv", "__pycache__", "local_sources")):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for pat in patterns:
                if pat.search(line):
                    report.add(f"{rel}:{i}: forbidden pattern {pat.pattern!r}: {line.strip()[:120]}")


def validate_unregistered_markers(
    root: Path, report: ValidationReport, allow: dict
) -> None:
    exclude = list(allow.get("exclude_globs") or [])
    globs = list(allow.get("release_critical_globs") or [])
    entries = list(allow.get("entries") or [])
    for path in _iter_release_critical(root, globs):
        rel = path.relative_to(root).as_posix()
        if _is_excluded(rel, exclude):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        # Do not scan the scanner or its unit tests (patterns are intentional).
        if rel in {
            "src/school_security_audit/validate_todos.py",
            "tests/test_todos.py",
        }:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for match in MARKER_RE.finditer(line):
                marker = match.group("m")
                if "MARKER_RE" in line or "re.compile" in line:
                    continue
                todo_id = _match_allowlisted(rel, marker, entries)
                if todo_id:
                    continue
                if re.search(r"TODO-[A-Z]+-\d+", marker):
                    continue
                report.add(
                    f"{rel}:{i}: unregistered unresolved marker {marker!r} "
                    f"(add to docs/todo/todo_allowlist.yaml + register)"
                )


def validate_p0_p1_transparency(root: Path, report: ValidationReport) -> None:
    """P0/P1 blocked items must remain listed as blocked in the register."""
    for row in _load_register(root):
        pri = row.get("priority", "")
        status = row.get("current_status", "")
        cat = row.get("category", "")
        if pri in {"P0", "P1"} and cat.startswith("BLOCKED_") and status == "resolved":
            report.add(
                f"{row.get('todo_id')}: P0/P1 blocked category marked resolved "
                f"without category change — refuse silent blocker removal"
            )


def validate_todos(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()
    allow = _load_allowlist(root)
    if not allow:
        report.add(f"missing {TODO_DIR / ALLOWLIST_NAME}")
        return report
    validate_register_schema(root, report)
    validate_p0_p1_transparency(root, report)
    validate_forbidden_patterns(root, report, allow)
    validate_unregistered_markers(root, report, allow)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: package REPO_ROOT)",
    )
    args = parser.parse_args(argv)
    report = validate_todos(args.root)
    if report.ok:
        print("TODO-register validation OK.")
        return 0
    print("TODO-register validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
