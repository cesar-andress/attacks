"""Tests for pilot source-acquisition manifests and gates."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import (
    AUTHORIZATION_STATUSES,
    PILOT_SOURCE_DISPOSITIONS,
    PILOT_USABLE_AUTHORIZATION_STATUSES,
    REPO_ROOT,
)
from school_security_audit.validate_metadata import validate_corpus


def test_authorization_status_set() -> None:
    assert "public_official_download" in AUTHORIZATION_STATUSES
    assert "access_restricted" in AUTHORIZATION_STATUSES


def test_pilot_usable_subset() -> None:
    assert PILOT_USABLE_AUTHORIZATION_STATUSES <= AUTHORIZATION_STATUSES


def test_disposition_set() -> None:
    assert "ready_for_pilot" in PILOT_SOURCE_DISPOSITIONS
    assert "hold_authorization" in PILOT_SOURCE_DISPOSITIONS


def test_acquisition_artefacts_exist() -> None:
    root = Path(REPO_ROOT)
    assert (root / "data/source_registry/pilot_source_acquisitions.csv").exists()
    assert (root / "data/source_checksums/pilot_source_checksums.csv").exists()
    assert (root / "data/pilot/PILOT_SOURCE_GATE.txt").exists()


def test_gate_records_operational_ready_without_phase_b_complete() -> None:
    text = Path(REPO_ROOT / "data/pilot/PILOT_SOURCE_GATE.txt").read_text(encoding="utf-8")
    assert "OPERATIONAL_COMPARATOR_READY" in text
    assert "BENCHMARK_CALIBRATION=NO_GO" in text
    assert "NOT_FOR_SUBSTANTIVE_INFERENCE" in text
    assert "DO_NOT_EQUATE_SOURCE_READY_WITH_PHASE_B_COMPLETE=true" in text


def test_local_sources_not_tracked_rows() -> None:
    from school_security_audit.io_utils import read_csv

    rows = read_csv(REPO_ROOT / "data/source_registry/pilot_source_acquisitions.csv")
    for row in rows:
        if row.get("local_path", "").startswith("local_sources/"):
            assert row.get("tracked_in_git", "").lower() == "false"


def test_validate_corpus_includes_acquisitions() -> None:
    report = validate_corpus()
    assert report.ok, report.errors
