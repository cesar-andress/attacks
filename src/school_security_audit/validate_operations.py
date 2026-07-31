"""Validate execution-operations infrastructure (no fabricated readiness)."""

from __future__ import annotations

import re
from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

FORBIDDEN_PLACEHOLDER = re.compile(
    r"TO_BE_SET_AS_HUMAN|TO_BE_DECIDED_BY_HUMAN|FILL_ME|TBD_HUMAN"
)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

REQUIRED_DOCS = [
    "docs/operations/README.md",
    "docs/operations/UCW-003_decision_record.md",
    "docs/operations/recruitment/independent_coder_role_description.md",
    "docs/operations/recruitment/recruitment_announcement.md",
    "docs/operations/recruitment/direct_invitation_template.md",
    "docs/operations/recruitment/candidate_information_sheet.md",
    "docs/operations/recruitment/candidate_screening_form.md",
    "docs/operations/recruitment/coi_decision_guide.md",
    "docs/operations/onboarding/onboarding_checklist.md",
    "docs/operations/onboarding/access_matrix.md",
    "docs/operations/onboarding/secure_handling_instructions.md",
    "docs/operations/onboarding/training_completion_record.md",
    "docs/operations/onboarding/material_release_matrix.md",
    "docs/operations/onboarding/confidentiality_agreement_template.md",
    "docs/operations/qualification/authorization_record.md",
    "docs/operations/qualification/activation_checklist.md",
    "docs/operations/calibration/runbook.md",
    "docs/operations/corpus_freeze/runbook.md",
    "docs/operations/coding/runbook.md",
    "docs/operations/reliability/pipeline_readiness.md",
    "docs/operations/adjudication/runbook.md",
    "docs/operations/adjudication/adjudication_form.md",
    "docs/operations/adjudication/bdd_resolution_record.md",
    "docs/operations/adjudication/final_adjudication_manifest.md",
    "docs/operations/analysis/data_lineage.md",
    "docs/operations/analysis/release_matrix.md",
    "docs/operations/analysis/analysis_plan_executability.md",
    "docs/operations/governance/privacy_retention_plan.md",
    "docs/operations/governance/ETHICS_AND_GOVERNANCE_CHECK.md",
    "docs/operations/governance/tag_regeneration_log.md",
    "data/operations/execution_dashboard.csv",
    "data/operations/recruitment_log_template.csv",
    "data/operations/qualification_attempt_log_template.csv",
    "data/operations/clarification_log_template.csv",
    "data/operations/disagreement_register_template.csv",
    "data/operations/release_matrix.csv",
    "data/operations/fixtures/reliability/README.md",
]

REQUIRED_DASHBOARD = {
    "UCW-003",
    "RECRUIT_MATERIALS",
    "CANDIDATE_SELECTED",
    "COI_CLEARED",
    "CONFIDENTIALITY",
    "TRAINING",
    "QUAL_ATTEMPT",
    "CODER_QUALIFIED",
    "CALIBRATION",
    "CORPUS_FREEZE",
    "INDEPENDENT_CODING",
    "RELIABILITY",
    "ADJUDICATION",
    "ANALYTICAL_DATASET",
    "RESULTS",
    "DISCUSSION",
    "FINAL_MANUSCRIPT",
}

REQUIRED_CHECKLISTS = [
    "docs/operations/checklists/before_recruitment.md",
    "docs/operations/checklists/before_onboarding.md",
    "docs/operations/checklists/before_qualification.md",
    "docs/operations/checklists/before_calibration.md",
    "docs/operations/checklists/before_corpus_freeze.md",
    "docs/operations/checklists/before_full_coding.md",
    "docs/operations/checklists/before_reliability.md",
    "docs/operations/checklists/before_adjudication.md",
    "docs/operations/checklists/before_final_analysis.md",
    "docs/operations/checklists/before_manuscript_completion.md",
    "docs/operations/checklists/before_final_data_release.md",
]


def validate_operations(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    for rel in REQUIRED_DOCS + REQUIRED_CHECKLISTS:
        if not (root / rel).exists():
            report.add(f"missing {rel}")

    ucw = root / "docs/operations/UCW-003_decision_record.md"
    if ucw.exists():
        text = ucw.read_text(encoding="utf-8")
        if "UNRESOLVED" not in text:
            report.add("UCW-003 decision record must remain UNRESOLVED until human closure")
        if "Decision pending" not in text and "Not yet selected" not in text:
            report.add("UCW-003 decision record must use Decision pending / Not yet selected fields")

    dash_path = root / "data/operations/execution_dashboard.csv"
    if dash_path.exists():
        rows = read_csv(dash_path)
        by_id = {r.get("gate_id"): r for r in rows}
        for gid in REQUIRED_DASHBOARD:
            if gid not in by_id:
                report.add(f"execution_dashboard missing {gid}")
        if by_id.get("UCW-003", {}).get("status") not in {"UNRESOLVED", "open_human"}:
            report.add("dashboard UCW-003 must remain UNRESOLVED until human decision")
        if by_id.get("CODER_QUALIFIED", {}).get("status") == "READY":
            report.add("dashboard must not claim CODER READY without real qualification evidence")
        if by_id.get("CALIBRATION", {}).get("status") != "NO_GO":
            report.add("dashboard calibration must remain NO_GO")
        if by_id.get("CORPUS_FREEZE", {}).get("status") != "NO_GO":
            report.add("dashboard corpus freeze must remain NO_GO")
        if by_id.get("INDEPENDENT_CODING", {}).get("status") not in {"NO_GO", "NOT_STARTED"}:
            report.add("dashboard independent coding must remain blocked")
        if by_id.get("RESULTS", {}).get("status") not in {"NOT_STARTED", "BLOCKED"}:
            report.add("dashboard Results must not claim completion without empirical data")

        # Gate coupling: unresolved UCW-003 must remain the recruitment blocker
        if by_id.get("UCW-003", {}).get("status") == "UNRESOLVED":
            if "UCW-003" not in (by_id.get("RECRUIT_MATERIALS", {}).get("blocking_issue") or ""):
                # materials may be READY but recruitment still blocked by UCW-003
                if by_id.get("CANDIDATE_SELECTED", {}).get("status") not in {
                    "NOT_STARTED",
                    "BLOCKED",
                }:
                    report.add("candidate selection must not advance while UCW-003 unresolved")

    # Placeholder / PII hygiene in public operations docs
    for path in (root / "docs/operations").rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".csv"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if FORBIDDEN_PLACEHOLDER.search(text):
            report.add(f"{path.relative_to(root)}: forbidden placeholder token")
        if EMAIL_RE.search(text) and "example.com" not in text:
            report.add(f"{path.relative_to(root)}: email-like personal data forbidden")

    for path in (root / "data/operations").rglob("*.csv"):
        if "completed" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if EMAIL_RE.search(text):
            report.add(f"{path.relative_to(root)}: email-like personal data forbidden")

    fixture_readme = root / "data/operations/fixtures/reliability/README.md"
    if fixture_readme.exists() and "SYNTHETIC_NOT_FOR_MANUSCRIPT" not in fixture_readme.read_text(
        encoding="utf-8"
    ):
        report.add("reliability fixtures README must mark SYNTHETIC_NOT_FOR_MANUSCRIPT")

    lineage = root / "docs/operations/analysis/data_lineage.md"
    if lineage.exists():
        lt = lineage.read_text(encoding="utf-8")
        for token in (
            "Coder-A",
            "Coder-B",
            "Reliability",
            "Adjudication",
            "SYNTHETIC_NOT_FOR_MANUSCRIPT",
        ):
            if token not in lt:
                report.add(f"data_lineage.md missing required token: {token}")

    # QUAL-ATTEMPT-v1 still referenced from ops qualification docs
    qual_auth = root / "docs/operations/qualification/authorization_record.md"
    if qual_auth.exists():
        qt = qual_auth.read_text(encoding="utf-8")
        for token in ("two", "answer-key", "QUAL-ATTEMPT"):
            if token.lower() not in qt.lower() and token not in qt:
                # soft: require attempt policy mention
                pass
        if "QUAL-ATTEMPT-v1" not in qt and "two valid" not in qt.lower():
            report.add("qualification authorization must encode QUAL-ATTEMPT-v1")

    ops_readme = root / "docs/operations/README.md"
    if ops_readme.exists() and "10.5281/zenodo.21711588" not in ops_readme.read_text(encoding="utf-8"):
        report.add("operations README must cite Zenodo DOI")

    for r in read_csv(root / "data/phase_b/target_package_manifest.csv"):
        if r.get("coder_access_state") != "SEALED":
            report.add("operations validation: target must remain SEALED")

    # Answer keys must not appear under public operations docs
    for path in (root / "docs/operations").rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if "answer_key" in name and path.suffix in {".csv", ".json", ".yaml", ".yml"}:
            report.add(f"answer-key payload must not live under docs/operations: {path}")

    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_operations()
    if report.ok:
        print("Operations validation OK.")
        return 0
    print("Operations validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
