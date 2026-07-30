"""Experimental Development Pack — validation and synthetic analysis."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv
from school_security_audit.validate_metadata import ValidationReport

EXPERIMENT_IDS = {f"EXP-0{i}" for i in range(1, 7)}
ALLOWED_STATUS = {"designed_not_executed", "internally_tested_synthetic", "piloted", "independently_replicated", "content_validated", "field_validated"}
DOMAIN_IDS = set("ABCDEFGH")
LAYERS = {"1", "2", "3", "4", "5"}
FORBIDDEN_TOTAL_FIELDS = {"total_readiness_score", "inclusive_security_score", "slapa_total_score"}
NON_INDEPENDENT_PASS = {"simulated_procedural_second_pass"}


def experiments_root(root: Path | None = None) -> Path:
    return (root or REPO_ROOT) / "experiments"


def validate_experiment_register(root: Path, report: ValidationReport) -> None:
    path = experiments_root(root) / "experiment_register.csv"
    if not path.exists():
        report.add(f"missing {path}")
        return
    rows = read_csv(path)
    found = {r.get("experiment_id", "").strip() for r in rows}
    if found != EXPERIMENT_IDS:
        report.add(f"{path}: expected {sorted(EXPERIMENT_IDS)}, found {sorted(found)}")
    for i, row in enumerate(rows, start=2):
        st = row.get("current_status", "").strip()
        if st not in ALLOWED_STATUS:
            report.add(f"{path}:{i}: invalid status '{st}'")
        if st not in {"designed_not_executed", "internally_tested_synthetic"}:
            # higher maturity requires explicit evidence beyond this pack
            report.add(
                f"{path}:{i}: maturity '{st}' not supported without additional evidence "
                "(keep designed_not_executed or internally_tested_synthetic)"
            )
        if "executed" in row.get("claims_permitted", "").lower() and "not" not in row.get("claims_permitted", "").lower():
            pass
        prohibited = row.get("claims_prohibited", "").lower()
        if "validated slapa" not in prohibited and "slapa is validated" not in prohibited:
            if "validated" not in prohibited:
                report.add(f"{path}:{i}: claims_prohibited should block premature validation claims")


def validate_no_restricted_or_pii(root: Path, report: ValidationReport) -> None:
    bad_tokens = [
        "kailes",
        "@gmail",
        "ssn",
        "passport",
        "real school:",
        "localhost password",
    ]
    for path in experiments_root(root).rglob("*"):
        if path.is_file() and path.suffix.lower() in {".csv", ".md", ".json", ".yaml", ".yml", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for tok in bad_tokens:
                if tok in text:
                    report.add(f"{path}: forbidden/sensitive token '{tok}'")
            if path.suffix == ".csv":
                # scan headers for total scores populated
                rows = read_csv(path)
                headers = set(rows[0].keys()) if rows else set(csv_headers_safe(path))
                for f in FORBIDDEN_TOTAL_FIELDS:
                    if f in headers:
                        for i, row in enumerate(rows, start=2):
                            if str(row.get(f, "")).strip() not in {"", "FORBIDDEN", "must_remain_empty"}:
                                report.add(
                                    f"{path}:{i}: forbidden total-score field '{f}' is populated"
                                )


def csv_headers_safe(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


def validate_exp_materials(root: Path, report: ValidationReport) -> None:
    exp = experiments_root(root)
    # EXP-01
    cases = read_csv(exp / "EXP-01_unitization/materials/cases.csv")
    ref = {r["case_id"]: r for r in read_csv(exp / "EXP-01_unitization/reference/reference_adjudication.csv")}
    if not (20 <= len(cases) <= 30):
        report.add(f"EXP-01: expected 20–30 cases, found {len(cases)}")
    for c in cases:
        if c["case_id"] not in ref:
            report.add(f"EXP-01: missing reference for {c['case_id']}")
        if ref.get(c["case_id"], {}).get("reference_label") != "REFERENCE_ADJUDICATION":
            report.add(f"EXP-01: reference must be REFERENCE_ADJUDICATION for {c['case_id']}")
        if c.get("source_status") != "synthetic_constructed":
            report.add(f"EXP-01: non-synthetic source_status for {c['case_id']}")

    # EXP-02
    cases2 = read_csv(exp / "EXP-02_coding_decisions/materials/cases.csv")
    ref2 = {r["case_id"]: r for r in read_csv(exp / "EXP-02_coding_decisions/reference/reference_adjudication.csv")}
    if not (24 <= len(cases2) <= 40):
        report.add(f"EXP-02: expected 24–40 cases, found {len(cases2)}")
    for c in cases2:
        if c["case_id"] not in ref2:
            report.add(f"EXP-02: missing reference for {c['case_id']}")

    # EXP-03
    items = read_csv(exp / "EXP-03_codebook_usability/materials/item_register.csv")
    ids = [r["item_id"] for r in items]
    if len(ids) != len(set(ids)):
        report.add("EXP-03: duplicate item_id")
    for r in items:
        if r.get("psychometric_claim") not in {"none", ""}:
            report.add(f"EXP-03: item {r['item_id']} must not claim psychometric validation")

    # EXP-04
    cases4 = read_csv(exp / "EXP-04_evidence_layers/materials/cases.csv")
    ref4 = read_csv(exp / "EXP-04_evidence_layers/reference/reference_adjudication.csv")
    if not (15 <= len(cases4) <= 20):
        report.add(f"EXP-04: expected 15–20 cases, found {len(cases4)}")
    for r in ref4:
        if r.get("reference_layer") not in LAYERS:
            report.add(f"EXP-04: invalid layer {r.get('reference_layer')}")

    # EXP-05
    domains = read_csv(exp / "EXP-05_slapa_content_mapping/materials/domains.csv")
    found = {r["domain_id"] for r in domains}
    if found != DOMAIN_IDS:
        report.add(f"EXP-05: domain IDs mismatch {found}")
    for r in domains:
        if r.get("validation_status") != "planned_unvalidated":
            report.add("EXP-05: domains must remain planned_unvalidated")

    # EXP-06
    schools = read_csv(exp / "EXP-06_synthetic_school_assessment/materials/synthetic_cases.csv")
    if len(schools) < 2:
        report.add("EXP-06: need at least 2 synthetic cases")
    for r in schools:
        if "fictional" not in r.get("fictional_disclaimer", "").lower():
            report.add(f"EXP-06: missing fictional disclaimer on {r.get('case_id')}")


def validate_experiments(root: Path | None = None) -> ValidationReport:
    root = root or REPO_ROOT
    report = ValidationReport()
    if not experiments_root(root).exists():
        report.add("missing experiments/ directory")
        return report
    validate_experiment_register(root, report)
    validate_exp_materials(root, report)
    validate_no_restricted_or_pii(root, report)
    for name in (
        "README.md",
        "experiment_register.md",
        "ethics_readiness_checklist.md",
        "data_management_plan.md",
        "analysis_plans.md",
    ):
        if not (experiments_root(root) / name).exists():
            report.add(f"missing experiments/{name}")
    return report


# --- Analysis helpers ---

def analyze_unitization(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    exp = experiments_root(root) / "EXP-01_unitization"
    ref = {r["case_id"]: int(r["reference_unit_count"]) for r in read_csv(exp / "reference/reference_adjudication.csv")}
    results = {"study_label": "synthetic_demonstration", "experiment_id": "EXP-01", "participants": {}}
    for path in sorted((exp / "responses").glob("synthetic_coder_*.csv")):
        rows = read_csv(path)
        pid = rows[0]["participant_id"]
        exact = 0
        total = 0
        for row in rows:
            total += 1
            if int(row["units_identified"]) == ref[row["case_id"]]:
                exact += 1
        results["participants"][pid] = {
            "n_cases": total,
            "exact_match_to_reference": exact,
            "exact_match_rate": exact / total if total else 0.0,
            "reference_label": "REFERENCE_ADJUDICATION",
            "not_ground_truth": True,
        }
    # pairwise if both
    if len(results["participants"]) >= 2:
        a = {r["case_id"]: int(r["units_identified"]) for r in read_csv(exp / "responses/synthetic_coder_A.csv")}
        b = {r["case_id"]: int(r["units_identified"]) for r in read_csv(exp / "responses/synthetic_coder_B.csv")}
        agree = sum(1 for k in a if a[k] == b[k])
        results["pairwise_unit_count_agreement"] = agree / len(a)
    return results


def analyze_coding(root: Path | None = None, response_paths: list[Path] | None = None) -> dict:
    root = root or REPO_ROOT
    exp = experiments_root(root) / "EXP-02_coding_decisions"
    ref = {r["case_id"]: r for r in read_csv(exp / "reference/reference_adjudication.csv")}
    if response_paths is None:
        response_paths = [
            exp / "responses/synthetic_coder_A.csv",
            exp / "responses/synthetic_coder_B.csv",
        ]
    out: dict = {
        "study_label": "synthetic_demonstration",
        "experiment_id": "EXP-02",
        "empirical_intercoder_reliability": None,
        "reliability_blocked_reason": None,
        "participants": {},
    }
    pass_types = set()
    for path in response_paths:
        rows = read_csv(path)
        if not rows:
            continue
        pid = rows[0]["participant_id"]
        pt = rows[0].get("pass_type", "")
        pass_types.add(pt)
        rung_agree = 0
        n = 0
        for row in rows:
            n += 1
            if row.get("executability_rung") == ref[row["case_id"]].get("executability_rung"):
                rung_agree += 1
        out["participants"][pid] = {
            "n": n,
            "rung_agreement_vs_reference": rung_agree / n if n else 0.0,
            "pass_type": pt,
        }
    if pass_types & NON_INDEPENDENT_PASS:
        out["empirical_intercoder_reliability"] = "NOT_COMPUTED"
        out["reliability_blocked_reason"] = (
            "Metadata include simulated_procedural_second_pass; "
            "empirical Krippendorff's alpha must not be reported."
        )
    elif len(response_paths) >= 2 and pass_types <= {"independent_human"}:
        # Still do not invent alpha without a proper library/implementation;
        # report raw agreement only for synthetic demo.
        a = {r["case_id"]: r["executability_rung"] for r in read_csv(response_paths[0])}
        b = {r["case_id"]: r["executability_rung"] for r in read_csv(response_paths[1])}
        keys = sorted(set(a) & set(b))
        raw = sum(1 for k in keys if a[k] == b[k]) / len(keys) if keys else 0.0
        out["raw_rung_agreement"] = raw
        out["empirical_intercoder_reliability"] = "NOT_COMPUTED_DEMO_ONLY_RAW_AGREEMENT"
        out["note"] = "Full alpha reserved for genuinely independent coder studies."
    return out


def analyze_usability(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    path = experiments_root(root) / "EXP-03_codebook_usability/responses/synthetic_responses.csv"
    rows = read_csv(path)
    numeric = defaultdict(list)
    for r in rows:
        try:
            val = float(r["response_value"])
        except ValueError:
            continue
        numeric[r["item_id"]].append(val)
    means = {k: sum(v) / len(v) for k, v in numeric.items() if v}
    return {
        "study_label": "synthetic_demonstration",
        "experiment_id": "EXP-03",
        "item_means": means,
        "psychometric_validation_claimed": False,
        "n_response_rows": len(rows),
    }


def analyze_layers(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    exp = experiments_root(root) / "EXP-04_evidence_layers"
    ref = {r["case_id"]: r["reference_layer"] for r in read_csv(exp / "reference/reference_adjudication.csv")}
    rows = read_csv(exp / "responses/synthetic_responses.csv")
    by_pid: dict[str, list] = defaultdict(list)
    for r in rows:
        by_pid[r["participant_id"]].append(r)
    conf: dict = {}
    for pid, items in by_pid.items():
        correct = sum(1 for r in items if r["assigned_layer"] == ref[r["case_id"]])
        conf[pid] = {"accuracy": correct / len(items), "n": len(items)}
    # confusion pairs
    pairs = Counter()
    for r in rows:
        pairs[(ref[r["case_id"]], r["assigned_layer"])] += 1
    return {
        "study_label": "synthetic_demonstration",
        "experiment_id": "EXP-04",
        "participants": conf,
        "confusion_counts": {f"{a}->{b}": n for (a, b), n in pairs.items()},
    }


def analyze_cvi(root: Path | None = None) -> dict:
    """Simplified I-CVI: proportion of experts rating relevance 3 or 4."""
    root = root or REPO_ROOT
    rows = read_csv(
        experiments_root(root)
        / "EXP-05_slapa_content_mapping/responses/synthetic_responses.csv"
    )
    by_domain: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_domain[r["domain_id"]].append(int(r["relevance_1_to_4"]))
    i_cvi = {
        d: sum(1 for x in vals if x >= 3) / len(vals)
        for d, vals in by_domain.items()
    }
    return {
        "study_label": "synthetic_demonstration",
        "experiment_id": "EXP-05",
        "i_cvi_relevance": i_cvi,
        "s_cvi_ave": sum(i_cvi.values()) / len(i_cvi) if i_cvi else 0.0,
        "slapa_validated": False,
        "note": "Synthetic CVI demonstration only; not content validation evidence.",
    }


def analyze_synthetic_schools(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    rows = read_csv(
        experiments_root(root)
        / "EXP-06_synthetic_school_assessment/responses/synthetic_responses.csv"
    )
    for r in rows:
        if str(r.get("total_readiness_score", "")).strip():
            raise ValueError("total_readiness_score must remain empty")
    missing = sum(1 for r in rows if r.get("information_missing", "").strip())
    unjust = sum(1 for r in rows if r.get("unjustified_if_scored", "").strip())
    return {
        "study_label": "synthetic_demonstration",
        "experiment_id": "EXP-06",
        "n_domain_judgements": len(rows),
        "missing_information_frequency": missing / len(rows) if rows else 0.0,
        "unsupported_inference_prompt_frequency": unjust / len(rows) if rows else 0.0,
        "total_score_emitted": False,
        "slapa_validated": False,
    }


def run_all_synthetic_analyses(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    # coding with procedural pass must block reliability
    proc = experiments_root(root) / "EXP-02_coding_decisions/responses/synthetic_procedural_second_pass.csv"
    independent = [
        experiments_root(root) / "EXP-02_coding_decisions/responses/synthetic_coder_A.csv",
        experiments_root(root) / "EXP-02_coding_decisions/responses/synthetic_coder_B.csv",
    ]
    blocked = analyze_coding(root, [independent[0], proc])
    return {
        "EXP-01": analyze_unitization(root),
        "EXP-02_independent_demo": analyze_coding(root, independent),
        "EXP-02_procedural_block_demo": blocked,
        "EXP-03": analyze_usability(root),
        "EXP-04": analyze_layers(root),
        "EXP-05": analyze_cvi(root),
        "EXP-06": analyze_synthetic_schools(root),
        "claims": {
            "experiments_executed_with_humans": False,
            "slapa_validated": False,
            "empirical_alpha_from_procedural_pass": False,
        },
    }


def write_synthetic_report(root: Path | None = None) -> Path:
    root = root or REPO_ROOT
    out_dir = experiments_root(root) / "_generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = run_all_synthetic_analyses(root)
    path = out_dir / "synthetic_demonstration_report.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md = out_dir / "synthetic_demonstration_report.md"
    lines = [
        "# Synthetic demonstration report",
        "",
        "**Label:** synthetic_demonstration",
        "**Human participants executed:** no",
        "**SLAPA validated:** no",
        "",
        "```json",
        json.dumps(report, indent=2),
        "```",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    del argv
    report = validate_experiments()
    if not report.ok:
        print("Experiment pack validation FAILED:")
        for e in report.errors:
            print(f"  - {e}")
        return 1
    path = write_synthetic_report()
    print("Experiment pack validation OK.")
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
