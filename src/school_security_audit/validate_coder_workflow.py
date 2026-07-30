"""Validate independent-coder workflow controls (no fabricated readiness)."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from school_security_audit.check_training_overlap import check_training_overlap
from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport
from school_security_audit.validate_phase_b import FNSS_CHECKSUM, validate_phase_b

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

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
    "docs/phase_b/independent_coding/attempt_policy.md",
    "docs/phase_b/independent_coding/ov05_semantic_overlap_decision.md",
    "docs/phase_b/independent_coding/operator_runbook.md",
    "docs/phase_b/independent_coding/qualification_decision_rules.md",
]

FROZEN_COMPONENTS = {
    "qualification_cases",
    "answer_key",
    "scorer",
    "pass_thresholds",
    "dimension_thresholds",
    "attempt_policy",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(root: Path) -> dict[str, str]:
    path = root / "data/phase_b/phase_b_execution_manifest.csv"
    return {r["field"]: r.get("value", "") for r in read_csv(path)} if path.exists() else {}


def validate_coder_workflow(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    base = validate_phase_b(root)
    for e in base.errors:
        report.add(e)

    for rel in REQUIRED:
        if not (root / rel).exists():
            report.add(f"missing {rel}")

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
    if man.get("attempt_policy_status") != "ADOPTED":
        report.add("manifest: attempt_policy_status must be ADOPTED after governance freeze")
    if man.get("qualification_freeze_status") != "AUTHORIZED":
        report.add("manifest: qualification_freeze_status must be AUTHORIZED")
    if man.get("attempt_policy_version") != "QUAL-ATTEMPT-v1":
        report.add("manifest: attempt_policy_version must be QUAL-ATTEMPT-v1")
    if man.get("checksum_sha256") != FNSS_CHECKSUM:
        report.add("manifest: FNSS checksum mismatch")
    if man.get("final_gate") != "BENCHMARK_CALIBRATION=NO_GO":
        report.add("manifest: calibration must remain NO_GO")

    # Adopted policy content
    pol = root / "docs/phase_b/independent_coding/attempt_policy.md"
    if pol.exists():
        text = pol.read_text(encoding="utf-8")
        if "**ADOPTED**" not in text and "Status:** **ADOPTED**" not in text:
            if "ADOPTED" not in text:
                report.add(f"{pol.relative_to(root)}: must record ADOPTED status")
        if "QUAL-ATTEMPT-v1" not in text:
            report.add(f"{pol.relative_to(root)}: must use QUAL-ATTEMPT-v1")
        if "QUALIFICATION_FAIL_FINAL" not in text:
            report.add(f"{pol.relative_to(root)}: must define QUALIFICATION_FAIL_FINAL")
    draft = root / "docs/phase_b/independent_coding/attempt_policy_DRAFT.md"
    if draft.exists() and "SUPERSEDED" not in draft.read_text(encoding="utf-8"):
        report.add(f"{draft.relative_to(root)}: draft must be marked SUPERSEDED")

    # Freeze authorization + checksum immutability
    freeze_path = root / "data/phase_b/qualification_freeze_record.csv"
    if freeze_path.exists():
        freeze = read_csv(freeze_path)
        by_c = {r["component"]: r for r in freeze}
        for name in FROZEN_COMPONENTS:
            row = by_c.get(name)
            if not row:
                report.add(f"freeze record missing component {name}")
                continue
            if row.get("frozen_status") != "AUTHORIZED":
                report.add(f"freeze {name}: frozen_status must be AUTHORIZED")
            if row.get("human_authorized", "").lower() != "true":
                report.add(f"freeze {name}: human_authorized must be true")
            for req in ("freeze_date", "authority", "amendment_linkage", "version", "sha256"):
                if not (row.get(req) or "").strip():
                    report.add(f"freeze {name}: missing {req}")
            rel = row.get("path", "")
            if rel and (root / rel).exists():
                actual = _sha256(root / rel)
                if actual != row.get("sha256"):
                    report.add(
                        f"freeze {name}: checksum mismatch (artifact changed after freeze)"
                    )
        bundle = by_c.get("freeze_bundle")
        if not bundle or bundle.get("frozen_status") != "AUTHORIZED":
            report.add("freeze_bundle must be AUTHORIZED")

    # UCW statuses
    items = {
        r["item_id"]: r
        for r in read_csv(root / "data/phase_b/unresolved_coder_workflow_items.csv")
    }
    for cid in ("UCW-001", "UCW-002", "UCW-004"):
        if items.get(cid, {}).get("status") != "closed":
            report.add(f"{cid} must be closed after governance freeze")
    if items.get("UCW-003", {}).get("status") != "open_human":
        report.add("UCW-003 must remain open_human (TO_BE_SET_BY_HUMAN)")
    if items.get("UCW-003", {}).get("resolution_condition") != "TO_BE_SET_BY_HUMAN":
        report.add("UCW-003 must remain TO_BE_SET_BY_HUMAN")

    # OV-05 pass
    ov = {
        r["check_id"]: r
        for r in read_csv(root / "data/phase_b/training_target_overlap_report.csv")
    }
    if ov.get("OV-05", {}).get("result") != "pass":
        report.add("OV-05 must be pass after UCW-004 closure")

    for r in read_csv(root / "data/phase_b/coder_admin_manifest.csv"):
        if r.get("row_type") != "TEMPLATE_ONLY":
            report.add("coder_admin_manifest: public repo may contain TEMPLATE_ONLY rows only")
        blob = " ".join(r.values())
        if EMAIL_RE.search(blob):
            report.add("coder_admin_manifest: email-like personal data forbidden in public repo")

    if read_csv(root / "data/phase_b/phase_b_target_codes.csv"):
        report.add("phase_b_target_codes must be empty")

    for r in read_csv(root / "data/phase_b/target_package_manifest.csv"):
        if r.get("coder_access_state") != "SEALED":
            report.add(f"target package {r.get('item_id')} must be SEALED")
        if r.get("prefilled_codes_exist", "").lower() == "true":
            report.add(f"target package {r.get('item_id')} prefilled codes forbidden")

    for r in read_csv(root / "data/phase_b/bdd_adjudication_blank.csv"):
        if (r.get("adjudicated_value") or "").strip():
            report.add(f"{r.get('decision_id')}: adjudicated_value must be blank before coding")
        if r.get("status") != "open_blank":
            report.add(f"{r.get('decision_id')}: status must remain open_blank")

    for r in read_csv(root / "data/phase_b/coding_form_schema.csv"):
        if r.get("field") in {"expected_answer", "adjudicated_answer"}:
            if r.get("required") != "forbidden":
                report.add(f"coding form field {r.get('field')} must be forbidden")

    for r in read_csv(root / "data/phase_b/synthetic_workflow_state.csv"):
        if r.get("real_gates_affected", "").lower() == "true":
            report.add("synthetic workflow must not affect real gates")

    for r in read_csv(root / "data/phase_b/unitization_template.csv"):
        if r.get("is_pe", "").strip():
            report.add("unitization template must not contain PE judgments")
        if r.get("TEMPLATE_ONLY", "").lower() != "true":
            report.add("unitization template rows must be TEMPLATE_ONLY")

    # Pilot status governance keys
    pilot = root / "data/pilot/PILOT_STATUS.txt"
    if pilot.exists():
        text = pilot.read_text(encoding="utf-8")
        for req in (
            "QUALIFICATION_FREEZE=AUTHORIZED",
            "ATTEMPT_POLICY=ADOPTED",
            "INDEPENDENT_CODER=NOT_READY",
            "TARGET_PACKAGE=SEALED",
        ):
            if req not in text:
                report.add(f"{pilot}: missing {req}")

    for path in (root / "docs/phase_b/independent_coding").rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in EMAIL_RE.finditer(text):
            report.add(f"{path.relative_to(root)}: personal email in coder package docs")

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
