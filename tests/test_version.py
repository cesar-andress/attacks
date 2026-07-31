"""Version consistency for stable releases."""

from pathlib import Path

import tomllib

from school_security_audit import __version__

ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_stable_release() -> None:
    assert __version__ == "1.0.0"


def test_pyproject_matches_package_version() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == __version__


def test_citation_cff_matches_package_version() -> None:
    text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "version: 1.0.0" in text
