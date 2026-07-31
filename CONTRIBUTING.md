# Contributing

Thank you for interest in the RP-P1 public research infrastructure.

## Scope of this repository

This repository holds **methods, schemas, empty templates, validators, and synthetic experiment packs** for a documentary content analysis. It does **not** redistribute copyrighted guidance PDFs and does **not** contain the private manuscript.

## Before proposing changes

1. Read [`docs/protocol/claims_policy.md`](docs/protocol/claims_policy.md).  
2. Do not invent empirical results, coder identities, qualification outcomes, or registry identifiers.  
3. Do not unseal or prefill Phase-B target materials.  
4. Do not weaken qualification freeze, reliability estimability rules, or OPT-B comparator roles without a formal protocol amendment.  
5. Register scientific/editorial blockers in [`docs/todo/`](docs/todo/) rather than leaving unmarked TODOs in released surfaces.

## Development checks

```bash
pip install -e ".[dev]"
make release-check
```

All checks must pass before a contribution can be considered.

## Protocol amendments

Substantive coding-rule or comparator changes require a versioned amendment under `docs/protocol/amendments/` and an `amendment_log.csv` entry **before** target coding. Qualification freeze materials must not be silently edited.

## Citation of the released package

Cite the Zenodo archive: https://doi.org/10.5281/zenodo.21711588 (`CITATION.cff` / `CITATION.bib`).

## License

Contributions are accepted under the MIT License (`LICENSE`).
