# Citation completion audit

**Date:** 2026-07-31  
**Rule:** Bibliographic citation ≠ authorized full-text access for coding.

| todo_id | Claim supported | Required source type | Candidate | Verified metadata | DOI / ID | Full-text for coding? | Decision |
|---|---|---|---|---|---|---|---|
| TODO-MAN-011 / TODO-PRO-001 | α band floors for content analysis | Primary methodological text | Krippendorff, *Content Analysis*, 4th ed. | SAGE, 2018; ISBN 9781506395678 / 9781506395661 | DOI 10.4135/9781071878781 | N/A (method citation only) | **Cite** `krippendorff2018content` |
| TODO-MAN-012 | Classic HRA / PSF lineage beyond SPAR-H | Primary HRA handbook | Swain & Guttmann 1983 THERP | NUREG/CR-1278; U.S. NRC | NUREG/CR-1278 | N/A (bib only; no HEP estimation claimed) | **Cite** `swain1983therp` |
| TODO-MAN-013 | Official AFN / functional-needs planning guidance | Official guidance | FEMA Nov 2010 FNSS shelter guidance | FEMA; Nov 2010 | FEMA media library / official PDF | **Does not** authorize CF-02 coding | **Cite** `fema2010fnss`; keep `kailes2007moving` |
| CF-02 coding | Benchmark calibration PE coding | Authorized L1 full text | Kailes & Enders 2007 and/or later CMIST ops doc | Article identity OpenAlex-confirmed | DOI 10.1177/10442073070170040601 | **Blocked** — PILOT_SOURCE_NO_GO | **Do not** treat bib access as coding access |

## Notes

- Page numbers for α bands are not invented; policy cites the 2018 edition’s standard interpretive bands as commonly applied (α≥0.800 / 0.667) and ties them to the cited work.
- CREAM (Hollnagel 1998) not required once THERP primary is present; SPAR-H remains the modern PSF illustration.
- Optional French/Caplan PE-fit primary remains P4 (van Vianen review already cited).
