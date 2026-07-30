"""Check training/qualification materials for target leakage."""

from __future__ import annotations

import re
from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

TARGET_MARKERS = (
    "DOC-ALT-FNSS-001",
    "fnssfinalguidance",
    "FEMA_2010_FNSS",
    "ab21f61b8ee451adb5cb6ca79dabf3305cdaea4a742ed7478b42ef6becf464a7",
)

CODER_FACING = [
    "docs/phase_b/independent_coding/training/",
    "docs/phase_b/independent_coding/training_package.md",
    "docs/phase_b/independent_coding/qualification/coder_facing_instructions.md",
    "docs/phase_b/independent_coding/coder_role.md",
    "docs/phase_b/independent_coding/forms/",
    "data/phase_b/qualification_cases.csv",
]


def check_training_overlap(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()

    for r in read_csv(root / "data/phase_b/qualification_cases.csv"):
        if r.get("PHASE_B_TARGET", "").lower() == "true":
            report.add(f"qualification case {r.get('case_id')} marked PHASE_B_TARGET")
        if r.get("source_status") != "synthetic_constructed":
            report.add(f"qualification case {r.get('case_id')} not synthetic_constructed")

    paths: list[Path] = []
    for rel in CODER_FACING:
        p = root / rel
        if p.is_dir():
            paths.extend(p.rglob("*"))
        elif p.exists():
            paths.append(p)

    for path in paths:
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".csv", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # Answer key must not be embedded
        if "pe_count_expected" in text and "qualification_cases" not in path.name:
            if "WITHHOLD" not in text and path.name != "qualification_reference.csv":
                # training docs shouldn't contain answer-key column names
                if "qualification_reference" not in text:
                    report.add(f"{path.relative_to(root)}: possible answer-key fields in coder-facing file")
        for marker in TARGET_MARKERS:
            if marker in text:
                # Allow role description mentioning FNSS as operational L1 conceptually
                if path.name == "coder_role.md" and marker == "DOC-ALT-FNSS-001":
                    continue
                if path.name == "training_guide.md" and "FEMA FNSS" in text and marker.startswith("ab21"):
                    continue
                # Full checksum or filename in coder-facing training is leakage risk
                if marker.startswith("ab21") or "fnssfinal" in marker.lower() or "FEMA_2010" in marker:
                    report.add(f"{path.relative_to(root)}: target marker {marker}")

    # Reference must not be listed as coder-facing in package manifest
    for r in read_csv(root / "data/phase_b/coder_package_manifest.csv"):
        if r.get("file_path", "").endswith("qualification_reference.csv"):
            if r.get("access_class") != "WITHHOLD_FROM_CODER":
                report.add("qualification_reference must be WITHHOLD_FROM_CODER")

    overlap = root / "data/phase_b/training_target_overlap_report.csv"
    if overlap.exists():
        for r in read_csv(overlap):
            if r.get("result") == "fail":
                report.add(f"overlap report {r.get('check_id')}: fail")

    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = check_training_overlap()
    if report.ok:
        print("Training/target overlap check OK.")
        return 0
    print("Training/target overlap check FAILED:")
    for e in report.errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
