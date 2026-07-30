"""Validate corpus metadata CSVs and related schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator

from school_security_audit.constants import (
    COMPARATOR_STATUSES,
    DOCUMENT_HEADERS,
    FRAMEWORK_HEADERS,
    PE_HEADERS,
    REPO_ROOT,
)
from school_security_audit.io_utils import csv_headers, load_json, missing_headers, read_csv


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, message: str) -> None:
        self.errors.append(message)


def _validate_headers(path: Path, required: list[str], report: ValidationReport) -> None:
    actual = csv_headers(path)
    missing = missing_headers(actual, required)
    if missing:
        report.add(f"{path}: missing required headers: {', '.join(missing)}")


def validate_framework_rows(
    rows: list[dict[str, str]],
    schema: dict,
    report: ValidationReport,
    *,
    path_label: str = "frameworks",
) -> set[str]:
    validator = Draft202012Validator(schema)
    ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        fid = row.get("framework_id", "").strip()
        if not fid:
            report.add(f"{path_label}:{i}: empty framework_id")
            continue
        if fid in ids:
            report.add(f"{path_label}:{i}: duplicate framework_id '{fid}'")
        ids.add(fid)
        status = row.get("comparator_status", "").strip()
        if status and status not in COMPARATOR_STATUSES:
            report.add(
                f"{path_label}:{i}: invalid comparator_status '{status}' "
                f"(use benchmark_comparator, not experimental positive_control)"
            )
        # JSON Schema validation on non-empty fields of interest
        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: e.path):
            report.add(f"{path_label}:{i}: schema: {err.message}")
    return ids


def validate_document_rows(
    rows: list[dict[str, str]],
    framework_ids: set[str],
    schema: dict,
    report: ValidationReport,
    *,
    path_label: str = "documents",
    require_known_framework: bool = True,
) -> set[str]:
    validator = Draft202012Validator(schema)
    ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        did = row.get("document_id", "").strip()
        fid = row.get("framework_id", "").strip()
        if not did:
            report.add(f"{path_label}:{i}: empty document_id")
            continue
        if did in ids:
            report.add(f"{path_label}:{i}: duplicate document_id '{did}'")
        ids.add(did)
        if require_known_framework and fid and fid not in framework_ids:
            report.add(f"{path_label}:{i}: orphan framework_id '{fid}' (no matching framework)")
        if row.get("inclusion_status") == "excluded" and not row.get("exclusion_reason", "").strip():
            report.add(f"{path_label}:{i}: exclusion_reason required when inclusion_status=excluded")
        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: e.path):
            report.add(f"{path_label}:{i}: schema: {err.message}")
    return ids


def validate_pe_rows(
    rows: list[dict[str, str]],
    document_ids: set[str],
    schema: dict,
    report: ValidationReport,
    *,
    path_label: str = "prescriptive_elements",
    require_known_document: bool = True,
) -> set[str]:
    validator = Draft202012Validator(schema)
    ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        pe_id = row.get("pe_id", "").strip()
        did = row.get("document_id", "").strip()
        if not pe_id:
            report.add(f"{path_label}:{i}: empty pe_id")
            continue
        if pe_id in ids:
            report.add(f"{path_label}:{i}: duplicate pe_id '{pe_id}'")
        ids.add(pe_id)
        if require_known_document and did and did not in document_ids:
            report.add(f"{path_label}:{i}: orphan document_id '{did}' (no matching document)")
        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: e.path):
            report.add(f"{path_label}:{i}: schema: {err.message}")
    return ids


def validate_corpus(
    root: Path | None = None,
    *,
    frameworks_path: Path | None = None,
    documents_path: Path | None = None,
    pe_path: Path | None = None,
) -> ValidationReport:
    root = root or REPO_ROOT
    frameworks_path = frameworks_path or root / "data/corpus/candidate_frameworks.csv"
    documents_path = documents_path or root / "data/corpus/document_registry.csv"
    pe_path = pe_path or root / "data/coding/prescriptive_elements.csv"

    report = ValidationReport()
    for path, headers in (
        (frameworks_path, FRAMEWORK_HEADERS),
        (documents_path, DOCUMENT_HEADERS),
        (pe_path, PE_HEADERS),
    ):
        if not path.exists():
            report.add(f"missing file: {path}")
            return report
        _validate_headers(path, headers, report)

    if report.errors:
        return report

    fw_schema = load_json(root / "schemas/framework.schema.json")
    doc_schema = load_json(root / "schemas/document.schema.json")
    pe_schema = load_json(root / "schemas/prescriptive_element.schema.json")

    frameworks = read_csv(frameworks_path)
    documents = read_csv(documents_path)
    pes = read_csv(pe_path)

    fw_ids = validate_framework_rows(frameworks, fw_schema, report, path_label=str(frameworks_path))
    doc_ids = validate_document_rows(
        documents, fw_ids, doc_schema, report, path_label=str(documents_path)
    )
    validate_pe_rows(pes, doc_ids, pe_schema, report, path_label=str(pe_path))
    return report


def main(argv: list[str] | None = None) -> int:
    del argv  # reserved for future CLI flags
    report = validate_corpus()
    if report.ok:
        print("Metadata validation OK.")
        return 0
    print("Metadata validation FAILED:")
    for err in report.errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
