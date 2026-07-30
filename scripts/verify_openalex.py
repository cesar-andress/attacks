#!/usr/bin/env python3
"""Query OpenAlex for literature identity checks.

Reads OPEN_ALEX_KEY from the environment only. Never prints or writes the key.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

OUT_CSV = ROOT / "data/corpus/openalex_literature_verifications.csv"

HEADERS = [
    "verification_id",
    "candidate_id",
    "document_id",
    "openalex_work_id",
    "doi",
    "title",
    "authors",
    "publication_year",
    "source_or_journal",
    "openalex_type",
    "retrieval_date",
    "verification_status",
    "relation_to_candidate",
    "peer_reviewed_indication",
    "prescriptive_or_assessment_bearing",
    "notes",
    "does_not_authorize_corpus_inclusion",
]

# Planned literature checks (not government guidance current-version checks)
PLANNED = [
    {
        "verification_id": "OA-CF02-001",
        "candidate_id": "CF-02",
        "document_id": "DOC-CF02-01",
        "work_id": "W2126945067",
        "relation_to_candidate": "candidate_primary_literature",
        "prescriptive_or_assessment_bearing": "possibly_prescriptive",
        "notes": (
            "Confirms peer-reviewed article identity for Kailes & Enders 2007. "
            "Does not by itself establish a later CMIST operational L1 document "
            "or authorize corpus freeze/inclusion."
        ),
    },
    {
        "verification_id": "OA-CF06-001",
        "candidate_id": "CF-06",
        "document_id": "DOC-CF06-01",
        "work_id": "W2078698107",
        "relation_to_candidate": "related_peer_reviewed_literature",
        "prescriptive_or_assessment_bearing": "likely_conceptual",
        "notes": (
            "Related peer-reviewed literature on Virginia Student Threat Assessment "
            "Guidelines (Cornell et al.). Does not establish the current operational "
            "CSTAG manual as L1, publisher identity, or institutional adoption."
        ),
    },
]


def _require_key() -> str:
    key = os.environ.get("OPEN_ALEX_KEY", "").strip()
    if not key:
        raise SystemExit(
            "OPEN_ALEX_KEY is not set in the environment. "
            "Load it via your shell config without printing the value."
        )
    return key


def oa_get(path: str, key: str, params: dict | None = None) -> dict:
    params = dict(params or {})
    params["api_key"] = key
    url = "https://api.openalex.org" + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "school-security-audit/0.2 (reproducible literature checks)"},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)


def work_to_row(plan: dict, work: dict, retrieval: str) -> dict:
    authors = " | ".join(
        a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])
    )
    source = ((work.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    doi = work.get("doi") or ""
    oa_type = work.get("type") or ""
    peer = "yes" if oa_type in {"article", "review"} else "unclear"
    return {
        "verification_id": plan["verification_id"],
        "candidate_id": plan["candidate_id"],
        "document_id": plan.get("document_id", ""),
        "openalex_work_id": work.get("id", ""),
        "doi": doi,
        "title": work.get("display_name", ""),
        "authors": authors,
        "publication_year": str(work.get("publication_year") or ""),
        "source_or_journal": source,
        "openalex_type": oa_type,
        "retrieval_date": retrieval,
        "verification_status": "confirmed_via_openalex"
        if plan["relation_to_candidate"] == "candidate_primary_literature"
        else "related_literature_only",
        "relation_to_candidate": plan["relation_to_candidate"],
        "peer_reviewed_indication": peer,
        "prescriptive_or_assessment_bearing": plan.get(
            "prescriptive_or_assessment_bearing", "unknown"
        ),
        "notes": plan.get("notes", ""),
        "does_not_authorize_corpus_inclusion": "true",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned work IDs only (no API calls, no key usage).",
    )
    args = parser.parse_args()

    if args.dry_run:
        for plan in PLANNED:
            print(
                f"{plan['verification_id']}: candidate={plan['candidate_id']} "
                f"work_id={plan['work_id']} relation={plan['relation_to_candidate']}"
            )
        return 0

    key = _require_key()
    retrieval = date.today().isoformat()
    rows: list[dict[str, str]] = []
    for plan in PLANNED:
        work = oa_get(f"/works/{plan['work_id']}", key)
        rows.append(work_to_row(plan, work, retrieval))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} OpenAlex verification row(s) to {OUT_CSV.relative_to(ROOT)}")
    print("API key was read from the environment and was not written to disk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
