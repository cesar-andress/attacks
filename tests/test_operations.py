"""Tests for execution-operations validators."""

from school_security_audit.validate_operations import validate_operations


def test_operations_validation_passes() -> None:
    report = validate_operations()
    assert report.ok, report.errors


def test_ucw003_decision_record_resolved() -> None:
    from school_security_audit.constants import REPO_ROOT

    text = (REPO_ROOT / "docs/operations/UCW-003_decision_record.md").read_text(encoding="utf-8")
    assert "RESOLVED" in text
    assert "Direct contact" in text or "direct contact" in text.lower()
    assert "voluntary" in text.lower() or "non-remunerated" in text.lower()
    assert "TO_BE_SET_AS_HUMAN" not in text
