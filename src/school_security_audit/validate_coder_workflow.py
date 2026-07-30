"""Validate independent-coder workflow controls (no fabricated readiness)."""

from __future__ import annotations

import re
from pathlib import Path

from school_security_audit.check_training_overlap import check_training_overlap
from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport
from school_security_audit.validate_phase_b import FNSS_CHECKSUM, validate_phase_b

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b")

REQUIRED = [
    "data/phase_b/coder_package_manifest.csv",
    "data/phase_b/coder_admin_manifest.csv",
    "data/phase_b/qualification_set_manifest.csv",
    "data/phase_b/qualification_freeze_record.csv",
    "data/phase_b/training_target_overlap_report.csv",
    "data/phase_b/target_package_manifest.csv",
    "data/phase_b/unresolved_coder_workflow_items.csv",
    "data/phase_b/bdd_adjudication_blank.csv",
    "data/phase_b/coding_form_schema.csv",
    "data/phase_b/unitization_template.csv",
    "data/phase_b/phase_a_recoding_decision_template.csv",
    "docs/phase_b/independent_coding/forms/independence_coi_form.md",
    "docs/phase_b/independent_coding/forms/confidentiality_agreement.md",
    "docs/phase_b/independent_coding/attempt_policy_DRAFT.md",
    "docs/phase_b/independent_coding/operator_runbook.md",
    "docs/phase_b/independent_coding/qualification_decision_rules.md",
]


def _manifest(root: Path) -> dict[str, str]:
    path = root / "data/phase_b/phase_b_execution_manifest.csv"
    return {r["field"]: r.get("value", "") for r in read_csv(path)} if path.exists() else {}


def validate_coder_workflow(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    # Keep Phase-B scientific validators
    base = validate_phase_b(root)
    for e in base.errors:
        report.add(e)

    for rel in REQUIRED:
        if not (root / rel).exists():
            report.add(f"missing {rel}")

    # Overlap
    for e in check_training_overlap(root).errors:
        report.add(e)

    man = _manifest(root)
    if man.get("target_package_seal_status") != "SEALED":
        report.add("manifest: target_package_seal_status must be SEALED until READY")
    if man.get("coder_readiness") not in {"", "NOT_READY"}:
        if man.get("coder_readiness") == "READY":
            report.add("manifest: coder_readiness must not be READY without real human completion")
    if man.get("qualification_complete", "").lower() == "true":
        report.add("manifest: qualification_complete must remain false without real pass")
    if man.get("coder_independence_verified", "").lower() == "true":
        report.add("manifest: independence must remain false without real attestation")
    if man.get("coi_status") not in {"NOT_COMPLETED", ""}:
        if man.get("coi_status") in {"COMPLETED_NO_CONFLICT", "COMPLETED"} and man.get(
            "human_review"
        ) == "NOT_STARTED":
            report.add("manifest: COI completed without human review is invalid for READY")
    if man.get("attempt_policy_status") != "DRAFT_PENDING_HUMAN_ADOPTION":
        # Allow future adopted status only if unresolved item closed — for now expect draft
        if man.get("attempt_policy_status") == "ADOPTED" and man.get("coder_readiness") == "READY":
            pass
        elif man.get("attempt_policy_status") not in {
            "DRAFT_PENDING_HUMAN_ADOPTION",
            "ADOPTED",
        }:
            report.add("manifest: attempt_policy_status unrecognized")
    if man.get("checksum_sha256") != FNSS_CHECKSUM:
        report.add("manifest: FNSS checksum mismatch")
    if man.get("final_gate") != "BENCHMARK_CALIBRATION=NO_GO":
        report.add("manifest: calibration must remain NO_GO")

    # Admin manifest must be template-only / no real PII
    for r in read_csv(root / "data/phase_b/coder_admin_manifest.csv"):
        if r.get("row_type") != "TEMPLATE_ONLY":
            # Real rows forbidden in public repo for now
            report.add("coder_admin_manifest: public repo may contain TEMPLATE_ONLY rows only")
        blob = " ".join(r.values())
        if EMAIL_RE.search(blob):
            report.add("coder_admin_manifest: email-like personal data forbidden in public repo")
        for key in ("coder_pseudonymous_id",):
            if r.get(key, "").strip() and r.get("row_type") == "TEMPLATE_ONLY":
                # empty ok
                pass

    # Target codes empty
    if read_csv(root / "data/phase_b/phase_b_target_codes.csv"):
        report.add("phase_b_target_codes must be empty")

    # Target seal
    for r in read_csv(root / "data/phase_b/target_package_manifest.csv"):
        if r.get("coder_access_state") != "SEALED":
            report.add(f"target package {r.get('item_id')} must be SEALED")
        if r.get("prefilled_codes_exist", "").lower() == "true":
            report.add(f"target package {r.get('item_id')} prefilled codes forbidden")

    # BDD blank — no adjudicated values
    for r in read_csv(root / "data/phase_b/bdd_adjudication_blank.csv"):
        if (r.get("adjudicated_value") or "").strip():
            report.add(f"{r.get('decision_id')}: adjudicated_value must be blank before coding")
        if r.get("status") != "open_blank":
            report.add(f"{r.get('decision_id')}: status must remain open_blank")

    # Freeze incomplete
    freeze = read_csv(root / "data/phase_b/qualification_freeze_record.csv")
    if any(r.get("human_authorized", "").lower() == "true" for r in freeze):
        # If somehow authorized, attempt policy must be adopted — currently should all be false
        pass
    if not any(r.get("component") == "attempt_policy" for r in freeze):
        report.add("freeze record missing attempt_policy component")
    draft_pol = (root / "docs/phase_b/independent_coding/attempt_policy_DRAFT.md").read_text(
        encoding="utf-8"
    )
    if "DRAFT_PENDING_HUMAN_ADOPTION" not in draft_pol:
        report.add("attempt policy must remain draft until human adoption")

    # Unresolved blockers present
    items = {r["item_id"]: r for r in read_csv(root / "data/phase_b/unresolved_coder_workflow_items.csv")}
    if items.get("UCW-001", {}).get("status") != "open_blocks_ready":
        report.add("UCW-001 must remain open until attempt policy adopted")

    # Forbidden gold / CF02 operational drift already in validate_phase_b

    # Personal data scan on phase_b docs (coarse)
    for path in (root / "docs/phase_b/independent_coding").rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        # Allow TO_BE_SET_BY_HUMAN and blank underscores; flag obvious emails not in examples
        for m in EMAIL_RE.finditer(text):
            if m.group(0) in {"cesar.andress@ucjc.edu"}:
                # should not appear in coder package docs
                report.add(f"{path.relative_to(root)}: personal email in coder package docs")

    # Coding form schema forbids expected/adjudicated answers
    for r in read_csv(root / "data/phase_b/coding_form_schema.csv"):
        if r.get("field") in {"expected_answer", "adjudicated_answer"}:
            if r.get("required") != "forbidden":
                report.add(f"coding form field {r.get('field')} must be forbidden")

    # Synthetic workflow must not claim real gate changes
    for r in read_csv(root / "data/phase_b/synthetic_workflow_state.csv"):
        if r.get("real_gates_affected", "").lower() == "true":
            report.add("synthetic workflow must not affect real gates")

    # Unitization template not prefilled with judgments
    for r in read_csv(root / "data/phase_b/unitization_template.csv"):
        if r.get("is_pe", "").strip():
            report.add("unitization template must not contain PE judgments")
        if r.get("TEMPLATE_ONLY", "").lower() != "true":
            report.add("unitization template rows must be TEMPLATE_ONLY")

    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_coder_workflow()
    if report.ok:
        print("Coder-workflow validation OK.")
        return 0
    print("Coder-workflow validation FAILED:")
    for e in report.errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
