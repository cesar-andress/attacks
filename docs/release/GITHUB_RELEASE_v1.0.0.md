# GitHub Release payload — v1.0.0

**Status:** tag `v1.0.0` pushed to `origin`; GitHub Release UI creation blocked in this environment (API 403: token lacks `contents:write` / release permission).

**Create manually:**

```bash
gh release create v1.0.0 \
  --title "RP-P1 v1.0.0 — First Stable Research Release" \
  --notes-file docs/release/RELEASE_NOTES_v1.0.0.md
```

Or open: https://github.com/cesar-andress/attacks/releases/new?tag=v1.0.0

**Title:** RP-P1 v1.0.0 — First Stable Research Release  

**Body:** use `docs/release/RELEASE_NOTES_v1.0.0.md` (or the shorter summary in the release-prep commit message / prior agent notes).
