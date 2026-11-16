# v0.84 — Model misspecification and apparent photon identity signals

Study: raw Poisson two-quadrature photon counts, independent AR(1) phase sensor, hyperparameter refitting inside parametric bootstrap, outer Monte Carlo testing nominal 5% rejection rates under three ordinary physics mechanisms.

**All 3 worlds have zero identity effect.** Correct stationary AR(1) model: 4/120 rejections (3.33%); random walk misspecification: 69/120 (57.5%); omitted ordinary test-group bias: 108/120 (90%). Off-model rejections indicate a mis-specified restricted null, NOT identification of permanent historical photon identity.

Dependencies: Python 3.10+, numpy, scipy.

From repository root:

```bash
python -m unittest discover -s tests -p 'test_robustness_v084.py' -v
python -m experiments.run_v084
```

Files:
- docs/robustness_v084_zh.md — Chinese mathematical research report and caveats
- models/robustness_v084.py — complete raw-count model and bootstrap
- tests/test_robustness_v084.py — 29 unittest checks
- experiments/run_v084.py — full reproduction script
- results/robustness_v084_summary.json — aggregated numerical results
- results/test_results_v084.txt — local executed test record

The user-downloadable photon_v084_complete.zip also contains the complete per-replicate p-value dataset at results/robustness_v084.json.

Only the independent sensor rho/sigma estimates are re-fitted in this fast GLS-based bootstrap. Detector efficiency/visibility/dark and sensor readout variance are held known. It is NOT the full latent-state Poisson MAP profile statistic of v0.83. No GitHub Actions run is claimed and no QED photon-identity prediction is provided.
