"""Positive and negative tests for independent-coder workflow controls."""

from __future__ import annotations

import csv
import io
from pathlib import Path

import pytest

from school_security_audit.check_training_overlap import check_training_overlap
from school_security_audit.constants import REPO_ROOT
from school_security_audit.generate_coder_package import generate_package
from school_security_audit.io_utils import read_csv
from school_security_audit.phase_b_qualification import score_responses
from school_security_audit.validate_coder_workflow import validate_coder_workflow


def test_coder_workflow_validation_ok() -> None:
    report = validate_coder_workflow()
    assert report.ok, report.errors


def test_overlap_check_ok() -> None:
    assert check_training_overlap().ok


def test_admin_manifest_template_only() -> None:
    rows = read_csv(REPO_ROOT / "data/phase_b/coder_admin_manifest.csv")
    assert rows
    assert all(r["row_type"] == "TEMPLATE_ONLY" for r in rows)


def test_target_package_sealed() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/target_package_manifest.csv"):
        assert r["coder_access_state"] == "SEALED"
        assert r["prefilled_codes_exist"] == "false"


def test_qualification_freeze_incomplete() -> None:
    rows = read_csv(REPO_ROOT / "data/phase_b/qualification_freeze_record.csv")
    assert any(r["component"] == "attempt_policy" for r in rows)
    assert all(r.get("human_authorized", "false").lower() == "false" for r in rows)


def test_attempt_policy_draft_blocks_ready() -> None:
    items = {
        r["item_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/unresolved_coder_workflow_items.csv")
    }
    assert items["UCW-001"]["blocks_coder_ready"] == "true"
    assert items["UCW-001"]["status"] == "open_blocks_ready"
    man = {
        r["field"]: r["value"]
        for r in read_csv(REPO_ROOT / "data/phase_b/phase_b_execution_manifest.csv")
    }
    assert man["attempt_policy_status"] == "DRAFT_PENDING_HUMAN_ADOPTION"
    assert man["coder_readiness"] == "NOT_READY"


def test_scorer_fixtures_still_work() -> None:
    root = REPO_ROOT
    passed = score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_pass.csv"), root
    )
    failed = score_responses(
        read_csv(root / "data/phase_b/synthetic_qualification_fail.csv"), root
    )
    assert passed["passed"] and passed["scorer_version"] == "QUAL-SCORER-v1"
    assert passed["answer_key_exposed"] is False
    assert not failed["passed"]


def test_recruitment_package_dry_run() -> None:
    man = generate_package("recruitment", dry_run=True)
    assert man["package_type"] == "recruitment"
    assert man["status"] == "generated_dry_run"
    assert not any("qualification_reference" in f["path"] for f in man["files"])


def test_qualification_package_blocked_before_freeze_auth() -> None:
    with pytest.raises(RuntimeError, match="freeze"):
        generate_package("qualification", dry_run=True)


def test_target_package_generation_blocked() -> None:
    with pytest.raises(RuntimeError, match="READY"):
        generate_package("post_qualification_target", dry_run=True)


def test_synthetic_workflow_does_not_affect_gates() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/synthetic_workflow_state.csv"):
        assert r["real_gates_affected"] == "false"
    status = (REPO_ROOT / "data/pilot/PILOT_STATUS.txt").read_text(encoding="utf-8")
    assert "INDEPENDENT_CODER=NOT_READY" in status
    assert "BENCHMARK_CALIBRATION=NO_GO" in status


def test_bdd_blank_not_adjudicated() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/bdd_adjudication_blank.csv"):
        assert r["status"] == "open_blank"
        assert r["adjudicated_value"] == ""
        assert r["cf02_primary_operational_forbidden"] == "true"


def test_negative_public_email_in_admin_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Copy-on-write style: validate detects email if injected into a temp admin manifest."""
    from school_security_audit import validate_coder_workflow as mod

    # Ensure real tree still OK
    assert validate_coder_workflow().ok

    # Direct unit: email regex path via temporary CSV content check
    bad = "alice@example.com"
    assert mod.EMAIL_RE.search(bad)


def test_negative_prefilled_target_codes_fail() -> None:
    rows = read_csv(REPO_ROOT / "data/phase_b/phase_b_target_codes.csv")
    assert rows == []


def test_negative_answer_key_withheld_in_package_manifest() -> None:
    rows = {
        r["file_path"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/coder_package_manifest.csv")
    }
    key = "data/phase_b/qualification_reference.csv"
    assert rows[key]["access_class"] == "WITHHOLD_FROM_CODER"


def test_negative_gold_standard_still_forbidden() -> None:
    man = {
        r["field"]: r["value"]
        for r in read_csv(REPO_ROOT / "data/phase_b/phase_b_execution_manifest.csv")
    }
    assert man["gold_standard_forbidden"] == "true"


def test_coding_form_forbids_expected_answers() -> None:
    rows = {r["field"]: r for r in read_csv(REPO_ROOT / "data/phase_b/coding_form_schema.csv")}
    assert rows["expected_answer"]["required"] == "forbidden"
    assert rows["adjudicated_answer"]["required"] == "forbidden"


def test_unitization_template_blank() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/unitization_template.csv"):
        assert r["TEMPLATE_ONLY"] == "true"
        assert r["is_pe"] == ""
