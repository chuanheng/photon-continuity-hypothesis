# v0.99 — Conditional Joint Bootstrap for HOM Calibration

**Scientific status:** Synthetic-data statistical audit; not a laboratory experiment, a new QED theory, or evidence for permanently surviving historical individual photons.

This model jointly resamples eight observable/calibration channels: (i) near/far HOM coincidence counts, (ii) source event categories, (iii) two calibrated PNR confusion rows, (iv) zero-phase reference, (v) repeated phase sensor readouts for 40 blocks, (vi) matched online-trigger electronics reference, (vii) blocked detector dark counts, (viii) independent detector efficiencies.

**Critically, this is NOT a fully integrated latent-state-space likelihood or posterior.** The environmental phase path is plugged in from noisy repeated sensor readings, then taken as fixed when resampling. This may induce biased intrinsic overlap and undercoverage even after all measured calibration channels have been resimulated.

## Local actually executed experiment

The complete `photon_v099_complete.zip` passed 31/31 Python unit tests and carries SHA-256 checksums for 18 research files, 180 full outer experiment records, 14,220 joint bootstrap replications, and two PNG figures.

True intrinsic optical overlap M0=.72. There were 60 outer datasets per calibration budget and 79 inner bootstrap replicates each.

| External reference shots | Mean corrected M0 | RMSE | Observed nominal 95% interval coverage |
|---:|---:|---:|---:|
| 1,300 | .733181 | .035228 | 43/60 (71.7%) |
| 13,000 | .729018 | .029686 | 48/60 (80%) |
| 130,000 | .722213 | .026595 | 53/60 (88.3%) |

The experiment-period mean mode overlap, a DIFFERENT estimand, was covered in 56/60, 55/60 and 55/60 cases. Larger calibration budgets reduced point-estimate RMSE but did **not** verify the desired nominal 95% coverage for the intrinsic parameter.

This audit is conditional on a correctly specified synthetic source and detectors, known optical calibration inputs, a trusted zero-phase reference, and a separate electronics reference genuinely matching the main measurement. Those are strong experimentally expensive assumptions.

## Reproduction

Use Python 3.10+, NumPy, SciPy. From repo root:
```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_joint_uncertainty_v099.py' -v
python -m experiments.run_v099
```

The GitHub model and regression tests are **independently authored companion versions**; their byte equivalence to the locally executed ZIP is not claimed. Their remote CI execution has **not** been verified. The exact local 31 tests are inside the ZIP; the remote companion has 18 test definitions.

- Full research report: `docs/joint_uncertainty_v099_zh.md`
- Model: `models/joint_uncertainty_v099.py`
- Regressions: `tests/test_joint_uncertainty_v099.py`
- Run entry: `experiments/run_v099.py`
- Numeric summary: `results/joint_uncertainty_v099_summary.json`
- Test provenance: `results/test_results_v099.txt`

Literature context: https://doi.org/10.1103/PhysRevLett.126.063602 ; https://doi.org/10.1364/AO.49.002173 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC10733784/ .

Next: v1.00 should infer the *latent stochastic phase trajectory* rather than treat noisy measurements as the exact path.
