# Local storage and redistribution policy

## Tracked vs untracked

| Content | Location | Git |
|---|---|---|
| Full-text PDFs/HTML of guidance | `local_sources/` | **Ignored** |
| Acquisition metadata | `data/source_registry/` | Tracked |
| Checksums | `data/source_checksums/` | Tracked |
| Permission queue | `data/source_registry/permission_request_queue.csv` | Tracked |

`.gitignore` includes `local_sources/`, `data/sources/`, `*.pdf`, `*.docx`.

## Authorization vs redistribution

Public downloadability ≠ permission to commit full text to a public repository.

Default for this study:

- **Access/analyze/retain locally:** allowed for statuses `public_official_download`, `public_official_web_text`, `public_archive_download`, `permission_granted`.
- **Redistribute full text in public git:** **not** done unless an explicit licence record is added.
- **Quote:** short excerpts for PE coding only, under applicable research/fair-use rules.

## Reacquisition

Researchers without local copies should re-fetch from `authoritative_url` / `archive_url` recorded in `pilot_source_acquisitions.csv` and verify `sha256`.
