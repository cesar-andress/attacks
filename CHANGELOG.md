# Changelog

All notable changes to this repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to adhere to [Semantic Versioning](https://semver.org/).

## [0.4.0] — 2026-07-31

### Added

- Experimental Development Pack (`experiments/EXP-01`…`EXP-06`) with synthetic
  stimuli, reference adjudications, response templates, analysis plans, ethics
  checklist, and data-management plan.
- Experiment validators, synthetic analysis/report generator, and tests.
- Makefile targets: `validate`, `test`, `experiment-demo`, `release-check`.
- Release notes and validation contract for the first annotated tag.

### Notes

- Pack is **internally_tested_synthetic** only; not a validated SLAPA survey;
  human experiments not executed; complete pilot still blocked on CF-02.

## [0.3.3] — 2026-07-31

### Added

- Research-programme charter and four-paper dependency register (RP-P1–P4).
- SLAPA architecture (planned/unvalidated), domain register, Paper 1→SLAPA
  traceability, evidence-layer model, Branch B programme record, validation
  roadmap, comparison safeguards, future claims policy, five-year roadmap,
  operational priority register.
- Lightweight `validate_research_program` checks and tests.

### Notes

- Does not redesign Paper 1; SLAPA is not validated; Priority 1 remains RP-P1
  execution (complete pilot still blocked on CF-02).

## [0.3.2] — 2026-07-31

### Added

- Protocol amendment PA-2026-07-31-001: two-phase pilot (Phase A operational /
  Phase B benchmark calibration).
- Separate gate register (`data/gates/gate_register.csv`).
- Phase A operational codebook pilot on P1–P4 (29 PEs): unitization, primary
  coding, simulated procedural second pass, adjudication, disagreement and
  amendment logs, benchmark-dependent decision register.
- Pilot-phase validator and tests; copyright-safe gitignored excerpts.
- CF-02 access track kept active; no silent comparator substitution.

### Notes

- Complete-pilot source gate remains **PILOT_SOURCE_NO_GO**.
- Phase A data: `NOT_FOR_SUBSTANTIVE_INFERENCE` /
  `NOT_FOR_BENCHMARK_COMPARISON` / `PROTOCOL_DEVELOPMENT_ONLY`.
- Corpus freeze and full coding remain **NO_GO**.

## [0.3.1] — 2026-07-31

### Added

- Pilot source-acquisition manifests, checksums, dossiers, and storage policy.
- Local full-text under gitignored `local_sources/pilot/` for CF-16, CF-03,
  CF-15, CF-13 (CF-02 full text not acquired).
- Validation for authorization statuses, dispositions, SHA-256, and
  `tracked_in_git` consistency.
- Gate file: **PILOT_SOURCE_NO_GO** (sole comparator CF-02 unauthorized).

### Notes

- Did not authorize complete-pilot coding or corpus freeze at 0.3.1.
- Live CISA/education.gouv.fr downloads were blocked; Wayback official-URL
  captures used where recorded.

## [0.3.0] — 2026-07-31

### Added

- Freeze-readiness register and candidate disposition recommendations
  (recommendations only; corpus **not** frozen).
- RQ2 denominator decision (primary: rung ≥ 1; complementary: all PEs).
- Reliability policy v0.1 with α bands and contingencies.
- Formal Branch B / Family F `inactive_for_current_study` decision.
- Pilot sampling plan and empty pilot data schemas marked
  `NOT_FOR_SUBSTANTIVE_INFERENCE`; execution blocked (no local source text).
- Preregistration-readiness checklist and NO-GO report.
- Verified official landing URLs for CF-03 (CISA) and CF-16 (GOV.UK).
- Validation coverage for disposition/freeze/pilot artefacts.

### Notes

- Decision for corpus freeze / full coding: **NO-GO** until local text +
  pilot + provenance holds are resolved.

## [0.2.1] — 2026-07-30

### Added

- OpenAlex literature verification table, schema, policy doc, and
  `scripts/verify_openalex.py` (API key from environment only).
- Seeded OpenAlex confirmations for Kailes & Enders 2007 (CF-02) and
  related CSTAG peer-reviewed literature (CF-06), without authorizing
  corpus inclusion or resolving operational L1 manuals.

## [0.2.0] — 2026-07-30

### Added

- Provisional candidate-framework register v0.1 (`CF-01`–`CF-22`) with
  identity, screening, and provenance-confidence fields.
- Provisional L1 document registry entries and framework–document
  relationship types.
- Pre-coding counterexample commitments CSV (surface indications only).
- Validation rules rejecting frozen/final inclusion labels, `EU/UK`
  geography, unverified CF-22 upgrades, missing unresolved actions, and
  codebook tokens in counterexample surfaces.

### Notes

- Register is exploratory and **not frozen**.
- No full-text screening or substantive coding performed.
- Several bibliographic and authorship claims remain unresolved by design.

## [0.1.0] — 2026-07-30

### Added

- Initial public scaffolding for a structured content-analysis audit of
  school-security and emergency-preparedness frameworks.
- L0/L1/L2 data model (framework / document / prescriptive element).
- Draft codebook v0.1 (YAML + human-readable Markdown).
- Draft demand-entailment table (constructed examples only).
- JSON Schemas for framework, document, PE, and coding records.
- Empty CSV templates for corpus and coding workflows.
- Validation scripts and constructed-fixture tests.
- Protocol outline, claims policy, corpus-selection notes, and data dictionary.
- MIT licence and `CITATION.cff`.

### Notes

- No framework audit has been performed.
- No copyrighted framework text or PDFs are included.
- Codebook and entailment table are draft instruments pending freeze before
  main coding.
