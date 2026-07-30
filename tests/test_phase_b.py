"""Tests for Phase-B benchmark preparation package."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.phase_b_qualification import score_responses
from school_security_audit.validate_phase_b import validate_phase_b


def test_phase_b_validation_ok() -> None:
    report = validate_phase_b()
    assert report.ok, report.errors


def test_no_phase_b_target_codes_yet() -> None:
    rows = read_csv(REPO_ROOT / "data/phase_b/phase_b_target_codes.csv")
    assert rows == []


def test_amendment_options_complete() -> None:
    ids = {r["option_id"] for r in read_csv(REPO_ROOT / "data/phase_b/amendment_options.csv")}
    assert ids == {"OPT-A", "OPT-B", "OPT-C", "OPT-D"}
    for r in read_csv(REPO_ROOT / "data/phase_b/amendment_options.csv"):
        assert r["status"] == "proposed_not_enacted"


def test_benchmark_design_gate_recommendation() -> None:
    rows = {
        r["gate_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/benchmark_design_gate.csv")
    }
    assert (
        rows["benchmark_design_gate"]["outcome"]
        == "OPERATIONAL_L1_AMENDMENT_RECOMMENDED"
    )
    assert rows["benchmark_design_gate"]["benchmark_calibration_status"] == "NO_GO"
    assert rows["cf02_access_subgate"]["outcome"] == "CF02_ACCESS_NO_GO"


def test_fnss_checksum_recorded_cf02_not_usable() -> None:
    by_id = {
        r["candidate_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/authorized_source_status.csv")
    }
    assert by_id["CF-02"]["usable_for_phase_b_coding"] == "false"
    assert by_id["ALT-FNSS-001"]["checksum_sha256"].startswith("ab21f61b")
    assert by_id["ALT-FNSS-001"]["usable_for_phase_b_coding"] == "conditional_on_amendment"


def test_qualification_pass_and_fail_fixtures() -> None:
    root = REPO_ROOT
    passed = score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_pass.csv"), root
    )
    failed = score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_fail.csv"), root
    )
    assert passed["passed"] is True
    assert failed["passed"] is False
    assert failed["critical_fails"]


def test_qualification_not_phase_b_targets() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/qualification_cases.csv"):
        assert r["PHASE_B_TARGET"] == "false"
        assert r["source_status"] == "synthetic_constructed"


def test_access_route_ids_present() -> None:
    ids = {r["route_id"] for r in read_csv(REPO_ROOT / "data/phase_b/access_routes.csv")}
    assert "AR-CF02-001" in ids
    assert "AR-FNSS-001" in ids
    assert "AR-CF02-009" in ids  # forbidden route documented


def test_draft_amendment_not_adopted() -> None:
    text = Path(
        REPO_ROOT / "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md"
    ).read_text(encoding="utf-8")
    assert "DRAFT_NOT_ADOPTED" in text


def test_pilot_gates_unchanged() -> None:
    text = Path(REPO_ROOT / "data/pilot/PILOT_STATUS.txt").read_text(encoding="utf-8")
    assert "BENCHMARK_CALIBRATION=NO_GO" in text
    assert "simulated_procedural_second_pass" in text
    assert "EMPIRICAL_INTERCODER_RELIABILITY=not_computed" in text
