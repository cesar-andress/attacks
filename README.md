# School-security framework audit (public infrastructure)

**Release:** [v1.0.0](https://github.com/cesar-andress/attacks/releases/tag/v1.0.0) — RP-P1 First Stable Research Protocol Release (methods/infrastructure; not empirical results).

**Canonical archive (cite this):** [https://doi.org/10.5281/zenodo.21711588](https://doi.org/10.5281/zenodo.21711588) (`10.5281/zenodo.21711588`)

Public, reproducible research software and metadata templates for a **structured documentary content analysis** of school-security and emergency-preparedness frameworks.

This repository supports **methods, schemas, codebook drafts, empty data templates, and validation tooling**. It does **not** contain the private manuscript, and it does **not** redistribute copyrighted framework PDFs unless redistribution is explicitly permitted and documented.

See [`docs/release/RELEASE_NOTES_v1.0.0.md`](docs/release/RELEASE_NOTES_v1.0.0.md), [`CITATION.cff`](CITATION.cff), and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Scientific purpose

The study asks whether recognized school-security and preparedness frameworks address, in their own prescriptive text:

1. **Protective-action executability** — documentary engagement with whether measures are assessed/tested as executable by intended occupants under realistic conditions (Branch E / current-paper spine).
2. **Threat detectability** — detection/assessment process codes and false-positive safeguards (Branch F) — **inactive for the current paper**; reserved for a secondary module or separate study ([`docs/protocol/branch_b_scope_decision.md`](docs/protocol/branch_b_scope_decision.md)).

These are **two separate analytical branches**. The repository deliberately does **not** define or accept a single combined “inclusive security score.”

**Corpus freeze status (2026-07-31):** **not frozen** — see [`docs/protocol/go_nogo_report.md`](docs/protocol/go_nogo_report.md) (**NO-GO**).

**Benchmark design (PA-2026-07-31-002 / OPT-B):** **GO** — CF-02 remains conceptual (access still NO_GO); FEMA FNSS 2010 is the single operational Phase-B L1 (`DOC-ALT-FNSS-001`, checksum verified).

**Reliability estimability (PA-2026-07-31-003):** adopted — distinguish non-estimable α from coder failure; exact agreement + marginals required; no post-hoc primary-ladder collapse.

**Phase B execution:** **NO_GO** until an independent coder is qualified and coding/adjudication complete. Source readiness ≠ calibration complete. Corpus freeze and full coding remain **NO_GO**.

**Two-phase pilot (PA-2026-07-31-001):** Phase A on P1–P4 = **COMPLETED** (`PROTOCOL_DEVELOPMENT_ONLY`). Package: [`docs/phase_b/`](docs/phase_b/). Gates: [`data/gates/gate_register.csv`](data/gates/gate_register.csv).

**Broader research programme:** Paper 1 (this documentary audit) is the empirical foundation of a four-paper programme on inclusive organisational preparedness (SLAPA architecture planned/unvalidated). Programme docs: [`docs/research_program/`](docs/research_program/). Operational Priority 1 remains completing RP-P1.

**Experimental Development Pack:** Synthetic methodological experiments EXP-01–EXP-06 under [`experiments/`](experiments/) — designed for future coder/expert studies; **not** a validated SLAPA survey; human experiments **not** executed. Run `make release-check`.

**Unresolved-item register:** Every open scientific/editorial blocker is tracked in [`docs/todo/`](docs/todo/) (`unresolved_item_register.csv` + allowlist). `make validate` includes `validate_todos` (rejects unregistered open editorial markers; does not ban legitimate scientific uses of “pending”).

## What this study is (and is not)

| This study **is** | This study **is not** |
|---|---|
| A documentary audit of frameworks | An effectiveness / outcome evaluation |
| A content analysis of what documents prescribe and assess | A claim that measures work (or fail) in real incidents |
| A methods-preregistrable coding design | A replacement for field validation of school practice |

Allowed and disallowed claim types are bindingly stated in [`docs/protocol/claims_policy.md`](docs/protocol/claims_policy.md).

## Units of analysis (L0 / L1 / L2)

| Level | Unit | Role |
|---|---|---|
| **L0** | Framework | Doctrine issued by an authority (may span multiple documents) |
| **L1** | Document | Versioned artifact (PDF/edition/tool) |
| **L2** | Prescriptive element (PE) | Atomic coding unit: one discrete prescription, control, or assessment question |

Aggregate upward from PE codes; do not impute framework-level judgements downward onto PEs.

**Default normalization denominator:** counts and rates are expressed **per PE** (or as PE proportions). Word-count density may be added later as a sensitivity analysis only.

## Coding families

| Family | Name |
|---|---|
| A | Framework metadata and scope |
| B | Security measures prescribed |
| C | Procedural demands |
| D | Contextual supports and accommodations |
| E | Protective-action executability |
| F | Threat detectability |
| G | Population and setting differentiation |
| H | Evidence, testing, and validation |
| I | Security–accessibility conflicts and trade-offs |

Executability **depth (rung 0–5)** and **locus** (individual / subgroup / setting / multiple / not specified) are **orthogonal** fields. See the codebook.

For Family C, every coded demand stores a separate `demand_source`:

- `explicit` — stated in text
- `entailed` — necessarily entailed by a prescribed action (entailment table)
- `ambiguous_memo` — uncertain; **must not** count as demand presence in confirmatory analyses

## OpenAlex literature checks

Scholarly identity for selected literature-linked candidates may be verified with the OpenAlex API (`scripts/verify_openalex.py`). Policy and limits: [`docs/protocol/openalex_verification.md`](docs/protocol/openalex_verification.md).

- Load `OPEN_ALEX_KEY` from the environment; never commit or print it.
- OpenAlex does **not** authorize corpus inclusion and is not authoritative for current government guidance versions or official URLs.

## Candidate frame v0.1 (current data status)

`data/corpus/candidate_frameworks.csv` holds a **provisional candidate register** assembled for later screening.

- It is **not** a frozen or final corpus.
- Do not treat candidate counts as a definitive “8 frameworks / 10–12 documents” study corpus.
- **Identity status** (is the doctrine identifiable?) is distinct from **screening status** (likely eligibility).
- **Surface indications** and `counterexample_commitments.csv` are sampling commitments, **not** audit findings or codebook values.
- England/UK use `geographic_region=Europe` and `eu_member_state=no` — never `EU/UK`.

## Freeze rules and falsification

Before main coding:

1. Complete provenance checks and full-text screening; then freeze the **corpus inclusion list**.
2. Freeze the **codebook** and **demand-entailment table** versions.
3. Preregister directional expectations **and** the disconfirming pattern.

**Benchmark comparator candidates** (accessibility / AFN) provide a falsification route once eligibility is confirmed: if general frameworks reach comparator scores on executability/support codes, the gap hypothesis is weakened or retired. They are **not** experimental “positive controls.”

## Copyright and local sources

- The public repo stores **metadata, URLs, schemas, templates, and derived open data**.
- Local PDFs (if any) belong under ignored paths such as `data/sources/` and are **not** tracked.
- `verbatim_trigger_text` fields may hold short excerpts for coding auditability; researchers remain responsible for fair-dealing / fair-use and copyright limits. **Do not populate PE tables with real framework text until legally reviewed.**
- The manuscript is maintained **privately outside this repository**.

## Repository layout

```text
attacks/
├── README.md
├── Makefile              # validate / test / experiment-demo / release-check
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── docs/                 # protocol, codebook, research_program, todo/, release
├── experiments/          # Experimental Development Pack (EXP-01…06)
├── schemas/              # JSON Schemas for L0/L1/L2/coding/experiments
├── data/                 # CSV templates (empty / constructed only)
├── src/school_security_audit/   # validation library (importable)
├── scripts/              # CLI wrappers
└── tests/                # constructed fixtures + experiment tests
```

## Quick start

```bash
cd ~/papers/attacks/attacks
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Full public validation contract (includes synthetic experiment demo)
make release-check
```

Without installing the package:

```bash
PYTHONPATH=src make release-check
```

## Citation

Please cite the Zenodo archive (preferred) or the equivalent BibTeX in [`CITATION.bib`](CITATION.bib):

> Andrés, C. (2026). *School-security framework audit — reproducible content-analysis infrastructure* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.21711588

Machine-readable metadata: [`CITATION.cff`](CITATION.cff).

## Licence

MIT — see [`LICENSE`](LICENSE). Framework source documents retain their own copyright terms and are not covered by this licence.
