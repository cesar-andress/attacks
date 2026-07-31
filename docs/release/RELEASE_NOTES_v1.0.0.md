# Release notes for v1.0.0

**Release name:** v1.0.0 School-security framework audit: reproducible content-analysis infrastructure 
**Release title:** RP-P1 v1.0.0 First Stable Research Protocol Release 
**Date:** 2026-07-31 
**Type:** First stable methodological / research-infrastructure release 
**Git tag:** `v1.0.0` 
**Canonical archive (citable):** [10.5281/zenodo.21711588](https://doi.org/10.5281/zenodo.21711588)

## Scope

This release freezes the public RP-P1 research infrastructure for a documentary content analysis of school-security and emergency-preparedness guidance.

It is a **stable methods and tooling release**. It is **not** an empirical results release.

The **canonical citable record** is the Zenodo archive at DOI **10.5281/zenodo.21711588**. The GitHub tag `v1.0.0` mirrors that archived repository state.

## Included

- Protocol, codebook schemas, claims policy, and research-programme architecture for RP-P1 
- Adopted amendments **PA-2026-07-31-001** (two-phase pilot), **PA-2026-07-31-002** (OPT-B / FNSS operational comparator), **PA-2026-07-31-003** (reliability estimability / sparsity) 
- Phase A operational pilot infrastructure (PROTOCOL_DEVELOPMENT_ONLY) 
- Phase-B benchmark design GO with FEMA FNSS 2010 as the single operational L1 comparator; CF-02 conceptual only 
- Independent-coder qualification workflow; `QUAL-FREEZE-v1` AUTHORIZED; `QUAL-ATTEMPT-v1` ADOPTED 
- Reliability estimability classifier and validators 
- Experimental Development Pack EXP-01-EXP-06 (synthetic only) 
- Full validator suite and automated tests (`make release-check`)

## Explicitly not included / not claimed

- No independent coder recruited or marked READY 
- Target package remains **SEALED** 
- No Phase-B target codes; no empirical intercoder α 
- Corpus freeze and full coding remain **NO_GO** 
- No manuscript Results / Discussion / Conclusion 
- Private manuscript tree is outside this repository 
- Copyrighted source PDFs are not redistributed (`local_sources/` gitignored) 
- RP-P2 remains planned; SLAPA remains `planned_unvalidated`

## Authoritative gate snapshot

| Gate | Status |
|---|---|
| Benchmark design | GO (OPT-B) |
| Benchmark source (FNSS) | READY |
| Qualification freeze | AUTHORIZED |
| Attempt policy | ADOPTED |
| Independent coder | NOT_READY |
| Target package | SEALED |
| Benchmark calibration | NO_GO |
| Corpus freeze | NO_GO |
| Full coding | NO_GO |

## Reproduce

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
make release-check
```

## Citation

Cite the Zenodo record:

> Andrés, C. (2026). School-security framework audit : reproducible content-analysis infrastructure (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.21711588

See also `CITATION.cff` and `CITATION.bib`.
