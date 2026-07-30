"""Score Phase-B coder qualification responses against reference adjudication."""

from __future__ import annotations

import argparse
from pathlib import Path

from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv


CRITICAL_CASES = {
    "Q-09": "ambiguous_memo_as_evidence",
    "Q-11": "auto_support_from_setting",
    "Q-12": "branch_b_coded",
    "Q-13": "missing_source_location",
}


def _ref_map(root: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(root / "data/phase_b/qualification_reference.csv")
    return {r["case_id"]: r for r in rows}


def score_responses(responses: list[dict[str, str]], root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    ref = _ref_map(root)
    critical_fails: list[str] = []
    rung_cases = {"Q-02", "Q-03", "Q-04", "Q-05"}
    rung_ok = 0
    rung_n = 0
    unit_ok = 0
    unit_n = 0

    by_id = {r["case_id"]: r for r in responses}
    for cid, rref in ref.items():
        resp = by_id.get(cid)
        if not resp:
            critical_fails.append(f"{cid}:missing_response")
            continue

        # Critical checks
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
                pass

    rung_rate = (rung_ok / rung_n) if rung_n else 0.0
    unit_rate = (unit_ok / unit_n) if unit_n else 0.0
    passed = not critical_fails and rung_rate >= 0.8 and unit_rate >= 0.8
    return {
        "passed": passed,
        "critical_fails": critical_fails,
        "rung_rate": rung_rate,
        "unitization_rate": unit_rate,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses_csv", type=Path)
    args = parser.parse_args(argv)
    rows = read_csv(args.responses_csv)
    result = score_responses(rows)
    print(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
