"""Metadata validation tests — constructed fixtures only."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.validate_metadata import validate_corpus

FIXTURES = Path(__file__).parent / "fixtures"
VALID = FIXTURES / "valid_minimal"
REPO = Path(__file__).resolve().parents[1]


def test_empty_templates_pass() -> None:
    report = validate_corpus(REPO)
    assert report.ok, report.errors


def test_valid_minimal_dataset_passes() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert report.ok, report.errors


def test_orphan_document_framework_id() -> None:
    orphan_dir = FIXTURES / "orphan_document"
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=orphan_dir / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("orphan framework_id" in e for e in report.errors)


def test_invalid_framework_document_pe_relationship() -> None:
    bad = FIXTURES / "invalid_relationship"
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=bad / "prescriptive_elements.csv",
    )
    assert not report.ok
    assert any("orphan document_id" in e for e in report.errors)
