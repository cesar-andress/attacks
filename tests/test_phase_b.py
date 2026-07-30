"""Tests for Phase-B package and OPT-B adoption."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.phase_b_qualification import score_responses
from school_security_audit.validate_phase_b import FNSS_CHECKSUM, validate_phase_b


def test_phase_b_validation_ok() -> None:
    report = validate_phase_b()
    assert report.ok, report.errors


def test_opt_b_adopted_and_draft_superseded() -> None:
    opts = {r["option_id"]: r for r in read_csv(REPO_ROOT / "data/phase_b/amendment_options.csv")}
    assert opts["OPT-B"]["status"] == "adopted"
    draft = (REPO_ROOT / "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md").read_text(
        encoding="utf-8"
    )
    assert "SUPERSEDED" in draft
    adopted = (
        REPO_ROOT / "docs/protocol/amendments/PA-2026-07-31-002_operational_fnss_comparator.md"
    ).read_text(encoding="utf-8")
    assert "PA-2026-07-31-002" in adopted
    assert FNSS_CHECKSUM in adopted
    assert "adopted" in adopted.lower()


def test_cf02_conceptual_fnss_operational() -> None:
    by_c = {
        r["candidate_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/authorized_source_status.csv")
    }
    assert by_c["CF-02"]["usable_for_phase_b_coding"] == "false"
    assert by_c["ALT-FNSS-001"]["usable_for_phase_b_coding"] == "true"
    assert by_c["ALT-FNSS-001"]["checksum_sha256"] == FNSS_CHECKSUM


def test_gates_design_go_calibration_nogo() -> None:
    rows = {
        r["gate_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/benchmark_design_gate.csv")
    }
    assert rows["benchmark_design_gate"]["outcome"] == "GO"
    assert rows["benchmark_design_gate"]["benchmark_calibration_status"] == "NO_GO"
    assert rows["benchmark_source_gate"]["outcome"] == "READY"
    assert rows["independent_coder_gate"]["outcome"] == "NOT_READY"
    assert rows["cf02_access_subgate"]["outcome"] == "CF02_ACCESS_NO_GO"


def test_no_phase_b_target_codes() -> None:
    assert read_csv(REPO_ROOT / "data/phase_b/phase_b_target_codes.csv") == []


def test_manifest_blocks_premature_execution() -> None:
    man = {
        r["field"]: r["value"]
        for r in read_csv(REPO_ROOT / "data/phase_b/phase_b_execution_manifest.csv")
    }
    assert man["amendment_id"] == "PA-2026-07-31-002"
    assert man["coder_independence_verified"] == "false"
    assert man["qualification_complete"] == "false"
    assert man["final_gate"] == "BENCHMARK_CALIBRATION=NO_GO"
    assert man["gold_standard_forbidden"] == "true"


def test_qualification_fixtures() -> None:
    root = REPO_ROOT
    assert score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_pass.csv"), root
    )["passed"]
    assert not score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_fail.csv"), root
    )["passed"]


def test_qualification_not_targets() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/qualification_cases.csv"):
        assert r["PHASE_B_TARGET"] == "false"


def test_doc_alt_fnss_registered() -> None:
    rows = {
        r["document_id"]: r
        for r in read_csv(REPO_ROOT / "data/corpus/document_registry.csv")
    }
    assert "DOC-ALT-FNSS-001" in rows
    assert rows["DOC-ALT-FNSS-001"]["checksum_sha256"] == FNSS_CHECKSUM


def test_rpp2_and_slapa_unchanged() -> None:
    papers = {
        r["paper_id"]: r["status"]
        for r in read_csv(REPO_ROOT / "docs/research_program/paper_dependency_register.csv")
    }
    assert papers["RP-P2"] == "planned"
    for r in read_csv(REPO_ROOT / "docs/research_program/slapa_domains.csv"):
        assert r["validation_status"] == "planned_unvalidated"


def test_freeze_and_full_coding_still_nogo() -> None:
    by_id = {
        r["gate_id"]: r["status"]
        for r in read_csv(REPO_ROOT / "data/gates/gate_register.csv")
    }
    assert by_id["benchmark_calibration_gate"] == "NO_GO"
    assert by_id["corpus_freeze_gate"] == "NO_GO"
    assert by_id["full_coding_gate"] == "NO_GO"


def test_no_gold_standard_affirmation_in_decision() -> None:
    text = Path(REPO_ROOT / "docs/phase_b/opt_b_decision_record.md").read_text(
        encoding="utf-8"
    ).lower()
    assert "is a gold standard" not in text
    assert "as a gold standard" not in text
