# Changelog

All notable changes to this repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to adhere to [Semantic Versioning](https://semver.org/).

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
