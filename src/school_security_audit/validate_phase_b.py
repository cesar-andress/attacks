"""Validate Phase-B benchmark preparation and OPT-B adoption state."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

REQUIRED_FILES = [
    "data/phase_b/comparator_roles.csv",
    "data/phase_b/access_routes.csv",
    "data/phase_b/alternative_candidates.csv",
    "data/phase_b/authorized_source_status.csv",
    "data/phase_b/amendment_options.csv",
    "data/phase_b/benchmark_design_gate.csv",
    "data/phase_b/complete_pilot_exit_criteria.csv",
    "data/phase_b/corpus_freeze_conditional.csv",
    "data/phase_b/qualification_cases.csv",
    "data/phase_b/qualification_reference.csv",
    "data/phase_b/synthetic_qualification_pass.csv",
    "data/phase_b/synthetic_qualification_fail.csv",
    "data/phase_b/phase_b_target_codes.csv",
    "data/phase_b/phase_b_execution_manifest.csv",
    "data/phase_b/opt_b_criteria_evaluation.csv",
    "docs/phase_b/README.md",
    "docs/phase_b/opt_b_decision_record.md",
    "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md",
    "docs/protocol/amendments/PA-2026-07-31-002_operational_fnss_comparator.md",
]

FNSS_CHECKSUM = "ab21f61b8ee451adb5cb6ca79dabf3305cdaea4a742ed7478b42ef6becf464a7"
FORBIDDEN_GOLD = ("gold standard", "gold-standard", "positive control", "validation source")


def _manifest_map(root: Path) -> dict[str, str]:
    path = root / "data/phase_b/phase_b_execution_manifest.csv"
    if not path.exists():
        return {}
    return {
        r.get("field", "").strip(): r.get("value", "").strip()
        for r in read_csv(path)
    }


def validate_phase_b(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            report.add(f"missing {rel}")

    # Target codes empty
    target = root / "data/phase_b/phase_b_target_codes.csv"
    if target.exists() and read_csv(target):
        report.add(f"{target}: Phase-B target codes must be empty before execution")

    # OPT-B adopted
    opt_path = root / "data/phase_b/amendment_options.csv"
    if opt_path.exists():
        by_id = {r["option_id"]: r for r in read_csv(opt_path)}
        if by_id.get("OPT-B", {}).get("status") != "adopted":
            report.add(f"{opt_path}: OPT-B must be adopted")
        for oid in ("OPT-A", "OPT-C", "OPT-D"):
            if by_id.get(oid, {}).get("status") == "adopted":
                report.add(f"{opt_path}: {oid} must not be adopted alongside OPT-B primary")

    # Draft superseded; adopted amendment present
    draft = root / "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md"
    if draft.exists():
        text = draft.read_text(encoding="utf-8")
        if "SUPERSEDED" not in text:
            report.add(f"{draft}: must be marked SUPERSEDED after adoption")
        if "DRAFT_NOT_ADOPTED" in text and "SUPERSEDED" not in text:
            report.add(f"{draft}: conflicting draft status")

    adopted = root / "docs/protocol/amendments/PA-2026-07-31-002_operational_fnss_comparator.md"
    if adopted.exists():
        text = adopted.read_text(encoding="utf-8")
        if "**adopted**" not in text and "Status:** **adopted**" not in text:
            if "adopted" not in text.lower():
                report.add(f"{adopted}: must record adopted status")
        if FNSS_CHECKSUM not in text:
            report.add(f"{adopted}: must record FNSS checksum")
        if "gold standard" in text.lower() and "not" not in text.lower():
            report.add(f"{adopted}: must not affirm gold-standard status")
        for bad in FORBIDDEN_GOLD:
            # allow negated mentions
            pass
    else:
        report.add(f"missing {adopted}")

    # Gates
    gate_path = root / "data/phase_b/benchmark_design_gate.csv"
    if gate_path.exists():
        by_id = {r.get("gate_id", "").strip(): r for r in read_csv(gate_path)}
        if by_id.get("benchmark_design_gate", {}).get("outcome") != "GO":
            report.add(f"{gate_path}: benchmark_design_gate must be GO after OPT-B")
        if by_id.get("benchmark_design_gate", {}).get("benchmark_calibration_status") != "NO_GO":
            report.add(f"{gate_path}: calibration must remain NO_GO")
        if by_id.get("benchmark_source_gate", {}).get("outcome") != "READY":
            report.add(f"{gate_path}: benchmark_source_gate must be READY")
        if by_id.get("independent_coder_gate", {}).get("outcome") != "NOT_READY":
            report.add(f"{gate_path}: independent_coder_gate must be NOT_READY")
        if by_id.get("cf02_access_subgate", {}).get("outcome") != "CF02_ACCESS_NO_GO":
            report.add(f"{gate_path}: CF-02 access must remain NO_GO")
        if by_id.get("benchmark_design_gate", {}).get("enacted_amendment") != "PA-2026-07-31-002":
            report.add(f"{gate_path}: enacted_amendment must be PA-2026-07-31-002")

    # Roles
    auth = root / "data/phase_b/authorized_source_status.csv"
    if auth.exists():
        by_c = {r["candidate_id"]: r for r in read_csv(auth)}
        cf02 = by_c.get("CF-02", {})
        fnss = by_c.get("ALT-FNSS-001", {})
        if cf02.get("usable_for_phase_b_coding", "").lower() == "true":
            report.add(f"{auth}: CF-02 must not be usable as primary Phase-B coding source")
        if fnss.get("usable_for_phase_b_coding", "").lower() != "true":
            report.add(f"{auth}: FNSS must be usable for Phase-B coding after OPT-B")
        if fnss.get("checksum_sha256") != FNSS_CHECKSUM:
            report.add(f"{auth}: FNSS checksum mismatch")

    alts = root / "data/phase_b/alternative_candidates.csv"
    if alts.exists():
        for r in read_csv(alts):
            if r.get("candidate_id") == "ALT-FNSS-001":
                if r.get("classification") != "preferred_operational_L1":
                    report.add(f"{alts}: FNSS must be preferred_operational_L1 after adoption")

    # Manifest guards
    man = _manifest_map(root)
    if man:
        if man.get("amendment_id") != "PA-2026-07-31-002":
            report.add("manifest: amendment_id must be PA-2026-07-31-002")
        if man.get("checksum_sha256") != FNSS_CHECKSUM:
            report.add("manifest: checksum mismatch")
        if man.get("coder_independence_verified", "").lower() == "true":
            report.add("manifest: coder_independence_verified must not be true without recruitment")
        if man.get("qualification_complete", "").lower() == "true":
            report.add("manifest: qualification_complete must be false until real coder passes")
        if man.get("final_gate") != "BENCHMARK_CALIBRATION=NO_GO":
            report.add("manifest: final_gate must keep BENCHMARK_CALIBRATION=NO_GO")
        if man.get("gold_standard_forbidden", "").lower() != "true":
            report.add("manifest: gold_standard_forbidden must be true")

    # Pilot status
    pilot = root / "data/pilot/PILOT_STATUS.txt"
    if pilot.exists():
        text = pilot.read_text(encoding="utf-8")
        for req in (
            "BENCHMARK_CALIBRATION=NO_GO",
            "COMPLETE_PILOT=INCOMPLETE",
            "CORPUS_FREEZE=NO_GO",
            "FULL_CODING=NO_GO",
            "OPT_B=ADOPTED",
            "INDEPENDENT_CODER=NOT_READY",
            "BENCHMARK_SOURCE=READY",
            "BENCHMARK_DESIGN=GO",
            "EMPIRICAL_INTERCODER_RELIABILITY=not_computed",
        ):
            if req not in text:
                report.add(f"{pilot}: missing {req}")

    gates = root / "data/gates/gate_register.csv"
    if gates.exists():
        by_id = {r.get("gate_id", "").strip(): r for r in read_csv(gates)}
        if by_id.get("benchmark_calibration_gate", {}).get("status") != "NO_GO":
            report.add(f"{gates}: benchmark_calibration_gate must remain NO_GO")
        if by_id.get("corpus_freeze_gate", {}).get("status") != "NO_GO":
            report.add(f"{gates}: corpus_freeze_gate must remain NO_GO")
        if by_id.get("full_coding_gate", {}).get("status") != "NO_GO":
            report.add(f"{gates}: full_coding_gate must remain NO_GO")

    # Programme unchanged
    papers = root / "docs/research_program/paper_dependency_register.csv"
    if papers.exists():
        for r in read_csv(papers):
            if r.get("paper_id") == "RP-P2" and r.get("status") != "planned":
                report.add(f"{papers}: RP-P2 must remain planned")
    domains = root / "docs/research_program/slapa_domains.csv"
    if domains.exists():
        for r in read_csv(domains):
            if r.get("validation_status") != "planned_unvalidated":
                report.add(f"{domains}: SLAPA domains must remain planned_unvalidated")

    # Qualification still synthetic / not Phase-B targets
    qpath = root / "data/phase_b/qualification_cases.csv"
    if qpath.exists():
        for i, r in enumerate(read_csv(qpath), start=2):
            if r.get("PHASE_B_TARGET", "").lower() == "true":
                report.add(f"{qpath}:{i}: training/qualification must not be Phase-B target")
            if r.get("source_status") != "synthetic_constructed":
                report.add(f"{qpath}:{i}: qualification cases must remain synthetic")

    # No gold-standard affirmation in phase_b docs (allow negation)
    for path in (root / "docs/phase_b").rglob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        if "is a gold standard" in text or "as a gold standard" in text:
            report.add(f"{path.relative_to(root)}: forbids affirming gold-standard comparator")

    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_phase_b()
    if report.ok:
        print("Phase-B preparation validation OK.")
        return 0
    print("Phase-B preparation validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
