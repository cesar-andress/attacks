"""Lightweight validation for research-programme registers."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

PAPER_IDS = {"RP-P1", "RP-P2", "RP-P3", "RP-P4"}
PAPER_STATUSES = {"active", "planned"}
DOMAIN_IDS = {"A", "B", "C", "D", "E", "F", "G", "H"}
FORBIDDEN_SCORE_TOKENS = {
    "inclusive_security_score",
    "combined_executability_detectability_score",
    "inclusive_security_index",
    "total_preparedness_rank",
}
FORBIDDEN_VALIDATED_STATUSES = {"validated", "validated_instrument", "implemented_validated"}


def _program_dir(root: Path) -> Path:
    return root / "docs/research_program"


def validate_paper_register(root: Path, report: ValidationReport) -> None:
    path = _program_dir(root) / "paper_dependency_register.csv"
    if not path.exists():
        report.add(f"missing {path}")
        return
    rows = read_csv(path)
    found = {r.get("paper_id", "").strip() for r in rows}
    if found != PAPER_IDS:
        report.add(
            f"{path}: expected paper_ids {sorted(PAPER_IDS)}, found {sorted(found)}"
        )
    by_id = {r.get("paper_id", "").strip(): r for r in rows}
    if by_id.get("RP-P1", {}).get("status", "").strip() != "active":
        report.add(f"{path}: RP-P1 status must be 'active'")
    for pid in ("RP-P2", "RP-P3", "RP-P4"):
        st = by_id.get(pid, {}).get("status", "").strip()
        if st != "planned":
            report.add(f"{path}: {pid} status must be 'planned' (got '{st}')")
    # RP-P1 and RP-P4 must remain separate entries
    if "RP-P1" in by_id and "RP-P4" in by_id:
        p1_scope = by_id["RP-P1"].get("excluded_scope", "").lower()
        if "detectability" not in p1_scope and "threat" not in p1_scope:
            report.add(f"{path}: RP-P1 excluded_scope should mention detectability exclusion")
    header_blob = ",".join(rows[0].keys()).lower() if rows else ""
    for tok in FORBIDDEN_SCORE_TOKENS:
        if tok in header_blob:
            report.add(f"{path}: forbidden single-score field in header: {tok}")
    for i, row in enumerate(rows, start=2):
        st = row.get("status", "").strip()
        if st not in PAPER_STATUSES:
            report.add(f"{path}:{i}: invalid status '{st}'")
        deps = row.get("dependencies", "").strip()
        if row.get("paper_id") == "RP-P2" and "RP-P1" not in deps:
            report.add(f"{path}:{i}: RP-P2 must depend on RP-P1")
        if row.get("paper_id") == "RP-P3":
            if "RP-P1" not in deps or "RP-P2" not in deps:
                report.add(f"{path}:{i}: RP-P3 must depend on RP-P1 and RP-P2")


def validate_slapa_domains(root: Path, report: ValidationReport) -> None:
    path = _program_dir(root) / "slapa_domains.csv"
    if not path.exists():
        report.add(f"missing {path}")
        return
    rows = read_csv(path)
    found = {r.get("domain_id", "").strip() for r in rows}
    if found != DOMAIN_IDS:
        report.add(f"{path}: expected domains {sorted(DOMAIN_IDS)}, found {sorted(found)}")
    for i, row in enumerate(rows, start=2):
        status = row.get("validation_status", "").strip()
        if status in FORBIDDEN_VALIDATED_STATUSES:
            report.add(f"{path}:{i}: domain must not be marked validated")
        if status and status != "planned_unvalidated":
            report.add(
                f"{path}:{i}: validation_status must be planned_unvalidated (got '{status}')"
            )
        blob = " ".join(row.values()).lower()
        for tok in FORBIDDEN_SCORE_TOKENS:
            if tok in blob.replace("-", "_"):
                report.add(f"{path}:{i}: forbidden single-score token '{tok}'")


def validate_traceability(root: Path, report: ValidationReport) -> None:
    path = _program_dir(root) / "paper1_slapa_traceability.csv"
    if not path.exists():
        report.add(f"missing {path}")
        return
    rows = read_csv(path)
    if len(rows) < 10:
        report.add(f"{path}: expected a substantial traceability mapping (>=10 rows)")
    required_vars = {
        "prescription_presence_measure_present",
        "support_specification_support_present",
        "executability_engagement_rung",
        "executability_locus",
        "demand_source_explicit_entailed_ambiguous_memo",
        "ambiguous_memo",
    }
    found_vars = {r.get("paper1_variable", "").strip() for r in rows}
    missing = required_vars - found_vars
    if missing:
        report.add(f"{path}: missing required variables: {', '.join(sorted(missing))}")
    for i, row in enumerate(rows, start=2):
        domains = row.get("slapa_domain", "").strip()
        if domains in {"", "method_only"}:
            continue
        for part in domains.replace(";", ",").split(","):
            d = part.strip()
            if d and d not in DOMAIN_IDS:
                report.add(f"{path}:{i}: invalid domain ref '{d}'")


def validate_required_markdown(root: Path, report: ValidationReport) -> None:
    required = [
        "programme_charter.md",
        "paper_dependency_register.md",
        "slapa_architecture.md",
        "evidence_layers.md",
        "branch_b_detectability.md",
        "validation_roadmap.md",
        "comparison_safeguards.md",
        "future_claims_policy.md",
        "five_year_roadmap.md",
        "operational_priorities.md",
        "README.md",
    ]
    base = _program_dir(root)
    for name in required:
        if not (base / name).exists():
            report.add(f"missing {base / name}")


def validate_no_p1_p4_merge_language(root: Path, report: ValidationReport) -> None:
    charter = _program_dir(root) / "programme_charter.md"
    if not charter.exists():
        return
    text = charter.read_text(encoding="utf-8").lower()
    if "do not merge rp-p1 and rp-p4" not in text and "do not merge" not in text:
        report.add(f"{charter}: should state RP-P1 and RP-P4 must not be merged")
    if "empirical foundation" not in text:
        report.add(f"{charter}: should state Paper 1 is the empirical foundation")


def validate_research_program(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()
    validate_required_markdown(root, report)
    validate_paper_register(root, report)
    validate_slapa_domains(root, report)
    validate_traceability(root, report)
    validate_no_p1_p4_merge_language(root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_research_program()
    if report.ok:
        print("Research-programme validation OK.")
        return 0
    print("Research-programme validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
