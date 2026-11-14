# v0.88 — Originality review and multitime hidden-memory example

**Scientific status:** This version performs a non-exhaustive literature-based originality review of PCH-A. Stinespring uniqueness, bosonic symmetrization, structural parameter redundancy, and the process-tensor formalism are established theory. No permanent historical photon identity, novel field equation or original theorem was established.

A qubit toy example provides one-step channel E(rho)=(rho+X rho X)/2. Two consecutive time steps reusing the same hidden random bit output |0><0| from initial |0>, while independent random bits output I/2; equal-prior optimal guessing success is 75%. This difference shows ordinary multitime environment memory, not evidence for a surviving original photon.

Python 3.10+ and numpy. Run from GitHub repo root:
```bash
python -m unittest discover -s tests -p 'test_originality_process_v088.py' -v
python -m experiments.run_v088
```

Files:
- docs/originality_review_v088_zh.md: literature audit, claims, limitations
- results/originality_matrix_v088.json: claim-by-claim novelty classification
- models/originality_process_v088.py: computational model
- tests/test_originality_process_v088.py: 25 unit tests
- experiments/run_v088.py: reproducibility script
- results/multitime_process_v088.json: numeric output
- results/test_results_v088.txt: actual local test summary

Local: 25/25 tests passed. GitHub CI has not been confirmed to run the v0.88 tests.
