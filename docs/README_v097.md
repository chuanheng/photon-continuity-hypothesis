# v0.97 — HOM calibration robustness under deliberately incorrect monitors

**Scientific status:** Synthetic statistics based on ordinary optical Fock-mode interference; no real laboratory measurements or independent claim of permanent historical individual photon identity.

This study challenges the v0.96 ideal independent calibrations: a PNR 5-class confusion matrix, Gaussian phase-sensor reading error, and offset between optically-triggered electronic reference clicks and on-line noise. The inference/bootstrap pipeline still assumes the calibrations are perfect.

Local `photon_v097_complete.zip` was **actually tested**: 44/44 tests passed. It contains 17 SHA-256 verified research files, full 480 synthetic outer datasets (8 scenarios × 60), 37,920 inner bootstrap replications (79 each), two numerical figures, complete Chinese mathematical report, and exact local source files.

Truth: intrinsic optical mode overlap `M0=0.72`. The baseline had mean estimated 0.71136 and nominal 95% CI coverage 54/60. The combined monitor error had mean estimate 0.75690 with only 36/60 interval coverage of M0. Neither percentage is a universal coverage rate; 60 outer simulations give substantial binomial uncertainty.

PNR errors in the principal stress study are limited to true `|2,1>` three-photon events being reported as ordinary `|1,1>` pairs. Phase reading: `u_reported = u_true + bias + independent Gaussian error`; true mode overlap `M_t=M0 exp(-|u_true|)`. Matched electronic monitor reports `q_reference=q_online+offset`. None of these modeled effects suggests an additional photon-history label.

The analysis distinguishes **intrinsic zero-drift overlap M0** from **experiment-period average overlap**; the noisy sensor affects these estimands differently. In the fixed-trajectory population-precision calculation, the true optical measurement probabilities and calibrated source probabilities are taken exact, and 40-point Gauss–Hermite quadrature integrates sensor-reading error.

The GitHub companion model and its 22 regression methods were **separately authored**, not byte-identical to the locally executed ZIP. No remote GitHub CI run is claimed.

From repository root (Python 3.10+, NumPy, SciPy):

```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_calibration_stress_v097.py' -v
python -m experiments.run_v097
```

Files: `docs/calibration_stress_v097_zh.md`, `models/calibration_stress_v097.py`, `tests/test_calibration_stress_v097.py`, `experiments/run_v097.py`, `results/calibration_stress_v097_summary.json`, `results/test_results_v097.txt`.

Research antecedents: https://doi.org/10.1103/PhysRevA.102.033714 and https://doi.org/10.1088/1367-2630/17/10/103044 .
