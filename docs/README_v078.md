# v0.78 — Loss, dephasing and identifiability

This version models a three-outcome (erasure, plus, minus) interferometry experiment. It shows that identical predictive distributions remain indistinguishable for arbitrary sample sizes; a genuinely different phase shift can be statistically distinguished, but does not prove permanent identity of historical photons.

Dependencies: Python 3.10+; numpy.

Run from the repo root:

```bash
python -m unittest discover -s tests -p 'test_loss_dephasing_v078.py' -v
python -m experiments.run_v078
```

Files:
- `docs/loss_dephasing_v078_zh.md` — detailed Chinese report
- `models/loss_dephasing_v078.py` — computational model
- `tests/test_loss_dephasing_v078.py` — 27 tests
- `experiments/run_v078.py` — experiment
- `results/loss_dephasing_v078.json` — numerical results
- `results/test_results_v078.txt` — record of local test run

Local validation: 27 tests passed in 0.008 seconds. GitHub CI has not independently run them. This is not a QED prediction or experimental confirmation.
