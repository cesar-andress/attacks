"""Validate coding records against codebook rules and schemas."""

from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator

from school_security_audit.constants import (
    CODING_REQUIRED_HEADERS,
    CONFIRMATORY_DEMAND_SOURCES,
    DEMAND_FIELDS,
    DEMAND_SOURCES,
    EXECUTABILITY_LOCI,
    EXECUTABILITY_RUNGS,
    FORBIDDEN_COMPOSITE_FIELDS,
    REPO_ROOT,
)
from school_security_audit.io_utils import csv_headers, load_json, load_yaml, missing_headers, read_csv
from school_security_audit.validate_metadata import ValidationReport


def load_codebook_versions(codebook_path: Path) -> set[str]:
    data = load_yaml(codebook_path)
    versions = set()
    if isinstance(data, dict):
        if data.get("codebook_version"):
            versions.add(str(data["codebook_version"]))
        for code in data.get("codes") or []:
            if code.get("version_introduced"):
                versions.add(str(code["version_introduced"]))
    return versions


def confirmatory_demand_presence(row: dict[str, str], demand_field: str) -> bool:
    """Return True only when demand is present AND source is confirmatory."""
    value = row.get(demand_field, "").strip()
    source = row.get(f"{demand_field}_source", "").strip()
    if value != "1":
        return False
    if source == "ambiguous_memo":
        return False
    return source in CONFIRMATORY_DEMAND_SOURCES


def validate_coding_rows(
    rows: list[dict[str, str]],
    *,
    pe_ids: set[str] | None,
    codebook_versions: set[str],
    schema: dict,
    report: ValidationReport,
    path_label: str = "coding",
    require_known_pe: bool = True,
) -> None:
    headers = set(rows[0].keys()) if rows else set()
    # Also check header-only files via caller; for rows, inspect keys on first row
    forbidden_hit = FORBIDDEN_COMPOSITE_FIELDS.intersection(headers)
    if forbidden_hit:
        report.add(
            f"{path_label}: forbidden composite score field(s): {', '.join(sorted(forbidden_hit))} "
            "(Branch E and Branch F must remain separate)"
        )

    validator = Draft202012Validator(schema)

    for i, row in enumerate(rows, start=2):
        row_forbidden = FORBIDDEN_COMPOSITE_FIELDS.intersection(row.keys())
        for field in row_forbidden:
            if str(row.get(field, "")).strip() != "":
                report.add(
                    f"{path_label}:{i}: populated forbidden composite field '{field}' "
                    "(do not collapse executability and detectability)"
                )

        pe_id = row.get("pe_id", "").strip()
        if not pe_id:
            report.add(f"{path_label}:{i}: empty pe_id")
        elif require_known_pe and pe_ids is not None and pe_id not in pe_ids:
            report.add(f"{path_label}:{i}: orphan pe_id '{pe_id}'")

        cb_version = row.get("codebook_version", "").strip()
        if cb_version and cb_version not in codebook_versions:
            report.add(
                f"{path_label}:{i}: unknown codebook_version '{cb_version}' "
                f"(known: {', '.join(sorted(codebook_versions)) or 'none'})"
            )

        rung = row.get("executability_rung", "").strip()
        if rung not in EXECUTABILITY_RUNGS:
            report.add(f"{path_label}:{i}: invalid executability_rung '{rung}'")

        locus = row.get("executability_locus", "").strip()
        if locus not in EXECUTABILITY_LOCI:
            report.add(f"{path_label}:{i}: invalid executability_locus '{locus}'")

        for demand in DEMAND_FIELDS:
            value = row.get(demand, "").strip()
            source = row.get(f"{demand}_source", "").strip()
            trigger = row.get(f"{demand}_trigger", "").strip()

            if source and source not in DEMAND_SOURCES:
                report.add(f"{path_label}:{i}: invalid {demand}_source '{source}'")

            if value == "1" and source == "ambiguous_memo":
                report.add(
                    f"{path_label}:{i}: demand '{demand}' marked present with "
                    "demand_source=ambiguous_memo (ambiguous_memo must not count as presence; "
                    "set value=0 and keep memo, or resolve to explicit/entailed)"
                )

            if value == "1" and source == "entailed" and not trigger:
                report.add(
                    f"{path_label}:{i}: entailed demand '{demand}' requires non-empty trigger evidence"
                )

            if value == "1" and source not in CONFIRMATORY_DEMAND_SOURCES and source != "ambiguous_memo":
                if source == "":
                    report.add(
                        f"{path_label}:{i}: demand '{demand}' present without demand_source"
                    )

            # Confirmatory helper must never treat ambiguous_memo as presence
            if value == "1" and source == "ambiguous_memo":
                assert confirmatory_demand_presence(row, demand) is False

        payload = {k: v for k, v in row.items() if v != "" and k not in FORBIDDEN_COMPOSITE_FIELDS}
        # Validate against schema only if no forbidden fields populated
        if not any(str(row.get(f, "")).strip() for f in FORBIDDEN_COMPOSITE_FIELDS if f in row):
            for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
                report.add(f"{path_label}:{i}: schema: {err.message}")


def validate_coding(
    root: Path | None = None,
    *,
    coding_path: Path | None = None,
    pe_path: Path | None = None,
    codebook_path: Path | None = None,
    allow_empty: bool = True,
) -> ValidationReport:
    root = root or REPO_ROOT
    coding_path = coding_path or root / "data/coding/coding_template.csv"
    pe_path = pe_path or root / "data/coding/prescriptive_elements.csv"
    codebook_path = codebook_path or root / "docs/codebook/codebook_v0.1.yaml"

    report = ValidationReport()
    if not coding_path.exists():
        report.add(f"missing file: {coding_path}")
        return report
    if not codebook_path.exists():
        report.add(f"missing file: {codebook_path}")
        return report

    headers = csv_headers(coding_path)
    missing = missing_headers(headers, CODING_REQUIRED_HEADERS)
    if missing:
        report.add(f"{coding_path}: missing required headers: {', '.join(missing)}")
        return report

    forbidden = FORBIDDEN_COMPOSITE_FIELDS.intersection(headers)
    if forbidden:
        report.add(
            f"{coding_path}: forbidden composite score field(s) in header: "
            f"{', '.join(sorted(forbidden))}"
        )

    rows = read_csv(coding_path)
    if not rows and allow_empty:
        return report

    pe_ids: set[str] | None = None
    if pe_path.exists():
        pe_ids = {
            r.get("pe_id", "").strip()
            for r in read_csv(pe_path)
            if r.get("pe_id", "").strip()
        }

    codebook_versions = load_codebook_versions(codebook_path)
    schema = load_json(root / "schemas/coding_record.schema.json")
    validate_coding_rows(
        rows,
        pe_ids=pe_ids,
        codebook_versions=codebook_versions,
        schema=schema,
        report=report,
        path_label=str(coding_path),
        require_known_pe=bool(pe_ids),
    )
    return report


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_coding()
    if report.ok:
        print("Coding validation OK.")
        return 0
    print("Coding validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
