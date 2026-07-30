"""Metadata validation tests — constructed fixtures only."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.validate_metadata import validate_corpus

FIXTURES = Path(__file__).parent / "fixtures"
VALID = FIXTURES / "valid_minimal"
REPO = Path(__file__).resolve().parents[1]


def test_repository_provisional_register_passes() -> None:
    report = validate_corpus(REPO)
    assert report.ok, report.errors


def test_valid_minimal_dataset_passes() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
        counterexamples_path=VALID / "counterexample_commitments.csv",
        openalex_path=VALID / "openalex_literature_verifications.csv",
    )
    assert report.ok, report.errors


def test_orphan_document_framework_id() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=FIXTURES / "orphan_document" / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
        counterexamples_path=VALID / "counterexample_commitments.csv",
        openalex_path=VALID / "openalex_literature_verifications.csv",
    )
    assert not report.ok
    assert any("orphan framework_id" in e for e in report.errors)


def test_invalid_framework_document_pe_relationship() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=FIXTURES / "invalid_relationship" / "prescriptive_elements.csv",
        counterexamples_path=VALID / "counterexample_commitments.csv",
        openalex_path=VALID / "openalex_literature_verifications.csv",
    )
    assert not report.ok
    assert any("orphan document_id" in e for e in report.errors)


EMPTY = FIXTURES / "empty_docs"


def _empty_oa_kwargs() -> dict:
    return {
        "documents_path": EMPTY / "document_registry.csv",
        "pe_path": EMPTY / "prescriptive_elements.csv",
        "counterexamples_path": EMPTY / "counterexample_commitments.csv",
        "openalex_path": EMPTY / "openalex_literature_verifications.csv",
    }


def test_rejects_eu_uk_and_final_statuses() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=FIXTURES / "bad_statuses" / "candidate_frameworks.csv",
        **_empty_oa_kwargs(),
    )
    assert not report.ok
    blob = " ".join(report.errors)
    assert "EU/UK" in blob or "forbidden geography" in blob
    assert "included" in blob or "forbidden status" in blob
    assert "frozen" in blob


def test_rejects_cf22_as_verified() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=FIXTURES / "cf22_verified_illegal" / "candidate_frameworks.csv",
        **_empty_oa_kwargs(),
    )
    assert not report.ok
    assert any("CF-22" in e for e in report.errors)


def test_unverified_requires_unresolved_action() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=FIXTURES / "unverified_missing_action" / "candidate_frameworks.csv",
        **_empty_oa_kwargs(),
    )
    assert not report.ok
    assert any("unresolved_verification_action required" in e for e in report.errors)


def test_rejects_codebook_tokens_in_counterexample_surface() -> None:
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
        counterexamples_path=FIXTURES / "bad_counterexample_tokens" / "counterexample_commitments.csv",
        openalex_path=VALID / "openalex_literature_verifications.csv",
    )
    assert not report.ok
    assert any("forbidden audit/codebook token" in e for e in report.errors)


def test_openalex_row_must_not_authorize_inclusion() -> None:
    bad = FIXTURES / "bad_openalex"
    report = validate_corpus(
        REPO,
        frameworks_path=VALID / "candidate_frameworks.csv",
        documents_path=VALID / "document_registry.csv",
        pe_path=VALID / "prescriptive_elements.csv",
        counterexamples_path=VALID / "counterexample_commitments.csv",
        openalex_path=bad / "openalex_literature_verifications.csv",
    )
    assert not report.ok
    assert any("does_not_authorize_corpus_inclusion" in e for e in report.errors)
