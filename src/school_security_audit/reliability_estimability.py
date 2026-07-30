"""Classify reliability estimability states (no empirical α values invented)."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

STATES = {
    "ESTIMABLE_PASS",
    "ESTIMABLE_BELOW_THRESHOLD",
    "NOT_ESTIMABLE_NO_VARIATION",
    "NOT_ESTIMABLE_INSUFFICIENT_CATEGORIES",
    "NOT_ESTIMABLE_INSUFFICIENT_UNITS",
    "COMPUTATION_ERROR",
    "PROTOCOL_DEVIATION",
    "PENDING_ADJUDICATION",
}


def classify_estimability(
    coder_a: Iterable[str],
    coder_b: Iterable[str],
    *,
    alpha: float | None = None,
    pass_threshold: float = 0.80,
    caution_threshold: float = 0.67,
    min_units: int = 2,
    min_categories_joint: int = 2,
    pending_adjudication: bool = False,
    protocol_deviation: bool = False,
    computation_error: bool = False,
) -> dict:
    a = [str(x) for x in coder_a]
    b = [str(x) for x in coder_b]
    if pending_adjudication:
        return {"state": "PENDING_ADJUDICATION", "n": min(len(a), len(b)), "exact_agreement": None}
    if protocol_deviation:
        return {"state": "PROTOCOL_DEVIATION", "n": min(len(a), len(b)), "exact_agreement": None}
    if computation_error:
        return {"state": "COMPUTATION_ERROR", "n": min(len(a), len(b)), "exact_agreement": None}
    n = min(len(a), len(b))
    if n < min_units:
        return {"state": "NOT_ESTIMABLE_INSUFFICIENT_UNITS", "n": n, "exact_agreement": None}
    a, b = a[:n], b[:n]
    exact = sum(1 for x, y in zip(a, b) if x == y) / n
    joint_cats = set(a) | set(b)
    if len(set(a)) == 1 and len(set(b)) == 1 and a[0] == b[0]:
        return {
            "state": "NOT_ESTIMABLE_NO_VARIATION",
            "n": n,
            "exact_agreement": exact,
            "marginals": dict(Counter(a)),
        }
    if len(joint_cats) < min_categories_joint:
        return {
            "state": "NOT_ESTIMABLE_INSUFFICIENT_CATEGORIES",
            "n": n,
            "exact_agreement": exact,
            "marginals": {"a": dict(Counter(a)), "b": dict(Counter(b))},
        }
    if alpha is None:
        return {
            "state": "COMPUTATION_ERROR",
            "n": n,
            "exact_agreement": exact,
            "note": "alpha_required_when_categories_vary",
        }
    if alpha >= pass_threshold:
        state = "ESTIMABLE_PASS"
    else:
        state = "ESTIMABLE_BELOW_THRESHOLD"
    return {"state": state, "n": n, "exact_agreement": exact, "alpha": alpha}


def collapsed_engagement(rung: str, *, scheme: str = "any") -> str:
    """Pre-specified secondary collapse helpers (do not replace primary ladder).

    Schemes:
      - any: rung 0 vs ≥1
      - support: rung ≤1 (none/prescription) vs ≥2 (support or higher)
    """
    try:
        r = int(rung)
    except ValueError as exc:
        raise ValueError(f"non-integer rung: {rung}") from exc
    if scheme == "any":
        return "no_engagement" if r <= 0 else "any_engagement"
    if scheme == "support":
        return "prescription_or_below" if r <= 1 else "support_or_higher"
    raise ValueError(f"unknown collapse scheme: {scheme}")


# Action guidance for reporting (not automatic pipeline gates)
STATE_ACTIONS = {
    "ESTIMABLE_PASS": {"review": False, "retrain": False, "recode": False, "demote": False, "failure": False},
    "ESTIMABLE_BELOW_THRESHOLD": {"review": True, "retrain": True, "recode": False, "demote": True, "failure": False},
    "NOT_ESTIMABLE_NO_VARIATION": {"review": False, "retrain": False, "recode": False, "demote": False, "failure": False},
    "NOT_ESTIMABLE_INSUFFICIENT_CATEGORIES": {"review": True, "retrain": False, "recode": False, "demote": False, "failure": False},
    "NOT_ESTIMABLE_INSUFFICIENT_UNITS": {"review": True, "retrain": False, "recode": False, "demote": False, "failure": False},
    "COMPUTATION_ERROR": {"review": True, "retrain": False, "recode": False, "demote": False, "failure": False},
    "PROTOCOL_DEVIATION": {"review": True, "retrain": False, "recode": True, "demote": True, "failure": True},
    "PENDING_ADJUDICATION": {"review": False, "retrain": False, "recode": False, "demote": False, "failure": False},
}
