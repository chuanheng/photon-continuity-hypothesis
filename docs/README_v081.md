# v0.81 — AR(1) phase drift and statistical false positives

**Status:** Finite-dimensional statistical simulation based on Gaussian phase readouts, NOT photon QED and NOT evidence of permanent historical photon identity.

The null-test false positive rates over 400 simulated experiments (n=80, AR(1) rho=.92, innovation sigma=.09, readout sigma=.05) are:
- Incorrect iid assumption: 94.25%
- Known-covariance GLS: 5.25%

Under an assumed phase delta=.15 rad, corrected power in these simulations: 29%.

Dependencies: Python 3.10+, NumPy and SciPy. Run from repository root:

```bash
python -m unittest discover -s tests -p 'test_correlated_drift_v081.py' -v
python -m experiments.run_v081
```

Files: docs/correlated_drift_v081_zh.md, models/correlated_drift_v081.py, tests/test_correlated_drift_v081.py, experiments/run_v081.py, results/correlated_drift_v081.json, results/test_results_v081.txt.

Local 27 unit tests passed in 0.027 s. No independent GitHub CI run has been performed. The bootstrap assumes known covariance and does not account for estimating drift parameters; adding an unknown group-specific bias still exactly confounds identity phase.
