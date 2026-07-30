"""Coding validation tests — constructed fixtures only."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.validate_coding import (
    confirmatory_demand_presence,
    validate_coding,
)

FIXTURES = Path(__file__).parent / "fixtures"
VALID = FIXTURES / "valid_minimal"
REPO = Path(__file__).resolve().parents[1]


def test_empty_coding_template_passes() -> None:
    report = validate_coding(REPO)
    assert report.ok, report.errors


def test_valid_minimal_coding_passes() -> None:
    report = validate_coding(
        REPO,
        coding_path=VALID / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert report.ok, report.errors


def test_invalid_executability_rung() -> None:
    report = validate_coding(
        REPO,
        coding_path=FIXTURES / "invalid_rung" / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("invalid executability_rung" in e for e in report.errors)


def test_entailed_demand_without_trigger() -> None:
    report = validate_coding(
        REPO,
        coding_path=FIXTURES / "entailed_no_trigger" / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("requires non-empty trigger evidence" in e for e in report.errors)


def test_ambiguous_memo_not_counted_as_presence() -> None:
    report = validate_coding(
        REPO,
        coding_path=FIXTURES / "ambiguous_as_presence" / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("ambiguous_memo" in e for e in report.errors)

    row = {
        "demand_inhibitory_acoustic": "1",
        "demand_inhibitory_acoustic_source": "ambiguous_memo",
    }
    assert confirmatory_demand_presence(row, "demand_inhibitory_acoustic") is False


def test_forbidden_combined_score_rejected() -> None:
    report = validate_coding(
        REPO,
        coding_path=FIXTURES / "combined_score" / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("forbidden composite" in e or "inclusive_security_score" in e for e in report.errors)


def test_orphan_pe_id() -> None:
    report = validate_coding(
        REPO,
        coding_path=FIXTURES / "orphan_pe" / "coding.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("orphan pe_id" in e for e in report.errors)
