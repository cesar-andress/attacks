"""End-to-end reliability pipeline for dual-coder documentary coding.

Uses synthetic fixtures for readiness tests. Never invents empirical study α.
Outputs always include exact agreement, alpha (when computable), marginals,
missingness, n, and PA-003 estimability state.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from school_security_audit.reliability_estimability import classify_estimability

SYNTHETIC_BANNER = "SYNTHETIC_NOT_FOR_MANUSCRIPT"
MISSING_TOKENS = {"", "NA", "N/A", "NULL", "MISSING", "."}


@dataclass
class PipelineIssue:
    code: str
    detail: str


@dataclass
class ReliabilityResult:
    ok: bool
    issues: list[PipelineIssue] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)


def _is_missing(v: str | None) -> bool:
    return v is None or str(v).strip().upper() in MISSING_TOKENS


def krippendorff_alpha(
    coder_a: list[str | None],
    coder_b: list[str | None],
    *,
    level: str = "nominal",
    value_order: list[str] | None = None,
) -> float | None:
    """Two-coder Krippendorff's α (nominal or ordinal). Returns None if undefined."""
    pairs: list[tuple[str, str]] = []
    for x, y in zip(coder_a, coder_b):
        if _is_missing(x) or _is_missing(y):
            continue
        pairs.append((str(x), str(y)))
    n_units = len(pairs)
    if n_units < 2:
        return None
    values = sorted({v for pair in pairs for v in pair})
    if len(values) < 2:
        return None

    if level == "ordinal":
        order = value_order or values
        rank = {v: i for i, v in enumerate(order)}
        if any(v not in rank for v in values):
            rank = {v: i for i, v in enumerate(values)}

        def delta(c: str, k: str) -> float:
            return float(rank[c] - rank[k]) ** 2

    elif level == "nominal":

        def delta(c: str, k: str) -> float:
            return 0.0 if c == k else 1.0

    else:
        raise ValueError(f"unsupported level: {level}")

    o: Counter[tuple[str, str]] = Counter()
    for c, k in pairs:
        if c == k:
            o[(c, c)] += 1.0
        else:
            o[(c, k)] += 1.0
            o[(k, c)] += 1.0

    n_c = {v: sum(o[(v, k)] for k in values) for v in values}
    n_star = sum(n_c.values())
    if n_star <= 1:
        return None

    observed = sum(o[(c, k)] * delta(c, k) for c in values for k in values) / n_star
    expected = (
        sum(n_c[c] * n_c[k] * delta(c, k) for c in values for k in values) / (n_star * (n_star - 1.0))
    )
    if expected == 0.0:
        return 1.0 if observed == 0.0 else None
    return 1.0 - (observed / expected)


def load_coder_file(
    path: Path,
    *,
    unit_col: str = "unit_id",
    value_col: str = "value",
    coder_id_col: str = "coder_id",
    expected_coder: str | None = None,
) -> tuple[dict[str, str | None], list[PipelineIssue]]:
    issues: list[PipelineIssue] = []
    if not path.exists():
        return {}, [PipelineIssue("MISSING_CODER_FILE", str(path))]
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return {}, [PipelineIssue("EMPTY_CODER_FILE", str(path))]
    seen: set[str] = set()
    out: dict[str, str | None] = {}
    for i, row in enumerate(rows, start=2):
        uid = (row.get(unit_col) or "").strip()
        if not uid:
            issues.append(PipelineIssue("MISSING_UNIT_ID", f"{path.name}:line {i}"))
            continue
        if uid in seen:
            issues.append(PipelineIssue("DUPLICATE_UNIT_ID", uid))
            continue
        seen.add(uid)
        if expected_coder is not None:
            cid = (row.get(coder_id_col) or "").strip()
            if cid and cid != expected_coder:
                issues.append(PipelineIssue("INVALID_CODER_IDENTITY", f"{cid}!={expected_coder}"))
        raw = row.get(value_col)
        out[uid] = None if _is_missing(raw) else str(raw).strip()
    return out, issues


def run_reliability_pipeline(
    coder_a_path: Path,
    coder_b_path: Path,
    *,
    coder_a_id: str = "CODER_A",
    coder_b_id: str = "CODER_B",
    level: str = "nominal",
    value_order: list[str] | None = None,
    allowed_values: set[str] | None = None,
    synthetic: bool = True,
    protocol_deviation: bool = False,
    pending_adjudication: bool = False,
    force_computation_error: bool = False,
) -> ReliabilityResult:
    issues: list[PipelineIssue] = []
    a_map, a_issues = load_coder_file(coder_a_path, expected_coder=coder_a_id)
    b_map, b_issues = load_coder_file(coder_b_path, expected_coder=coder_b_id)
    issues.extend(a_issues)
    issues.extend(b_issues)

    blocking = {
        "MISSING_CODER_FILE",
        "EMPTY_CODER_FILE",
        "DUPLICATE_UNIT_ID",
        "INVALID_CODER_IDENTITY",
    }
    banner = SYNTHETIC_BANNER if synthetic else "EMPIRICAL_PENDING_HUMAN_REVIEW"

    def err_payload() -> dict[str, Any]:
        return {
            "banner": banner,
            "operational_error": True,
            "issues": [i.__dict__ for i in issues],
            "exact_agreement": None,
            "alpha": None,
            "marginals": None,
            "estimability": {"state": "COMPUTATION_ERROR"},
        }

    if any(i.code in blocking for i in issues):
        return ReliabilityResult(ok=False, issues=issues, payload=err_payload())

    a_ids, b_ids = set(a_map), set(b_map)
    if a_ids != b_ids:
        issues.append(
            PipelineIssue(
                "MISMATCHED_UNIT_SETS",
                f"only_a={sorted(a_ids - b_ids)}; only_b={sorted(b_ids - a_ids)}",
            )
        )
        return ReliabilityResult(ok=False, issues=issues, payload=err_payload())

    units = sorted(a_ids)
    a_vals = [a_map[u] for u in units]
    b_vals = [b_map[u] for u in units]

    if allowed_values is not None:
        for u, v in zip(units, a_vals):
            if v is not None and v not in allowed_values:
                issues.append(PipelineIssue("MALFORMED_VALUE", f"{coder_a_id}:{u}={v}"))
        for u, v in zip(units, b_vals):
            if v is not None and v not in allowed_values:
                issues.append(PipelineIssue("MALFORMED_VALUE", f"{coder_b_id}:{u}={v}"))
        if any(i.code == "MALFORMED_VALUE" for i in issues):
            return ReliabilityResult(ok=False, issues=issues, payload=err_payload())

    missing_a = sum(1 for v in a_vals if v is None)
    missing_b = sum(1 for v in b_vals if v is None)
    complete_idx = [i for i, (x, y) in enumerate(zip(a_vals, b_vals)) if x is not None and y is not None]
    a_comp = [a_vals[i] for i in complete_idx]  # type: ignore[misc]
    b_comp = [b_vals[i] for i in complete_idx]  # type: ignore[misc]
    n_complete = len(a_comp)
    exact = (
        sum(1 for x, y in zip(a_comp, b_comp) if x == y) / n_complete if n_complete else None
    )

    alpha: float | None = None
    computation_error = force_computation_error
    if not computation_error and n_complete >= 2:
        try:
            alpha = krippendorff_alpha(a_comp, b_comp, level=level, value_order=value_order)
        except Exception as exc:  # noqa: BLE001
            issues.append(PipelineIssue("COMPUTATION_FAILURE", str(exc)))
            computation_error = True

    if pending_adjudication or protocol_deviation or computation_error:
        estim = classify_estimability(
            a_comp or ["0"],
            b_comp or ["0"],
            alpha=alpha,
            pending_adjudication=pending_adjudication,
            protocol_deviation=protocol_deviation,
            computation_error=computation_error,
        )
    elif n_complete < 2:
        estim = classify_estimability(["0"], ["1"], alpha=None)  # forces insufficient units path via n=1
        estim = {
            "state": "NOT_ESTIMABLE_INSUFFICIENT_UNITS",
            "n": n_complete,
            "exact_agreement": exact,
        }
    else:
        # When alpha is None solely due to invariance, classifier handles NO_VARIATION
        if alpha is None and len(set(a_comp) | set(b_comp)) >= 2:
            estim = classify_estimability(a_comp, b_comp, alpha=None, computation_error=True)
        else:
            estim = classify_estimability(a_comp, b_comp, alpha=alpha if alpha is not None else 1.0)

    marginals = {
        "coder_a": dict(Counter(a_comp)),
        "coder_b": dict(Counter(b_comp)),
        "joint_units": n_complete,
    }

    payload = {
        "banner": banner,
        "n_units": len(units),
        "n_complete_pairs": n_complete,
        "missingness": {"coder_a": missing_a, "coder_b": missing_b},
        "exact_agreement": exact,
        "alpha": alpha,
        "alpha_level": level,
        "marginals": marginals,
        "estimability": estim,
        "issues": [i.__dict__ for i in issues],
        "operational_error": False,
        "protocol_failure": protocol_deviation or estim.get("state") == "PROTOCOL_DEVIATION",
    }
    return ReliabilityResult(ok=True, issues=issues, payload=payload)


def write_outputs(result: ReliabilityResult, out_dir: Path, stem: str = "reliability") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(result.payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    p = result.payload
    lines = [
        "# Reliability report",
        "",
        f"**Banner:** {p.get('banner')}",
        f"**Exact agreement:** {p.get('exact_agreement')}",
        f"**Alpha ({p.get('alpha_level')}):** {p.get('alpha')}",
        f"**n complete pairs:** {p.get('n_complete_pairs')}",
        f"**Missingness:** {p.get('missingness')}",
        f"**Marginals:** {p.get('marginals')}",
        f"**Estimability:** {p.get('estimability')}",
        f"**Operational error:** {p.get('operational_error')}",
        f"**Protocol failure:** {p.get('protocol_failure')}",
        "",
    ]
    if p.get("banner") == SYNTHETIC_BANNER:
        lines[2:2] = ["> SYNTHETIC fixture output — excluded from manuscript Results.", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    del argv
    print("Use tests/test_reliability_pipeline.py for synthetic readiness checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
