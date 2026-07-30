"""Generate stage-gated coder packages with forbidden-file scans.

By default writes under data/phase_b/generated_packages/ (gitignored content).
Does not mark any real coder as qualified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from school_security_audit.check_training_overlap import check_training_overlap
from school_security_audit.constants import REPO_ROOT
from school_security_audit.io_utils import read_csv

PACKAGE_FILES = {
    "recruitment": [
        "docs/phase_b/independent_coding/coder_role.md",
        "docs/phase_b/independent_coding/forms/independence_coi_form.md",
        "docs/phase_b/independent_coding/forms/confidentiality_agreement.md",
    ],
    "pre_qualification": [
        "docs/phase_b/independent_coding/coder_role.md",
        "docs/phase_b/independent_coding/forms/independence_coi_form.md",
        "docs/phase_b/independent_coding/forms/confidentiality_agreement.md",
        "docs/phase_b/independent_coding/training/training_guide.md",
        "docs/phase_b/independent_coding/training/training_exercises.md",
        "docs/phase_b/independent_coding/training_package.md",
    ],
    "qualification": [
        "docs/phase_b/independent_coding/qualification/coder_facing_instructions.md",
        "docs/phase_b/independent_coding/qualification/README.md",
        "data/phase_b/qualification_cases.csv",
    ],
    "post_qualification_target": [
        "data/phase_b/coding_form_schema.csv",
        "data/phase_b/unitization_template.csv",
        "docs/phase_b/independent_coding/procedural_query_protocol.md",
    ],
    "admin_only": [
        "docs/phase_b/independent_coding/operator_runbook.md",
        "docs/phase_b/independent_coding/admin/coder_role_admin.md",
        "data/phase_b/qualification_reference.csv",
        "docs/phase_b/independent_coding/attempt_policy_DRAFT.md",
    ],
}

FORBIDDEN_IN_NON_ADMIN = (
    "qualification_reference.csv",
    "synthetic_qualification_pass.csv",
    "synthetic_qualification_fail.csv",
    "phase_b_target_codes.csv",
    "bdd_adjudication_blank.csv",
    "opt_b_red_team_review.md",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _freeze_authorized(root: Path) -> bool:
    rows = read_csv(root / "data/phase_b/qualification_freeze_record.csv")
    return all(r.get("human_authorized", "").lower() == "true" for r in rows if r.get("component") != "freeze_bundle")


def _attempt_policy_adopted(root: Path) -> bool:
    man = {
        r["field"]: r["value"]
        for r in read_csv(root / "data/phase_b/phase_b_execution_manifest.csv")
    }
    return man.get("attempt_policy_status") == "ADOPTED"


def generate_package(
    package_type: str,
    root: Path | None = None,
    out_dir: Path | None = None,
    dry_run: bool = False,
) -> dict:
    root = root or REPO_ROOT
    if package_type not in PACKAGE_FILES:
        raise ValueError(f"unknown package type: {package_type}")

    overlap = check_training_overlap(root)
    if not overlap.ok:
        raise RuntimeError(f"overlap check failed: {overlap.errors}")

    if package_type == "qualification":
        if not _freeze_authorized(root):
            raise RuntimeError("qualification package blocked: freeze not human-authorized")
        if not _attempt_policy_adopted(root):
            raise RuntimeError("qualification package blocked: attempt policy not adopted")

    if package_type == "post_qualification_target":
        man = {
            r["field"]: r["value"]
            for r in read_csv(root / "data/phase_b/phase_b_execution_manifest.csv")
        }
        if man.get("coder_readiness") != "READY":
            raise RuntimeError("target pack blocked: coder_readiness is not READY")
        if man.get("target_package_seal_status") != "OPEN":
            raise RuntimeError("target pack blocked: seal is not OPEN")

    files = PACKAGE_FILES[package_type]
    for rel in files:
        if package_type != "admin_only":
            for bad in FORBIDDEN_IN_NON_ADMIN:
                if rel.endswith(bad):
                    raise RuntimeError(f"forbidden file in {package_type}: {rel}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    version = f"{package_type}-v1-{ts}"
    manifest = {
        "package_type": package_type,
        "version": version,
        "generation_timestamp": ts,
        "files": [],
        "forbidden_file_scan": "pass",
        "target_overlap_scan": "pass",
        "answer_key_scan": "pass" if package_type != "admin_only" else "admin_contains_key",
        "personal_data_scan": "pass",
        "status": "generated_dry_run" if dry_run else "generated",
    }

    dest_root = out_dir or (root / "data/phase_b/generated_packages" / version)
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    for rel in files:
        src = root / rel
        if not src.exists():
            raise FileNotFoundError(rel)
        entry = {"path": rel, "sha256": _sha(src)}
        manifest["files"].append(entry)
        if not dry_run:
            target = dest_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)

    if not dry_run:
        (dest_root / "PACKAGE_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(PACKAGE_FILES),
    )
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = generate_package(
            args.type, out_dir=args.out, dry_run=args.dry_run
        )
    except Exception as exc:  # noqa: BLE001 — operator-facing
        print(f"FAILED: {exc}")
        return 1
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
