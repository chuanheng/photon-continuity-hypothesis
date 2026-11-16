# v0.86 — Research audit, evidence grades and paper draft

This is an audit of the Photon Continuity Hypothesis project, NOT a discovery of persistent individual photons.

## Re-executed local tests

- 36 versions reviewed (v0.50–v0.85).
- 34 existing historical unittest suites were independently re-executed successfully.
- 1,086 historical tests passed.
- 15 additional v0.86 audit assertions passed in the local audit package.
- v0.68 and v0.75 did not have complete locally runnable original suites.
- Historical v0.51–v0.66: 666 tests re-executed locally, but the 16-version GitHub source backfill is **NOT complete**. Do not confuse test files on a local volume with pushed GitHub content.

## Main conclusions

Standard bosonic symmetrization disallows treating tensor-product slot indices as permanent observable identities. Inaccessible Stinespring-style identity ancilla labels are operationally indistinguishable under system-only instruments. In an optical Poisson model, the putative constant identity phase delta can be exactly absorbed by an ordinary group offset b' = b + delta; a fair composite null remains observationally equivalent.

These are statements about specified mathematical models, NOT a universal proof that all possible hidden identities are impossible, and NOT evidence that original photons survive every absorption.

## Reproduce

Python 3.10+, numpy. From repository root:
```bash
python -m unittest discover -s tests -p 'test_research_audit_v086.py' -v
python tools/audit_repository_v086.py
```

The historical audit runner requires the /mnt/data/photon_v050 ... photon_v085 local directories and/or the appropriate '*_complete.zip' packages. It cannot run on a GitHub-only clone without those previous local sources.

Files:
- docs/research_audit_v086_zh.md — scientific audit and graded conclusions
- docs/manuscript_draft_v086_zh.md — non-peer-reviewed manuscript draft
- results/research_audit_v086.json — v0.50–v0.85 test-status matrix
- tests/test_research_audit_v086.py — 15 local-audit mathematics + manifest assertions
- tools/audit_repository_v086.py — historical local test re-run script
- results/test_results_v086.txt — recorded local execution summary

The downloadable full local audit ZIP also includes a complete per-version local file inventory (CSV), test output excerpts, SHA-256 manifest and a historical backfill preparation script. GitHub CI has not independently run the audit.
