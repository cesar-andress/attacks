# OpenAlex literature verification policy

**Purpose.** OpenAlex may be used to verify **literature identity and citation provenance** for peer-reviewed or indexed works related to the candidate frame.

## Allowed uses

- Confirm publication identity (title, authors, year, journal/source).
- Resolve DOIs and OpenAlex work IDs.
- Check whether a candidate is indexed as a peer-reviewed article/book chapter.
- Locate related editions or cited scholarly works.
- Backward/forward citation exploration (scholarly graph).
- Help distinguish conceptual articles from documents that *may* contain prescriptive/assessment content (still requires full-text screening).

## Not authoritative for

- Current version of government guidance.
- Current official URLs.
- Whether a government document has been superseded.
- Legal or regulatory status.
- Institutional adoption.
- Copyright or redistribution permissions.

For those matters, prefer the **official issuing-body source**.

When OpenAlex and an official source disagree, **preserve the discrepancy** and treat the official source as authoritative for institutional documents.

## Corpus rule

Do **not** add a publication to the candidate corpus merely because OpenAlex indexes it.  
It must still satisfy the fixed authority, scope, and prescriptive-content criteria after screening.

## Required retained fields

Every OpenAlex-derived literature record in `data/corpus/openalex_literature_verifications.csv` must retain:

- OpenAlex work ID
- DOI (if available)
- title
- authors
- publication year
- source or journal
- retrieval date
- verification status

## API key handling

- Load `OPEN_ALEX_KEY` from the environment (e.g. via `source ~/.bashrc`).
- Never echo, log, commit, or write the key into repository files, fixtures, or reports.
- The verification script reads the key only from the process environment.

## Script

```bash
source ~/.bashrc
cd ~/papers/attacks/attacks
.venv/bin/python scripts/verify_openalex.py --dry-run   # shows planned queries only
.venv/bin/python scripts/verify_openalex.py             # writes/updates CSV rows
```
