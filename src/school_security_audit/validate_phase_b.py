"""Validate Phase-B benchmark preparation artefacts without opening calibration gate."""

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
    "docs/phase_b/README.md",
    "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md",
]

OPTION_IDS = {"OPT-A", "OPT-B", "OPT-C", "OPT-D"}
GATE_OUTCOMES = {
    "CF02_ACCESS_GO",
    "OPERATIONAL_L1_AMENDMENT_RECOMMENDED",
    "DUAL_BENCHMARK_RECOMMENDED",
    "BENCHMARK_DESIGN_NO_GO",
    "CF02_ACCESS_NO_GO",
    "OPERATIONAL_L1_AVAILABLE_PENDING_AMENDMENT",
}
CLASSIFICATIONS = {
    "unsuitable",
    "citation_only",
    "supplementary_benchmark",
    "potential_operational_L1",
    "preferred_operational_L1",
    "requires_protocol_amendment",
}


def validate_phase_b(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            report.add(f"missing {rel}")

    # Target codes must be empty (header only)
    target = root / "data/phase_b/phase_b_target_codes.csv"
    if target.exists():
        rows = read_csv(target)
        if rows:
            report.add(
                f"{target}: Phase-B target codes must be empty before execution "
                f"(found {len(rows)} rows)"
            )

    # Amendment options
    opt_path = root / "data/phase_b/amendment_options.csv"
    if opt_path.exists():
        opts = {r.get("option_id", "").strip() for r in read_csv(opt_path)}
        if opts != OPTION_IDS:
            report.add(f"{opt_path}: expected {sorted(OPTION_IDS)}, found {sorted(opts)}")
        for r in read_csv(opt_path):
            if r.get("status", "").strip() not in {
                "proposed_not_enacted",
                "adopted",
                "rejected",
            }:
                report.add(f"{opt_path}: invalid status {r.get('status')!r}")
            if r.get("status", "").strip() == "adopted":
                # If somehow adopted, draft file should not still say NOT_ADOPTED — checked below
                pass

    # Draft amendment must remain not adopted
    draft = root / "docs/protocol/amendments/PA-DRAFT-002_operational_fnss_comparator.md"
    if draft.exists():
        text = draft.read_text(encoding="utf-8")
        if "DRAFT_NOT_ADOPTED" not in text:
            report.add(f"{draft}: must remain DRAFT_NOT_ADOPTED until human approval")

    # Gate outcomes
    gate_path = root / "data/phase_b/benchmark_design_gate.csv"
    if gate_path.exists():
        rows = read_csv(gate_path)
        by_id = {r.get("gate_id", "").strip(): r for r in rows}
        main = by_id.get("benchmark_design_gate", {})
        if main.get("outcome", "").strip() not in GATE_OUTCOMES:
            report.add(f"{gate_path}: invalid benchmark_design_gate outcome")
        if main.get("benchmark_calibration_status", "").strip() != "NO_GO":
            report.add(
                f"{gate_path}: benchmark_calibration_status must remain NO_GO "
                "until Phase B executed"
            )
        if main.get("enacted_amendment", "").strip() not in {"", "none"}:
            # enacted_amendment should be none while draft
            if "DRAFT" in (main.get("enacted_amendment") or ""):
                report.add(f"{gate_path}: draft amendment must not be marked enacted")

    # Alternative classifications
    alt_path = root / "data/phase_b/alternative_candidates.csv"
    if alt_path.exists():
        for i, r in enumerate(read_csv(alt_path), start=2):
            cls = r.get("classification", "").strip()
            if cls not in CLASSIFICATIONS:
                report.add(f"{alt_path}:{i}: invalid classification {cls!r}")
            # No silent preferred replacement without amendment
            if cls == "preferred_operational_L1" and "amendment" not in (
                r.get("recommendation", "").lower()
            ):
                report.add(
                    f"{alt_path}:{i}: preferred_operational_L1 requires amendment note"
                )

    # CF-02 must still be blocked in authorized_source_status
    auth = root / "data/phase_b/authorized_source_status.csv"
    if auth.exists():
        for r in read_csv(auth):
            if r.get("candidate_id", "").strip() == "CF-02":
                if r.get("usable_for_phase_b_coding", "").strip().lower() == "true":
                    report.add(f"{auth}: CF-02 must not be marked usable without access")
                if r.get("authorization_status", "").strip() not in {
                    "access_restricted",
                    "unavailable",
                    "copyright_unclear",
                }:
                    # allow only restricted-like statuses while blocked
                    if r.get("local_file_status", "").strip() not in {"none", ""}:
                        report.add(f"{auth}: CF-02 unexpected local_file_status")

    # Qualification cases must not be Phase-B targets
    qpath = root / "data/phase_b/qualification_cases.csv"
    if qpath.exists():
        for i, r in enumerate(read_csv(qpath), start=2):
            if r.get("PHASE_B_TARGET", "").strip().lower() == "true":
                report.add(f"{qpath}:{i}: qualification case marked as Phase-B target")
            if r.get("source_status", "").strip() != "synthetic_constructed":
                report.add(f"{qpath}:{i}: qualification cases must be synthetic_constructed")

    # Pilot status / gates still NO_GO
    pilot = root / "data/pilot/PILOT_STATUS.txt"
    if pilot.exists():
        text = pilot.read_text(encoding="utf-8")
        if "BENCHMARK_CALIBRATION=NO_GO" not in text:
            report.add(f"{pilot}: BENCHMARK_CALIBRATION must remain NO_GO")
        if "COMPLETE_PILOT=INCOMPLETE" not in text:
            report.add(f"{pilot}: COMPLETE_PILOT must remain INCOMPLETE")
        if "CORPUS_FREEZE=NO_GO" not in text:
            report.add(f"{pilot}: CORPUS_FREEZE must remain NO_GO")

    gates = root / "data/gates/gate_register.csv"
    if gates.exists():
        by_id = {r.get("gate_id", "").strip(): r for r in read_csv(gates)}
        for gid in (
            "benchmark_calibration_gate",
            "corpus_freeze_gate",
            "full_coding_gate",
            "complete_pilot_source_gate",
        ):
            if by_id.get(gid, {}).get("status", "").strip() != "NO_GO":
                report.add(f"{gates}: {gid} must remain NO_GO")

    # RP-P2 still planned
    papers = root / "docs/research_program/paper_dependency_register.csv"
    if papers.exists():
        for r in read_csv(papers):
            if r.get("paper_id") == "RP-P2" and r.get("status", "").strip() != "planned":
                report.add(f"{papers}: RP-P2 must remain planned")

    # No claim that simulated pass is independent
    if pilot.exists() and "simulated_procedural_second_pass" in pilot.read_text(
        encoding="utf-8"
    ):
        if "EMPIRICAL_INTERCODER_RELIABILITY=not_computed" not in pilot.read_text(
            encoding="utf-8"
        ):
            report.add(f"{pilot}: empirical reliability must remain not_computed")

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
