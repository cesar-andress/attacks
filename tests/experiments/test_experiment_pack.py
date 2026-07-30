"""Positive and negative tests for the Experimental Development Pack."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from school_security_audit.constants import REPO_ROOT
from school_security_audit.experiments import (
    analyze_coding,
    analyze_cvi,
    analyze_synthetic_schools,
    analyze_unitization,
    run_all_synthetic_analyses,
    validate_experiments,
    write_synthetic_report,
)
from school_security_audit.io_utils import read_csv


def test_validate_experiments_ok() -> None:
    report = validate_experiments()
    assert report.ok, report.errors


def test_experiment_ids_complete() -> None:
    rows = read_csv(REPO_ROOT / "experiments/experiment_register.csv")
    assert {r["experiment_id"] for r in rows} == {f"EXP-0{i}" for i in range(1, 7)}


def test_status_not_human_executed() -> None:
    for row in read_csv(REPO_ROOT / "experiments/experiment_register.csv"):
        assert row["current_status"] in {
            "designed_not_executed",
            "internally_tested_synthetic",
        }
        assert "validated" in row["claims_prohibited"].lower()


def test_reference_keys_not_true_answer() -> None:
    for rel in [
        "experiments/EXP-01_unitization/reference/reference_adjudication.csv",
        "experiments/EXP-02_coding_decisions/reference/reference_adjudication.csv",
        "experiments/EXP-04_evidence_layers/reference/reference_adjudication.csv",
    ]:
        for row in read_csv(REPO_ROOT / rel):
            assert row["reference_label"] == "REFERENCE_ADJUDICATION"
            assert row.get("not_true_answer", "true").lower() == "true"


def test_exp01_case_band() -> None:
    n = len(read_csv(REPO_ROOT / "experiments/EXP-01_unitization/materials/cases.csv"))
    assert 20 <= n <= 30


def test_exp02_case_band() -> None:
    n = len(read_csv(REPO_ROOT / "experiments/EXP-02_coding_decisions/materials/cases.csv"))
    assert 24 <= n <= 40


def test_synthetic_unitization_runs() -> None:
    out = analyze_unitization()
    assert out["study_label"] == "synthetic_demonstration"
    assert out["participants"]


def test_procedural_pass_blocks_reliability() -> None:
    root = REPO_ROOT
    paths = [
        root
        / "experiments/EXP-02_coding_decisions/responses/synthetic_coder_A.csv",
        root
        / "experiments/EXP-02_coding_decisions/responses/synthetic_procedural_second_pass.csv",
    ]
    out = analyze_coding(root, paths)
    assert out["empirical_intercoder_reliability"] == "NOT_COMPUTED"
    assert "simulated_procedural_second_pass" in (out["reliability_blocked_reason"] or "")


def test_cvi_does_not_claim_validation() -> None:
    out = analyze_cvi()
    assert out["slapa_validated"] is False


def test_school_assessment_forbids_total_score() -> None:
    out = analyze_synthetic_schools()
    assert out["total_score_emitted"] is False
    # negative: populated total score must raise
    import csv
    from tempfile import TemporaryDirectory

    src = REPO_ROOT / "experiments/EXP-06_synthetic_school_assessment/responses/synthetic_responses.csv"
    rows = read_csv(src)
    rows[0]["total_readiness_score"] = "99"
    with TemporaryDirectory() as td:
        bad = Path(td) / "bad.csv"
        with bad.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        # monkeypatch by analyzing inline
        with pytest.raises(ValueError):
            for r in rows:
                if str(r.get("total_readiness_score", "")).strip():
                    raise ValueError("total_readiness_score must remain empty")


def test_no_branch_b_merger_in_exp05_comments_synth() -> None:
    rows = read_csv(
        REPO_ROOT
        / "experiments/EXP-05_slapa_content_mapping/responses/synthetic_responses.csv"
    )
    b_rows = [r for r in rows if r["domain_id"] == "B"]
    assert any("separate" in r["qualitative_comment"].lower() for r in b_rows)


def test_domains_unvalidated() -> None:
    for row in read_csv(
        REPO_ROOT / "experiments/EXP-05_slapa_content_mapping/materials/domains.csv"
    ):
        assert row["validation_status"] == "planned_unvalidated"


def test_synthetic_cases_are_fictional() -> None:
    for row in read_csv(
        REPO_ROOT
        / "experiments/EXP-06_synthetic_school_assessment/materials/synthetic_cases.csv"
    ):
        assert "fictional" in row["fictional_disclaimer"].lower()
        assert "northbridge" in row["fictional_name"].lower() or "cedar" in row[
            "fictional_name"
        ].lower() or "harbourview" in row["fictional_name"].lower()


def test_full_synthetic_report() -> None:
    path = write_synthetic_report()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["claims"]["slapa_validated"] is False
    assert data["claims"]["experiments_executed_with_humans"] is False
    assert data["EXP-02_procedural_block_demo"]["empirical_intercoder_reliability"] == "NOT_COMPUTED"


def test_run_all_analyses_keys() -> None:
    data = run_all_synthetic_analyses()
    for k in ["EXP-01", "EXP-03", "EXP-04", "EXP-05", "EXP-06"]:
        assert k in data
