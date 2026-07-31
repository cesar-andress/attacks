"""Synthetic reliability-pipeline readiness (NOT_FOR_MANUSCRIPT)."""

from __future__ import annotations

from pathlib import Path

import pytest

from school_security_audit.constants import REPO_ROOT
from school_security_audit.reliability_pipeline import (
    SYNTHETIC_BANNER,
    krippendorff_alpha,
    run_reliability_pipeline,
    write_outputs,
)

FIX = REPO_ROOT / "data/operations/fixtures/reliability"


def _write_pair(dir_path: Path, a_rows: list[tuple[str, str]], b_rows: list[tuple[str, str]]) -> tuple[Path, Path]:
    dir_path.mkdir(parents=True, exist_ok=True)
    a = dir_path / "coder_a.csv"
    b = dir_path / "coder_b.csv"
    a.write_text(
        "unit_id,coder_id,value\n" + "\n".join(f"{u},CODER_A,{v}" for u, v in a_rows) + "\n",
        encoding="utf-8",
    )
    b.write_text(
        "unit_id,coder_id,value\n" + "\n".join(f"{u},CODER_B,{v}" for u, v in b_rows) + "\n",
        encoding="utf-8",
    )
    return a, b


def test_perfect_agreement(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "perfect",
        [("U1", "0"), ("U2", "1"), ("U3", "2")],
        [("U1", "0"), ("U2", "1"), ("U3", "2")],
    )
    r = run_reliability_pipeline(a, b, level="ordinal", value_order=["0", "1", "2", "3", "4", "5"])
    assert r.ok
    assert r.payload["banner"] == SYNTHETIC_BANNER
    assert r.payload["exact_agreement"] == 1.0
    assert r.payload["alpha"] == pytest.approx(1.0)
    assert r.payload["estimability"]["state"] == "ESTIMABLE_PASS"
    write_outputs(r, tmp_path / "out")
    assert "SYNTHETIC" in (tmp_path / "out/reliability.md").read_text(encoding="utf-8")


def test_partial_disagreement(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "partial",
        [("U1", "0"), ("U2", "1"), ("U3", "2"), ("U4", "1")],
        [("U1", "0"), ("U2", "2"), ("U3", "2"), ("U4", "1")],
    )
    r = run_reliability_pipeline(a, b, level="nominal")
    assert r.ok
    assert 0.0 < r.payload["exact_agreement"] < 1.0
    assert r.payload["alpha"] is not None
    assert r.payload["estimability"]["state"] in {"ESTIMABLE_PASS", "ESTIMABLE_BELOW_THRESHOLD"}


def test_ordinal_disagreement(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "ord",
        [("U1", "0"), ("U2", "1"), ("U3", "4"), ("U4", "2")],
        [("U1", "0"), ("U2", "2"), ("U3", "5"), ("U4", "2")],
    )
    r = run_reliability_pipeline(a, b, level="ordinal", value_order=["0", "1", "2", "3", "4", "5"])
    assert r.ok
    assert r.payload["alpha_level"] == "ordinal"


def test_missing_values(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "miss",
        [("U1", "0"), ("U2", "NA"), ("U3", "1"), ("U4", "2")],
        [("U1", "0"), ("U2", "1"), ("U3", "NA"), ("U4", "2")],
    )
    r = run_reliability_pipeline(a, b)
    assert r.ok
    assert r.payload["missingness"]["coder_a"] == 1
    assert r.payload["missingness"]["coder_b"] == 1
    assert r.payload["n_complete_pairs"] == 2


def test_invariant_both_agree(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "inv",
        [("U1", "0"), ("U2", "0"), ("U3", "0")],
        [("U1", "0"), ("U2", "0"), ("U3", "0")],
    )
    r = run_reliability_pipeline(a, b)
    assert r.ok
    assert r.payload["exact_agreement"] == 1.0
    assert r.payload["estimability"]["state"] == "NOT_ESTIMABLE_NO_VARIATION"


def test_one_invariant_coder(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "oneinv",
        [("U1", "0"), ("U2", "0"), ("U3", "0"), ("U4", "0")],
        [("U1", "0"), ("U2", "1"), ("U3", "0"), ("U4", "2")],
    )
    r = run_reliability_pipeline(a, b)
    assert r.ok
    assert r.payload["alpha"] is not None
    assert r.payload["estimability"]["state"] in {
        "ESTIMABLE_PASS",
        "ESTIMABLE_BELOW_THRESHOLD",
    }


def test_insufficient_units(tmp_path: Path) -> None:
    a, b = _write_pair(tmp_path / "n1", [("U1", "0")], [("U1", "1")])
    r = run_reliability_pipeline(a, b)
    assert r.ok
    assert r.payload["estimability"]["state"] == "NOT_ESTIMABLE_INSUFFICIENT_UNITS"


def test_malformed_values(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "bad",
        [("U1", "0"), ("U2", "9")],
        [("U1", "0"), ("U2", "1")],
    )
    r = run_reliability_pipeline(a, b, allowed_values={"0", "1", "2", "3", "4", "5"})
    assert not r.ok
    assert r.payload["operational_error"] is True
    assert any(i.code == "MALFORMED_VALUE" for i in r.issues)


def test_duplicate_unit_ids(tmp_path: Path) -> None:
    d = tmp_path / "dup"
    d.mkdir()
    a = d / "coder_a.csv"
    b = d / "coder_b.csv"
    a.write_text("unit_id,coder_id,value\nU1,CODER_A,0\nU1,CODER_A,1\n", encoding="utf-8")
    b.write_text("unit_id,coder_id,value\nU1,CODER_B,0\nU2,CODER_B,1\n", encoding="utf-8")
    r = run_reliability_pipeline(a, b)
    assert not r.ok
    assert any(i.code == "DUPLICATE_UNIT_ID" for i in r.issues)


def test_mismatched_unit_sets(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "mm",
        [("U1", "0"), ("U2", "1")],
        [("U1", "0"), ("U3", "1")],
    )
    r = run_reliability_pipeline(a, b)
    assert not r.ok
    assert any(i.code == "MISMATCHED_UNIT_SETS" for i in r.issues)


def test_missing_coder_file(tmp_path: Path) -> None:
    a = tmp_path / "missing_a.csv"
    b = tmp_path / "coder_b.csv"
    b.write_text("unit_id,coder_id,value\nU1,CODER_B,0\n", encoding="utf-8")
    r = run_reliability_pipeline(a, b)
    assert not r.ok
    assert any(i.code == "MISSING_CODER_FILE" for i in r.issues)


def test_invalid_coder_identity(tmp_path: Path) -> None:
    d = tmp_path / "id"
    d.mkdir()
    a = d / "coder_a.csv"
    b = d / "coder_b.csv"
    a.write_text("unit_id,coder_id,value\nU1,WRONG,0\nU2,WRONG,1\n", encoding="utf-8")
    b.write_text("unit_id,coder_id,value\nU1,CODER_B,0\nU2,CODER_B,1\n", encoding="utf-8")
    r = run_reliability_pipeline(a, b)
    assert not r.ok
    assert any(i.code == "INVALID_CODER_IDENTITY" for i in r.issues)


def test_protocol_deviation(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "pd",
        [("U1", "0"), ("U2", "1")],
        [("U1", "0"), ("U2", "1")],
    )
    r = run_reliability_pipeline(a, b, protocol_deviation=True)
    assert r.payload["estimability"]["state"] == "PROTOCOL_DEVIATION"
    assert r.payload["protocol_failure"] is True


def test_computation_failure_flag(tmp_path: Path) -> None:
    a, b = _write_pair(
        tmp_path / "cf",
        [("U1", "0"), ("U2", "1")],
        [("U1", "0"), ("U2", "1")],
    )
    r = run_reliability_pipeline(a, b, force_computation_error=True)
    assert r.payload["estimability"]["state"] == "COMPUTATION_ERROR"


def test_alpha_perfect_known() -> None:
    assert krippendorff_alpha(["0", "1", "2"], ["0", "1", "2"]) == pytest.approx(1.0)


def test_repo_fixture_readme_marks_synthetic() -> None:
    readme = FIX / "README.md"
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "SYNTHETIC_NOT_FOR_MANUSCRIPT" in text
