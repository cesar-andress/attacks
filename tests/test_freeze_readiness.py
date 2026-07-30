"""Tests for freeze-readiness artefacts and RQ2/Branch B constants."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import (
    BRANCH_B_FAMILY_F_FIELDS,
    BRANCH_B_STATUS,
    FREEZE_DISPOSITION_VALUES,
    RQ2_PRIMARY_MIN_RUNG,
    REPO_ROOT,
)
from school_security_audit.validate_metadata import validate_corpus


def test_branch_b_inactive_constant() -> None:
    assert BRANCH_B_STATUS == "inactive_for_current_study"
    assert "false_positive_safeguard" in BRANCH_B_FAMILY_F_FIELDS


def test_rq2_primary_min_rung() -> None:
    assert RQ2_PRIMARY_MIN_RUNG == 1


def test_disposition_values() -> None:
    assert {"include", "exclude", "hold", "comparator", "background_only"} <= FREEZE_DISPOSITION_VALUES


def test_freeze_artefacts_exist() -> None:
    root = REPO_ROOT
    assert (root / "data/corpus/freeze_readiness_register.csv").exists()
    assert (root / "data/corpus/candidate_disposition_recommendations.csv").exists()
    assert (root / "data/pilot/PILOT_STATUS.txt").exists()
    assert (root / "docs/protocol/go_nogo_report.md").exists()


def test_validate_corpus_with_disposition() -> None:
    report = validate_corpus()
    assert report.ok, report.errors


def test_pilot_status_keeps_later_gates_blocked() -> None:
    text = Path(REPO_ROOT / "data/pilot/PILOT_STATUS.txt").read_text(encoding="utf-8")
    assert "NOT_FOR_SUBSTANTIVE_INFERENCE" in text
    assert "COMPLETE_PILOT=INCOMPLETE" in text
    assert "CORPUS_FREEZE=NO_GO" in text
    assert "FULL_CODING=NO_GO" in text
    # Phase A may be completed under PA-2026-07-31-001 without opening later gates
    assert "OPERATIONAL_PILOT=" in text
