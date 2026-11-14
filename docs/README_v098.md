# v0.98 — Externally calibrated HOM with reference-sample cost

This release performs a **synthetic** study of HOM mode-overlap estimation with three imperfect external calibration channels: photon-number-resolving (PNR) source class confusion, Gaussian phase readout noise, and illumination-triggered electronics reference mismatch.

The new correction needs *known* optical source class references, an independent *known-zero-phase* reference, and an independent electronic control replicating the online trigger. These are STRONG assumptions, not quantities identifiable from two HOM coincidences alone.

With 300 paired simulated main experiments, true zero-drift M0=0.72, the uncorrected bias was +0.03765 and RMSE 0.04679. An additional 1,300, 13,000, or 130,000 reference trials (not counting per-block repeated phase readings) gave corrected biases +0.01750, +0.00978, and +0.00226; RMSE 0.03427, 0.02726, and 0.02266. All are Monte Carlo point-estimation results. **No valid joint 95% confidence interval coverage is claimed.**

## Files

- docs/joint_calibration_v098_zh.md — Chinese methods, assumptions and statistical limitations
- models/joint_calibration_v098.py — independently authored GitHub counterpart
- tests/test_joint_calibration_v098.py — 16 separately authored GitHub regression assertions
- experiments/run_v098.py — regeneration entrypoint
- results/joint_calibration_v098_summary.json — actual locally simulated numeric summary
- results/test_results_v098.txt — exact local execution provenance

**Complete downloadable local ZIP**: `photon_v098_complete.zip` contains 17 verified research files, the 34/34 actually executed local tests, 300 paired simulation results, two figures, and SHA-256 manifest. The GitHub counterpart code is not byte-identical and its tests have NOT been confirmed through CI.

## Run (GitHub companion)

Python 3.10+, NumPy, SciPy:

```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_joint_calibration_v098.py' -v
python -m experiments.run_v098
```

This is not a discovery of a historical photon identity or novel QED. Published work on HOM uncertainty and detector response tomography: https://doi.org/10.1364/AO.49.002173 and https://doi.org/10.1088/1367-2630/17/10/103044 .
