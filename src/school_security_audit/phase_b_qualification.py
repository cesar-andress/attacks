"""Score Phase-B coder qualification responses against reference adjudication.

Scorer version is frozen with qualification materials. Do not change thresholds
after a real coder attempt has been authorized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv

SCORER_VERSION = "QUAL-SCORER-v1"
QUAL_SET_VERSION = "QUAL-SET-v1"
ANSWER_KEY_VERSION = "QUAL-KEY-v1"

CRITICAL_CASES = {
    "Q-09": "ambiguous_memo_as_evidence",
    "Q-11": "auto_support_from_setting",
    "Q-12": "branch_b_coded",
    "Q-13": "missing_source_location",
}

RUNG_THRESHOLD = 0.8
UNIT_THRESHOLD = 0.8


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ref_map(root: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(root / "data/phase_b/qualification_reference.csv")
    return {r["case_id"]: r for r in rows}


def score_responses(
    responses: list[dict[str, str]],
    root: Path | None = None,
    *,
    coder_id: str = "",
    attempt_number: str = "",
    submission_timestamp: str = "",
) -> dict:
    root = root or REPO_ROOT
    ref_path = root / "data/phase_b/qualification_reference.csv"
    cases_path = root / "data/phase_b/qualification_cases.csv"
    ref = _ref_map(root)
    critical_fails: list[str] = []
    warnings: list[str] = []
    rung_cases = {"Q-02", "Q-03", "Q-04", "Q-05"}
    rung_ok = 0
    rung_n = 0
    unit_ok = 0
    unit_n = 0
    locus_ok = 0
    locus_n = 0

    by_id = {r.get("case_id", ""): r for r in responses}
    if len(by_id) != len(responses):
        critical_fails.append("duplicate_case_id_in_submission")

    for cid, rref in ref.items():
        resp = by_id.get(cid)
        if not resp:
            critical_fails.append(f"{cid}:missing_response")
            continue

        if cid == "Q-09":
            if resp.get("support_present", "").strip() == "1" or resp.get(
                "demand_source_primary", ""
            ).strip() == "explicit":
                if resp.get("is_pe", "").strip().lower() == "true":
                    critical_fails.append(CRITICAL_CASES[cid])
        if cid == "Q-11":
            if resp.get("support_present", "").strip() == "1":
                critical_fails.append(CRITICAL_CASES[cid])
        if cid == "Q-12":
            if resp.get("branch_b_coded", "").strip().lower() in {"true", "1", "yes"}:
                critical_fails.append(CRITICAL_CASES[cid])
        if cid == "Q-13":
            if not (resp.get("source_location") or "").strip():
                critical_fails.append(CRITICAL_CASES[cid])

        if cid in rung_cases:
            rung_n += 1
            if resp.get("executability_rung", "").strip() == rref.get(
                "executability_rung", ""
            ).strip():
                rung_ok += 1

        if cid == "Q-01":
            unit_n += 1
            try:
                if int(resp.get("pe_count", "0")) == int(rref.get("pe_count_expected", "0")):
                    unit_ok += 1
            except ValueError:
                warnings.append("Q-01:non_integer_pe_count")

        if cid == "Q-06":
            locus_n += 1
            if resp.get("executability_locus", "").strip() == rref.get(
                "executability_locus", ""
            ).strip():
                locus_ok += 1

    rung_rate = (rung_ok / rung_n) if rung_n else 0.0
    unit_rate = (unit_ok / unit_n) if unit_n else 0.0
    locus_rate = (locus_ok / locus_n) if locus_n else None
    passed = (
        not critical_fails
        and rung_rate >= RUNG_THRESHOLD
        and unit_rate >= UNIT_THRESHOLD
    )

    # Coder-facing result must not embed answer key rows
    return {
        "coder_pseudonymous_id": coder_id or None,
        "attempt_number": attempt_number or None,
        "scorer_version": SCORER_VERSION,
        "qualification_set_version": QUAL_SET_VERSION,
        "answer_key_version": ANSWER_KEY_VERSION,
        "submission_timestamp": submission_timestamp or None,
        "qualification_cases_sha256": _sha256(cases_path) if cases_path.exists() else None,
        "answer_key_sha256": _sha256(ref_path) if ref_path.exists() else None,
        "overall_result": "PASS" if passed else "FAIL",
        "passed": passed,
        "dimension_results": {
            "critical_fails": critical_fails,
            "rung_rate": rung_rate,
            "unitization_rate": unit_rate,
            "locus_rate": locus_rate,
            "thresholds": {
                "rung": RUNG_THRESHOLD,
                "unitization": UNIT_THRESHOLD,
            },
        },
        "failure_reasons": critical_fails
        + (
            []
            if rung_rate >= RUNG_THRESHOLD
            else [f"rung_rate_below_threshold:{rung_rate:.2f}"]
        )
        + (
            []
            if unit_rate >= UNIT_THRESHOLD
            else [f"unitization_rate_below_threshold:{unit_rate:.2f}"]
        ),
        "warnings": warnings,
        "answer_key_exposed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses_csv", type=Path)
    parser.add_argument("--coder-id", default="")
    parser.add_argument("--attempt", default="")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = read_csv(args.responses_csv)
    result = score_responses(
        rows,
        coder_id=args.coder_id,
        attempt_number=args.attempt,
        submission_timestamp=args.timestamp,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
