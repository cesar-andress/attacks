"""Tests for execution-operations validators."""

from school_security_audit.validate_operations import validate_operations


def test_operations_validation_passes() -> None:
    report = validate_operations()
    assert report.ok, report.errors


def test_ucw003_decision_record_unresolved() -> None:
    from pathlib import Path
    from school_security_audit.constants import REPO_ROOT

    text = (REPO_ROOT / "docs/operations/UCW-003_decision_record.md").read_text(encoding="utf-8")
    assert "UNRESOLVED" in text
    assert "Decision pending" in text or "Not yet selected" in text
    assert "TO_BE_SET_AS_HUMAN" not in text
