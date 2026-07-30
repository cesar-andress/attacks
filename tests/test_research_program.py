"""Tests for research-programme registers and boundaries."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import BRANCH_B_STATUS, REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_research_program import validate_research_program


def test_research_program_validation_ok() -> None:
    report = validate_research_program()
    assert report.ok, report.errors


def test_only_p1_active() -> None:
    rows = read_csv(REPO_ROOT / "docs/research_program/paper_dependency_register.csv")
    statuses = {r["paper_id"]: r["status"] for r in rows}
    assert statuses["RP-P1"] == "active"
    assert statuses["RP-P2"] == "planned"
    assert statuses["RP-P3"] == "planned"
    assert statuses["RP-P4"] == "planned"


def test_slapa_domains_unvalidated() -> None:
    for row in read_csv(REPO_ROOT / "docs/research_program/slapa_domains.csv"):
        assert row["validation_status"] == "planned_unvalidated"


def test_branch_b_still_inactive_for_paper1() -> None:
    assert BRANCH_B_STATUS == "inactive_for_current_study"
    text = Path(REPO_ROOT / "docs/research_program/branch_b_detectability.md").read_text(
        encoding="utf-8"
    )
    assert "inactive_for_current_study" in text
    assert "RP-P4" in text


def test_operational_priorities_put_p1_first() -> None:
    text = Path(REPO_ROOT / "docs/research_program/operational_priorities.md").read_text(
        encoding="utf-8"
    )
    assert "Priority 1" in text or "**P1**" in text
    assert "PILOT_SOURCE_NO_GO" in text or "CF-02" in text


def test_charter_not_claiming_completed_future_papers() -> None:
    text = Path(REPO_ROOT / "docs/research_program/programme_charter.md").read_text(
        encoding="utf-8"
    ).lower()
    assert "not a completed study" in text or "planned" in text
    # May mention the phrase only as a risk/prohibition, not as an achieved status
    assert "slapa is **not** validated" in text or "slapa is not validated" in text
    assert "planned" in text
