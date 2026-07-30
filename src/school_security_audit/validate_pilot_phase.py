"""Validation for two-phase pilot gates and Phase A artefacts."""

from __future__ import annotations

from pathlib import Path

from school_security_audit.constants import (
    BRANCH_B_FAMILY_F_FIELDS,
    BRANCH_B_STATUS,
    EXECUTABILITY_LOCI,
    EXECUTABILITY_RUNGS,
    REPO_ROOT,
)
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_coding import validate_coding
from school_security_audit.validate_metadata import ValidationReport

REQUIRED_LABELS = {
    "inference_flag": "NOT_FOR_SUBSTANTIVE_INFERENCE",
    "benchmark_flag": "NOT_FOR_BENCHMARK_COMPARISON",
    "protocol_flag": "PROTOCOL_DEVELOPMENT_ONLY",
}

PHASE_A_PILOT_IDS = {"P1", "P2", "P3", "P4"}
PHASE_A_CANDIDATES = {"CF-16", "CF-03", "CF-15", "CF-13"}
FORBIDDEN_PHASE_A = {"P5", "CF-02"}

GATE_IDS = {
    "complete_pilot_source_gate",
    "operational_pilot_gate",
    "benchmark_calibration_gate",
    "corpus_freeze_gate",
    "full_coding_gate",
}


def validate_gate_register(root: Path, report: ValidationReport) -> None:
    path = root / "data/gates/gate_register.csv"
    if not path.exists():
        report.add(f"missing gate register: {path}")
        return
    rows = read_csv(path)
    found = {r.get("gate_id", "").strip() for r in rows}
    missing = GATE_IDS - found
    if missing:
        report.add(f"{path}: missing gate_id(s): {', '.join(sorted(missing))}")
    by_id = {r.get("gate_id", "").strip(): r for r in rows}

    complete = by_id.get("complete_pilot_source_gate", {})
    complete_status = complete.get("status", "").strip()
    p5_ready = _p5_ready(root)
    if not p5_ready and complete_status != "NO_GO":
        report.add(
            f"{path}: complete_pilot_source_gate must be NO_GO while operational P5 unauthorized"
        )
    if p5_ready and complete_status not in {"GO", "CONDITIONAL_GO"}:
        report.add(
            f"{path}: complete_pilot_source_gate should be GO or CONDITIONAL_GO when "
            "operational Phase-B source is ready (OPT-B)"
        )

    # Calibration / freeze / full coding remain NO_GO until execution + freeze criteria
    for gid in ("benchmark_calibration_gate", "corpus_freeze_gate", "full_coding_gate"):
        status = by_id.get(gid, {}).get("status", "").strip()
        if status != "NO_GO":
            report.add(f"{path}: {gid} must remain NO_GO until Phase B execution / freeze criteria met")

    op = by_id.get("operational_pilot_gate", {}).get("status", "").strip()
    if op not in {"GO", "CONDITIONAL_GO", "COMPLETED", "NO_GO"}:
        report.add(f"{path}: operational_pilot_gate has unexpected status '{op}'")


def _p5_ready(root: Path) -> bool:
    path = root / "data/source_registry/pilot_source_readiness.csv"
    if not path.exists():
        return False
    for row in read_csv(path):
        if row.get("pilot_id", "").strip() == "P5":
            return row.get("pilot_usable", "").strip().lower() == "true"
    return False


def validate_phase_a_membership(root: Path, report: ValidationReport) -> None:
    pe_path = root / "data/pilot/prescriptive_elements.csv"
    if not pe_path.exists():
        return
    rows = read_csv(pe_path)
    if not rows:
        return
    for i, row in enumerate(rows, start=2):
        phase = row.get("pilot_phase", "").strip()
        if phase and phase != "A_operational":
            report.add(f"{pe_path}:{i}: unexpected pilot_phase '{phase}'")
        pid = row.get("pilot_id", "").strip()
        cid = row.get("candidate_id", "").strip()
        if pid in FORBIDDEN_PHASE_A or cid in FORBIDDEN_PHASE_A:
            report.add(f"{pe_path}:{i}: P5/CF-02 must not appear in Phase A sample")
        if pid and pid not in PHASE_A_PILOT_IDS:
            report.add(f"{pe_path}:{i}: pilot_id '{pid}' not in operational_pilot_sample")
        if cid and cid not in PHASE_A_CANDIDATES:
            report.add(f"{pe_path}:{i}: candidate_id '{cid}' not in operational_pilot_sample")
        for field, expected in REQUIRED_LABELS.items():
            val = row.get(field, "").strip()
            if val != expected:
                report.add(f"{pe_path}:{i}: {field} must be '{expected}' (got '{val}')")
        excerpt = row.get("verbatim_trigger_text", "")
        if len(excerpt) > 180:
            report.add(
                f"{pe_path}:{i}: public verbatim_trigger_text too long "
                f"({len(excerpt)} chars); keep short stem / use gitignored excerpts"
            )


def validate_coding_labels_and_branch_b(root: Path, report: ValidationReport) -> None:
    for name in (
        "coding_coder_A.csv",
        "coding_coder_B_procedural.csv",
        "coding_adjudicated.csv",
    ):
        path = root / "data/pilot" / name
        if not path.exists():
            continue
        rows = read_csv(path)
        if not rows:
            continue
        coding_report = validate_coding(
            root,
            coding_path=path,
            pe_path=root / "data/pilot/prescriptive_elements.csv",
        )
        for err in coding_report.errors:
            report.add(err)
        for i, row in enumerate(rows, start=2):
            for field, expected in REQUIRED_LABELS.items():
                val = row.get(field, "").strip()
                if val != expected:
                    report.add(f"{path}:{i}: {field} must be '{expected}'")
            if row.get("pilot_phase", "").strip() not in {"", "A_operational"}:
                report.add(f"{path}:{i}: pilot_phase must be A_operational")
            rung = row.get("executability_rung", "").strip()
            if rung and rung not in EXECUTABILITY_RUNGS:
                report.add(f"{path}:{i}: invalid rung")
            locus = row.get("executability_locus", "").strip()
            if locus and locus not in EXECUTABILITY_LOCI:
                report.add(f"{path}:{i}: invalid locus")
            # Branch B inactivity for Phase A aggregates: Family F fields must be empty
            # unless analysis_scope explicitly marks out-of-scope note-only rows.
            scope = row.get("analysis_scope", "").strip()
            if scope == "branch_a_executability":
                for f in BRANCH_B_FAMILY_F_FIELDS:
                    if row.get(f, "").strip() != "":
                        report.add(
                            f"{path}:{i}: Branch B field '{f}' must be empty when "
                            f"analysis_scope=branch_a_executability "
                            f"(BRANCH_B_STATUS={BRANCH_B_STATUS})"
                        )
            # ambiguous_memo must not be treated as presence (already in validate_coding)


def validate_no_phase_a_in_final_coding(root: Path, report: ValidationReport) -> None:
    final_coding = root / "data/coding/coding_template.csv"
    if not final_coding.exists():
        return
    rows = read_csv(final_coding)
    for i, row in enumerate(rows, start=2):
        pe = row.get("pe_id", "").strip()
        if pe.startswith("PE-OPA-"):
            report.add(
                f"{final_coding}:{i}: Phase A pe_id '{pe}' must not enter final coding path"
            )


def validate_status_files(root: Path, report: ValidationReport) -> None:
    source_gate = root / "data/pilot/PILOT_SOURCE_GATE.txt"
    if source_gate.exists():
        text = source_gate.read_text(encoding="utf-8")
        if not _p5_ready(root) and "PILOT_SOURCE_NO_GO" not in text:
            report.add(f"{source_gate}: must retain PILOT_SOURCE_NO_GO while P5 blocked")
        if _p5_ready(root) and "OPERATIONAL_COMPARATOR_READY" not in text:
            report.add(
                f"{source_gate}: expected OPERATIONAL_COMPARATOR_READY when OPT-B source ready"
            )
        if _p5_ready(root) and "DO_NOT_EQUATE_SOURCE_READY_WITH_PHASE_B_COMPLETE=true" not in text:
            report.add(
                f"{source_gate}: must warn that source readiness ≠ Phase B completion"
            )
        if "NOT_FOR_SUBSTANTIVE_INFERENCE" not in text:
            report.add(f"{source_gate}: missing NOT_FOR_SUBSTANTIVE_INFERENCE")

    status = root / "data/pilot/PILOT_STATUS.txt"
    if status.exists():
        text = status.read_text(encoding="utf-8")
        if "NOT_FOR_SUBSTANTIVE_INFERENCE" not in text:
            report.add(f"{status}: missing NOT_FOR_SUBSTANTIVE_INFERENCE")
        if "COMPLETE_PILOT=INCOMPLETE" not in text:
            report.add(f"{status}: COMPLETE_PILOT must remain INCOMPLETE until Phase B executed")
        if "BENCHMARK_CALIBRATION=NO_GO" not in text:
            report.add(f"{status}: BENCHMARK_CALIBRATION must remain NO_GO until execution")
        if "CORPUS_FREEZE=" in text and "CORPUS_FREEZE=NO_GO" not in text:
            report.add(f"{status}: CORPUS_FREEZE must be NO_GO")
        if "FULL_CODING=" in text and "FULL_CODING=NO_GO" not in text:
            report.add(f"{status}: FULL_CODING must be NO_GO")


def validate_pilot_phase(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()
    validate_gate_register(root, report)
    validate_phase_a_membership(root, report)
    validate_coding_labels_and_branch_b(root, report)
    validate_no_phase_a_in_final_coding(root, report)
    validate_status_files(root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_pilot_phase()
    if report.ok:
        print("Pilot-phase validation OK.")
        return 0
    print("Pilot-phase validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
