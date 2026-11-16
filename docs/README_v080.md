# v0.80 — Fair model competition and independent calibration

**Scientific status:** A mathematical/statistical model of interferometer counts, not QED or experimental evidence for conserved individual photon identity.

Our results: test-only rank 4/5; joint test+calibration Fisher rank 5/5 under the strong assumption of shared ordinary drift; allowing an unrestricted test-specific ordinary drift restores exact predictive equivalence.

Dependencies: Python 3.10+, NumPy, SciPy.

Run from repository root:

```bash
python -m unittest discover -s tests -p 'test_fair_model_competition_v080.py' -v
python -m experiments.run_v080
```

Files:
- `docs/fair_model_competition_v080_zh.md` — complete Chinese study
- `models/fair_model_competition_v080.py` — full statistical model
- `tests/test_fair_model_competition_v080.py` — 28 tests
- `experiments/run_v080.py` — reproduces JSON results
- `results/model_competition_v080.json` — numerical results
- `results/test_results_v080.txt` — local test execution summary

Original local full project ZIP contains verbose unittest log. 28/28 tests passed locally; no remote GitHub Actions run is claimed.
