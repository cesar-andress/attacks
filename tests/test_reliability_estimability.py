"""Tests for reliability estimability classification (no empirical study α)."""

from school_security_audit.reliability_estimability import (
    classify_estimability,
    collapsed_engagement,
)


def test_no_variation() -> None:
    r = classify_estimability(["1"] * 10, ["1"] * 10, alpha=1.0)
    assert r["state"] == "NOT_ESTIMABLE_NO_VARIATION"
    assert r["exact_agreement"] == 1.0


def test_insufficient_units() -> None:
    r = classify_estimability(["1"], ["1"], alpha=1.0)
    assert r["state"] == "NOT_ESTIMABLE_INSUFFICIENT_UNITS"


def test_estimable_pass() -> None:
    a = ["0", "1", "2", "1", "0", "2"]
    b = ["0", "1", "2", "1", "0", "1"]
    r = classify_estimability(a, b, alpha=0.85)
    assert r["state"] == "ESTIMABLE_PASS"
    assert 0.0 <= r["exact_agreement"] <= 1.0


def test_estimable_below() -> None:
    a = ["0", "1", "2", "3"]
    b = ["0", "2", "1", "3"]
    r = classify_estimability(a, b, alpha=0.50)
    assert r["state"] == "ESTIMABLE_BELOW_THRESHOLD"


def test_perfect_agreement_low_prevalence_still_no_variation_if_single_cat() -> None:
    r = classify_estimability(["0"] * 20, ["0"] * 20, alpha=None)
    assert r["state"] == "NOT_ESTIMABLE_NO_VARIATION"


def test_collapsed_bands() -> None:
    assert collapsed_engagement("0") == "no_engagement"
    assert collapsed_engagement("3") == "any_engagement"
    assert collapsed_engagement("1", scheme="support") == "prescription_or_below"
    assert collapsed_engagement("2", scheme="support") == "support_or_higher"


def test_insufficient_categories_disagreement() -> None:
    # Two categories in joint set but one coder invariant? joint has 2 → estimable path
    r = classify_estimability(["0", "0", "1"], ["1", "1", "0"], alpha=0.2)
    assert r["state"] == "ESTIMABLE_BELOW_THRESHOLD"


def test_alpha_missing_when_variable() -> None:
    r = classify_estimability(["0", "1", "2"], ["0", "1", "1"], alpha=None)
    assert r["state"] == "COMPUTATION_ERROR"


def test_pending_and_errors() -> None:
    assert classify_estimability(["0", "1"], ["0", "1"], pending_adjudication=True)[
        "state"
    ] == "PENDING_ADJUDICATION"
    assert classify_estimability(["0", "1"], ["0", "1"], protocol_deviation=True)[
        "state"
    ] == "PROTOCOL_DEVIATION"
    assert classify_estimability(["0", "1"], ["0", "1"], computation_error=True)[
        "state"
    ] == "COMPUTATION_ERROR"


def test_states_are_distinct() -> None:
    from school_security_audit.reliability_estimability import STATES, STATE_ACTIONS

    assert STATES == set(STATE_ACTIONS)
    assert "FAIL" not in STATES
