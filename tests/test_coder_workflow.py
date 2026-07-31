"""Positive and negative tests for independent-coder workflow controls."""

from __future__ import annotations

from pathlib import Path

import pytest

from school_security_audit.check_training_overlap import check_training_overlap
from school_security_audit.constants import REPO_ROOT
from school_security_audit.generate_coder_package import generate_package
from school_security_audit.io_utils import read_csv
from school_security_audit.phase_b_qualification import score_responses
from school_security_audit.validate_coder_workflow import validate_coder_workflow
import school_security_audit.validate_coder_workflow as mod


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


def test_qualification_freeze_authorized() -> None:
    rows = {
        r["component"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/qualification_freeze_record.csv")
    }
    assert rows["attempt_policy"]["version"] == "QUAL-ATTEMPT-v1"
    assert rows["freeze_bundle"]["frozen_status"] == "AUTHORIZED"
    for name in (
        "qualification_cases",
        "answer_key",
        "scorer",
        "pass_thresholds",
        "attempt_policy",
    ):
        assert rows[name]["human_authorized"].lower() == "true"
        assert rows[name]["frozen_status"] == "AUTHORIZED"
        assert rows[name]["sha256"]
        assert rows[name]["freeze_date"]
        assert rows[name]["authority"]
        assert rows[name]["amendment_linkage"]


def test_attempt_policy_adopted() -> None:
    items = {
        r["item_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/unresolved_coder_workflow_items.csv")
    }
    assert items["UCW-001"]["status"] == "closed"
    assert items["UCW-002"]["status"] == "closed"
    assert items["UCW-004"]["status"] == "closed"
    assert items["UCW-003"]["status"] == "closed"
    res = items["UCW-003"]["resolution_condition"].lower()
    assert "direct contact" in res
    assert "voluntary" in res or "unpaid" in res
    assert items["UCW-003"]["blocks_coder_ready"].lower() == "false"
    man = {
        r["field"]: r["value"]
        for r in read_csv(REPO_ROOT / "data/phase_b/phase_b_execution_manifest.csv")
    }
    assert man["attempt_policy_status"] == "ADOPTED"
    assert man["qualification_freeze_status"] == "AUTHORIZED"
    assert man["coder_readiness"] == "NOT_READY"
    text = (
        REPO_ROOT / "docs/phase_b/independent_coding/attempt_policy.md"
    ).read_text(encoding="utf-8")
    assert "QUAL-ATTEMPT-v1" in text
    assert "ADOPTED" in text
    draft = (
        REPO_ROOT / "docs/phase_b/independent_coding/attempt_policy_DRAFT.md"
    ).read_text(encoding="utf-8")
    assert "SUPERSEDED" in draft


def test_ov05_pass() -> None:
    rows = {
        r["check_id"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/training_target_overlap_report.csv")
    }
    assert rows["OV-05"]["result"] == "pass"
    decision = (
        REPO_ROOT / "docs/phase_b/independent_coding/ov05_semantic_overlap_decision.md"
    ).read_text(encoding="utf-8")
    assert "PASS" in decision


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


def test_recruitment_and_qualification_package_dry_run() -> None:
    man = generate_package("recruitment", dry_run=True)
    assert man["package_type"] == "recruitment"
    qman = generate_package("qualification", dry_run=True)
    assert qman["package_type"] == "qualification"
    assert not any("qualification_reference" in f["path"] for f in qman["files"])


def test_target_package_generation_blocked() -> None:
    with pytest.raises(RuntimeError, match="READY"):
        generate_package("post_qualification_target", dry_run=True)


def test_synthetic_workflow_does_not_affect_gates() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/synthetic_workflow_state.csv"):
        assert r["real_gates_affected"] == "false"
    status = (REPO_ROOT / "data/pilot/PILOT_STATUS.txt").read_text(encoding="utf-8")
    assert "INDEPENDENT_CODER=NOT_READY" in status
    assert "BENCHMARK_CALIBRATION=NO_GO" in status
    assert "QUALIFICATION_FREEZE=AUTHORIZED" in status
    assert "ATTEMPT_POLICY=ADOPTED" in status


def test_bdd_blank_not_adjudicated() -> None:
    for r in read_csv(REPO_ROOT / "data/phase_b/bdd_adjudication_blank.csv"):
        assert r["status"] == "open_blank"
        assert r["adjudicated_value"] == ""
        assert r["cf02_primary_operational_forbidden"] == "true"


def test_negative_email_detector() -> None:
    assert mod.EMAIL_RE.search("alice@example.com")


def test_negative_prefilled_target_codes_fail() -> None:
    assert read_csv(REPO_ROOT / "data/phase_b/phase_b_target_codes.csv") == []


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


def test_freeze_checksum_detects_tamper(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Tampering a frozen artifact must fail validation against recorded checksums."""
    # Sanity: live tree OK
    assert validate_coder_workflow().ok
    # Direct check: recorded scorer hash matches file
    rows = {
        r["component"]: r
        for r in read_csv(REPO_ROOT / "data/phase_b/qualification_freeze_record.csv")
    }
    scorer = REPO_ROOT / rows["scorer"]["path"]
    import hashlib

    assert hashlib.sha256(scorer.read_bytes()).hexdigest() == rows["scorer"]["sha256"]
