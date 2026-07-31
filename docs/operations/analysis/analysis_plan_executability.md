# Analysis-plan executability audit (no empirical data)

**Scope:** verify that planned outputs for registered RQs can be produced when real data exist.  
**Constraint:** research questions unchanged; no combined preparedness score; RQ4 secondary and document-specific; FNSS not a gold standard.

## Mapping (scripts / artefacts → planned tables)

| Planned output | Supporting artefact / script | Status |
|---|---|---|
| Corpus flow counts | Corpus freeze manifest + metadata CSVs; `validate_metadata` | Ready when freeze exists |
| Document characteristics | `data/` metadata schemas + summary notebooks/scripts in protocol analysis plan | Schema ready; empirical empty |
| Unit counts | Coding CSVs + `validate_coding` | Ready when coding locked |
| L0/L1/L2 distributions | Coding fields + analysis tables (post-adjudication layer) | Blocked on data |
| Executability-ladder distributions | `executability_rung` | Blocked on data |
| Locus distributions | Locus fields; RQ2 denominator policy | Blocked on data |
| Manifest cue distributions | Cue fields in coding schema | Blocked on data |
| Demand-source distributions | Demand-source fields | Blocked on data |
| Document-level summaries | Aggregation scripts (to run on analytical dataset) | Lineage defined |
| Counterexample tables | Counterexample register + coding | Schema ready |
| Reliability tables | `reliability_pipeline` + PA-003 classifier | Synthetic fixtures pass; empirical absent |
| Missingness tables | Pipeline missingness block | Ready |
| Sparse-category diagnostics | PA-003 / reliability estimability | Ready (classifier) |
| Collapsed-rung sensitivities | `collapsed_engagement` helpers | Ready |
| Document-specific FNSS contrast (RQ4) | OPT-B comparator coding only | Secondary; blocked on calibration/coding |
| Contingent taxonomic summaries | Authorized only if confirmatory reliability allows | Gated |

## Explicit non-goals

- No combined preparedness / quality score.  
- No Branch B activation.  
- No substitution of synthetic fixture outputs into manuscript Results.  
- No conversion of FNSS into a gold standard.

## Fixture policy

All technical validation outputs must carry `SYNTHETIC_NOT_FOR_MANUSCRIPT` and are excluded from Results.
