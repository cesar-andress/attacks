"""Validate corpus metadata CSVs and related schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator

from school_security_audit.constants import (
    CF22_ID,
    COMPARATOR_STATUSES,
    COUNTEREXAMPLE_HEADERS,
    DOCUMENT_HEADERS,
    FORBIDDEN_COUNTEREXAMPLE_TOKENS,
    FORBIDDEN_GEOGRAPHY_LABELS,
    FORBIDDEN_REGISTER_STATUSES,
    FORBIDDEN_SCREENING_OR_INCLUSION_VALUES,
    FRAMEWORK_HEADERS,
    FREEZE_DISPOSITION_VALUES,
    IDENTITY_STATUSES,
    OPENALEX_HEADERS,
    OPENALEX_VERIFICATION_STATUSES,
    PE_HEADERS,
    PROVENANCE_CONFIDENCE,
    REGISTER_STATUSES,
    REPO_ROOT,
    SCREENING_STATUSES,
    UNVERIFIED_IDENTITY_STATUSES,
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


def _check_forbidden_status_fields(row: dict[str, str], path_label: str, line: int, report: ValidationReport) -> None:
    for key in ("screening_status", "identity_status", "inclusion_status", "register_status"):
        value = row.get(key, "").strip()
        if value in FORBIDDEN_SCREENING_OR_INCLUSION_VALUES or value in FORBIDDEN_REGISTER_STATUSES:
            report.add(
                f"{path_label}:{line}: forbidden status value '{value}' in '{key}' "
                "(provisional register must not use final/frozen/included values)"
            )


def _check_geography(row: dict[str, str], path_label: str, line: int, report: ValidationReport) -> None:
    for key in ("geographic_region", "jurisdiction", "geographic_group"):
        value = row.get(key, "").strip()
        if value in FORBIDDEN_GEOGRAPHY_LABELS:
            report.add(
                f"{path_label}:{line}: forbidden geography label '{value}' "
                "(do not use EU/UK; use geographic_region=Europe and eu_member_state=no for UK/England)"
            )


def _require_unresolved_action_for_unverified(
    row: dict[str, str], path_label: str, line: int, report: ValidationReport
) -> None:
    identity = row.get("identity_status", "").strip()
    action = row.get("unresolved_verification_action", "").strip()
    if identity in UNVERIFIED_IDENTITY_STATUSES and not action:
        report.add(
            f"{path_label}:{line}: unresolved_verification_action required when "
            f"identity_status='{identity}'"
        )


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

        _check_forbidden_status_fields(row, path_label, i, report)
        _check_geography(row, path_label, i, report)
        _require_unresolved_action_for_unverified(row, path_label, i, report)

        identity = row.get("identity_status", "").strip()
        if identity and identity not in IDENTITY_STATUSES:
            report.add(f"{path_label}:{i}: invalid identity_status '{identity}'")

        screening = row.get("screening_status", "").strip()
        if screening and screening not in SCREENING_STATUSES:
            report.add(f"{path_label}:{i}: invalid screening_status '{screening}'")

        provenance = row.get("provenance_confidence", "").strip()
        if provenance and provenance not in PROVENANCE_CONFIDENCE:
            report.add(f"{path_label}:{i}: invalid provenance_confidence '{provenance}'")

        comparator = row.get("comparator_status", "").strip()
        if comparator and comparator not in COMPARATOR_STATUSES:
            report.add(
                f"{path_label}:{i}: invalid comparator_status '{comparator}' "
                "(use benchmark_comparator_candidate / frame_candidate / not_comparator)"
            )

        register_status = row.get("register_status", "").strip()
        if register_status and register_status not in REGISTER_STATUSES:
            report.add(
                f"{path_label}:{i}: invalid register_status '{register_status}' "
                "(only provisional_v0.1 is allowed; corpus is not frozen)"
            )

        # CF-22 must remain unverified
        if fid == CF22_ID:
            if identity == "candidate_verified_identity":
                report.add(
                    f"{path_label}:{i}: CF-22 must not be marked candidate_verified_identity "
                    "(no citable framework/document identified yet)"
                )
            if provenance == "verified_official_source":
                report.add(
                    f"{path_label}:{i}: CF-22 must not claim verified_official_source provenance"
                )

        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
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

        _check_forbidden_status_fields(row, path_label, i, report)
        _check_geography(row, path_label, i, report)
        _require_unresolved_action_for_unverified(row, path_label, i, report)

        if fid == CF22_ID and row.get("identity_status", "").strip() == "candidate_verified_identity":
            report.add(f"{path_label}:{i}: CF-22 document cannot be marked verified")

        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
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
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
            report.add(f"{path_label}:{i}: schema: {err.message}")
    return ids


def validate_openalex_rows(
    rows: list[dict[str, str]],
    framework_ids: set[str],
    schema: dict,
    report: ValidationReport,
    *,
    path_label: str = "openalex",
) -> None:
    validator = Draft202012Validator(schema)
    for i, row in enumerate(rows, start=2):
        for key in ("OPEN_ALEX_KEY", "api_key", "apikey"):
            blob = " ".join(row.values())
            if key in blob:
                report.add(f"{path_label}:{i}: possible API key material detected in field values")

        cid = row.get("candidate_id", "").strip()
        if framework_ids and cid and cid not in framework_ids:
            report.add(f"{path_label}:{i}: orphan candidate_id '{cid}'")

        status = row.get("verification_status", "").strip()
        if status and status not in OPENALEX_VERIFICATION_STATUSES:
            report.add(f"{path_label}:{i}: invalid verification_status '{status}'")

        if row.get("does_not_authorize_corpus_inclusion", "").strip() != "true":
            report.add(
                f"{path_label}:{i}: does_not_authorize_corpus_inclusion must be 'true' "
                "(OpenAlex hits do not authorize corpus inclusion)"
            )

        required_retained = [
            "openalex_work_id",
            "title",
            "authors",
            "publication_year",
            "source_or_journal",
            "retrieval_date",
            "verification_status",
        ]
        for field_name in required_retained:
            if not row.get(field_name, "").strip():
                report.add(f"{path_label}:{i}: missing required OpenAlex field '{field_name}'")

        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
            report.add(f"{path_label}:{i}: schema: {err.message}")


def validate_counterexample_rows(
    rows: list[dict[str, str]],
    framework_ids: set[str],
    schema: dict,
    report: ValidationReport,
    *,
    path_label: str = "counterexamples",
) -> None:
    validator = Draft202012Validator(schema)
    for i, row in enumerate(rows, start=2):
        cid = row.get("candidate_id", "").strip()
        if not cid:
            report.add(f"{path_label}:{i}: empty candidate_id")
            continue
        if framework_ids and cid not in framework_ids:
            report.add(f"{path_label}:{i}: orphan candidate_id '{cid}'")

        surface = row.get("surface_indication", "")
        lowered = surface.lower()
        for token in FORBIDDEN_COUNTEREXAMPLE_TOKENS:
            if token.lower() in lowered:
                report.add(
                    f"{path_label}:{i}: surface_indication contains forbidden audit/codebook token "
                    f"'{token}' (surface indications are not coded findings)"
                )

        warning = row.get("warning_not_coded_finding", "").strip()
        if "NOT_A_CODED_FINDING" not in warning:
            report.add(
                f"{path_label}:{i}: warning_not_coded_finding must explicitly state NOT_A_CODED_FINDING"
            )

        payload = {k: v for k, v in row.items() if v != ""}
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
            report.add(f"{path_label}:{i}: schema: {err.message}")


def validate_corpus(
    root: Path | None = None,
    *,
    frameworks_path: Path | None = None,
    documents_path: Path | None = None,
    pe_path: Path | None = None,
    counterexamples_path: Path | None = None,
    openalex_path: Path | None = None,
) -> ValidationReport:
    root = root or REPO_ROOT
    frameworks_path = frameworks_path or root / "data/corpus/candidate_frameworks.csv"
    documents_path = documents_path or root / "data/corpus/document_registry.csv"
    pe_path = pe_path or root / "data/coding/prescriptive_elements.csv"
    counterexamples_path = (
        counterexamples_path or root / "data/corpus/counterexample_commitments.csv"
    )
    openalex_path = openalex_path or root / "data/corpus/openalex_literature_verifications.csv"

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

    if not counterexamples_path.exists():
        report.add(f"missing file: {counterexamples_path}")
    else:
        _validate_headers(counterexamples_path, COUNTEREXAMPLE_HEADERS, report)

    if not openalex_path.exists():
        report.add(f"missing file: {openalex_path}")
    else:
        _validate_headers(openalex_path, OPENALEX_HEADERS, report)

    if report.errors:
        return report

    fw_schema = load_json(root / "schemas/framework.schema.json")
    doc_schema = load_json(root / "schemas/document.schema.json")
    pe_schema = load_json(root / "schemas/prescriptive_element.schema.json")
    cx_schema = load_json(root / "schemas/counterexample_commitment.schema.json")
    oa_schema = load_json(root / "schemas/openalex_literature_verification.schema.json")

    frameworks = read_csv(frameworks_path)
    documents = read_csv(documents_path)
    pes = read_csv(pe_path)
    counterexamples = read_csv(counterexamples_path) if counterexamples_path.exists() else []
    openalex_rows = read_csv(openalex_path) if openalex_path.exists() else []

    # Reject affirmative claims that the corpus has been frozen (allow "not frozen")
    for path_label, rows in (
        (str(frameworks_path), frameworks),
        (str(documents_path), documents),
    ):
        for i, row in enumerate(rows, start=2):
            blob = " ".join(row.values()).lower()
            if "not frozen" in blob or "not a frozen" in blob or "is not frozen" in blob:
                continue
            if "corpus is frozen" in blob or "corpus has been frozen" in blob:
                report.add(f"{path_label}:{i}: claim that the corpus is frozen is forbidden")
            if row.get("register_status", "").strip() in FORBIDDEN_REGISTER_STATUSES:
                report.add(f"{path_label}:{i}: register_status must not be frozen/final")

    fw_ids = validate_framework_rows(frameworks, fw_schema, report, path_label=str(frameworks_path))
    doc_ids = validate_document_rows(
        documents, fw_ids, doc_schema, report, path_label=str(documents_path)
    )
    validate_pe_rows(pes, doc_ids, pe_schema, report, path_label=str(pe_path))
    validate_counterexample_rows(
        counterexamples, fw_ids, cx_schema, report, path_label=str(counterexamples_path)
    )
    validate_openalex_rows(
        openalex_rows, fw_ids, oa_schema, report, path_label=str(openalex_path)
    )

    # Freeze/pilot artefacts are validated only when checking the live corpus paths,
    # not when unit tests pass fixture CSVs via explicit path arguments.
    default_fw = root / "data/corpus/candidate_frameworks.csv"
    if frameworks_path.resolve() == default_fw.resolve():
        disposition_path = root / "data/corpus/candidate_disposition_recommendations.csv"
        if disposition_path.exists():
            _validate_disposition_recommendations(disposition_path, fw_ids, report)

        freeze_reg = root / "data/corpus/freeze_readiness_register.csv"
        if freeze_reg.exists():
            headers = set(csv_headers(freeze_reg))
            for required in ("issue_id", "blocking_status", "final_status"):
                if required not in headers:
                    report.add(f"{freeze_reg}: missing header '{required}'")

        pilot_status = root / "data/pilot/PILOT_STATUS.txt"
        if pilot_status.exists():
            text = pilot_status.read_text(encoding="utf-8")
            if "NOT_FOR_SUBSTANTIVE_INFERENCE" not in text:
                report.add(f"{pilot_status}: must declare NOT_FOR_SUBSTANTIVE_INFERENCE")
            for coding_name in (
                "coding_coder_A.csv",
                "coding_coder_B_procedural.csv",
                "coding_adjudicated.csv",
                "prescriptive_elements.csv",
            ):
                coding_file = root / "data/pilot" / coding_name
                if not coding_file.exists():
                    continue
                for i, row in enumerate(read_csv(coding_file), start=2):
                    flag = row.get("inference_flag", "").strip()
                    if flag and flag != "NOT_FOR_SUBSTANTIVE_INFERENCE":
                        report.add(
                            f"{coding_file}:{i}: inference_flag must be "
                            "NOT_FOR_SUBSTANTIVE_INFERENCE when present"
                        )

    return report


def _validate_disposition_recommendations(
    path: Path, fw_ids: set[str], report: ValidationReport
) -> None:
    rows = read_csv(path)
    for i, row in enumerate(rows, start=2):
        fid = row.get("framework_id", "").strip()
        if fid and fid not in fw_ids:
            report.add(f"{path}:{i}: unknown framework_id '{fid}'")
        disp = row.get("recommended_freeze_disposition", "").strip()
        if disp and disp not in FREEZE_DISPOSITION_VALUES:
            report.add(f"{path}:{i}: invalid recommended_freeze_disposition '{disp}'")
        if row.get("NOT_A_FROZEN_INCLUSION", "").strip().lower() not in {"true", "1", "yes"}:
            report.add(f"{path}:{i}: NOT_A_FROZEN_INCLUSION must be true")
        # Disposition file must not use forbidden screening inclusion tokens as disposition
        if disp in FORBIDDEN_SCREENING_OR_INCLUSION_VALUES:
            report.add(f"{path}:{i}: disposition must not use frozen/final inclusion tokens")


def main(argv: list[str] | None = None) -> int:
    del argv
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
