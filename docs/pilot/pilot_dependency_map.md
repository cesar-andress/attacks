# Pilot dependency map (two-phase)

**Amendment:** PA-2026-07-31-001  
**NOT_FOR_SUBSTANTIVE_INFERENCE**

```
[Source acquisition P1–P4] ──GO──► [Phase A operational pilot]
                                           │
                                           │ outputs: codebook usability,
                                           │ amendments (non-benchmark),
                                           │ procedural disagreement types
                                           ▼
[Source acquisition P5/CF-02] ─NO_GO─► [Phase B benchmark calibration]
                                           │
                                           ▼
                              [Complete pilot] ─currently INCOMPLETE─
                                           │
                                           ▼
                              [Corpus freeze] ─NO_GO─
                                           │
                                           ▼
                              [Full coding / prereg submit] ─NO_GO─
```

| Stage | Inputs | Outputs | Enables |
|---|---|---|---|
| Phase A | P1–P4 authorized text; codebook v0.1 | Unitization; procedural coding; disagreement/amendment logs | Codebook clarity for Phase B; does **not** enable freeze |
| Phase B | P5/CF-02 or approved L1 amendment | Comparator calibration; benchmark rule closure | Complete pilot eligibility |
| Complete pilot | Phase A + Phase B | Closed pilot report | Freeze candidacy (with other freeze blockers) |
| Freeze | Complete pilot + provenance + dispositions | Frozen L0/L1 lists | Full coding |
| Full coding | Frozen corpus + frozen codebook | Confirmatory dataset | Manuscript Results |

**Hard rule:** Phase A data are `PROTOCOL_DEVELOPMENT_ONLY` and must not be merged into confirmatory analysis files.
