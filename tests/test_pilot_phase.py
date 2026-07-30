"""Tests for two-phase pilot gates and Phase A constraints."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_pilot_phase import validate_pilot_phase


def test_gate_register_blocks_later_stages() -> None:
    rows = {r["gate_id"]: r for r in read_csv(REPO_ROOT / "data/gates/gate_register.csv")}
    assert rows["complete_pilot_source_gate"]["status"] == "NO_GO"
    assert rows["benchmark_calibration_gate"]["status"] == "NO_GO"
    assert rows["corpus_freeze_gate"]["status"] == "NO_GO"
    assert rows["full_coding_gate"]["status"] == "NO_GO"
    assert rows["operational_pilot_gate"]["status"] in {"GO", "COMPLETED", "CONDITIONAL_GO"}


def test_phase_a_excludes_p5() -> None:
    for row in read_csv(REPO_ROOT / "data/pilot/prescriptive_elements.csv"):
        assert row.get("pilot_id") != "P5"
        assert row.get("candidate_id") != "CF-02"
        assert row.get("inference_flag") == "NOT_FOR_SUBSTANTIVE_INFERENCE"
        assert row.get("benchmark_flag") == "NOT_FOR_BENCHMARK_COMPARISON"
        assert row.get("protocol_flag") == "PROTOCOL_DEVELOPMENT_ONLY"


def test_phase_a_pe_count_band() -> None:
    rows = read_csv(REPO_ROOT / "data/pilot/prescriptive_elements.csv")
    assert 20 <= len(rows) <= 32


def test_no_phase_a_in_final_coding_template() -> None:
    rows = read_csv(REPO_ROOT / "data/coding/coding_template.csv")
    for row in rows:
        assert not str(row.get("pe_id", "")).startswith("PE-OPA-")


def test_source_gate_still_no_go() -> None:
    text = Path(REPO_ROOT / "data/pilot/PILOT_SOURCE_GATE.txt").read_text(encoding="utf-8")
    assert "PILOT_SOURCE_NO_GO" in text


def test_pilot_status_complete_incomplete() -> None:
    text = Path(REPO_ROOT / "data/pilot/PILOT_STATUS.txt").read_text(encoding="utf-8")
    assert "OPERATIONAL_PILOT=COMPLETED" in text
    assert "COMPLETE_PILOT=INCOMPLETE" in text
    assert "CORPUS_FREEZE=NO_GO" in text
    assert "FULL_CODING=NO_GO" in text
    assert "NOT_FOR_SUBSTANTIVE_INFERENCE" in text


def test_validate_pilot_phase_ok() -> None:
    report = validate_pilot_phase()
    assert report.ok, report.errors


def test_procedural_pass_not_labeled_independent() -> None:
    rows = read_csv(REPO_ROOT / "data/pilot/coding_coder_B_procedural.csv")
    assert rows
    for row in rows:
        assert row.get("coder_pass_type") == "simulated_procedural_second_pass"
        assert row.get("coder_id") == "procedural_second_pass"
