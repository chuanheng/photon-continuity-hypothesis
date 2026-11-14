# v0.85 — Fair ordinary-memory composite null

**Scientific status:** finite-dimensional Poisson-count statistical model, NOT QED, and NOT evidence of permanent historical photon identity.

If an identity theory predicts a constant extra phase delta but the ordinary-memory theory permits its own test-group phase bias b, the null can set b'=b+delta. This reproduces the complete joint counting distribution for stationary AR(1), nonstationary random walk, and stepwise drift. No number of photons or bootstrap replicates can distinguish these two explanations within the stated observables.

Run from the repository root (Python 3.10+, NumPy, SciPy):

```bash
python -m unittest discover -s tests -p 'test_fair_composite_null_v085.py' -v
python -m experiments.run_v085
```

Files:
- `docs/fair_composite_null_v085_zh.md`: Chinese research report
- `models/fair_composite_null_v085.py`: numerical model
- `tests/test_fair_composite_null_v085.py`: 31 unittest tests
- `experiments/run_v085.py`: numerical reproduction
- `results/fair_composite_null_v085.json`: numerical result
- `results/test_results_v085.txt`: local test execution record

Local tests 31/31 passed in 0.009 seconds. GitHub Actions have NOT independently executed this version. The downloadable ZIP also contains the expanded report and original local file layout.
