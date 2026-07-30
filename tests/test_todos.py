"""Tests for the unresolved-item register and TODO validator."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_todos import MARKER_RE, validate_todos


def test_todo_validation_ok() -> None:
    report = validate_todos()
    assert report.ok, report.errors


def test_register_has_required_ids() -> None:
    rows = read_csv(REPO_ROOT / "docs/todo/unresolved_item_register.csv")
    ids = {r["todo_id"] for r in rows}
    for required in (
        "TODO-SRC-001",
        "TODO-FRZ-001",
        "TODO-PIL-001",
        "TODO-PRE-001",
        "TODO-MAN-014",
        "TODO-VAL-001",
    ):
        assert required in ids, required


def test_p0_source_blocker_still_blocked() -> None:
    rows = {
        r["todo_id"]: r
        for r in read_csv(REPO_ROOT / "docs/todo/unresolved_item_register.csv")
    }
    src = rows["TODO-SRC-001"]
    assert src["current_status"] == "blocked"
    assert src["category"] == "BLOCKED_BY_SOURCE_ACCESS"
    assert src["priority"] == "P0"


def test_register_ids_not_flagged_as_open_todos() -> None:
    text = "See TODO-SRC-001 and TODO-MAN-014 before freeze."
    assert MARKER_RE.search(text) is None
    assert MARKER_RE.search("TODO: fix this") is not None
    assert MARKER_RE.search(r"\todo{CITATION NEEDED: foo}") is not None


def test_reliability_policy_has_no_citation_todo() -> None:
    text = Path(REPO_ROOT / "docs/protocol/reliability_policy_v0.1.md").read_text(
        encoding="utf-8"
    )
    assert "CITATION NEEDED" not in text
    assert "Krippendorff" in text
    assert "≤ 15" in text or "<= 15" in text or "at most 15" in text.lower() or "≤15" in text or "<=15" in text
    assert "250" in text


def test_small_corpus_threshold_documented() -> None:
    text = Path(REPO_ROOT / "docs/protocol/reliability_policy_v0.1.md").read_text(
        encoding="utf-8"
    )
    assert "15" in text and "250" in text
