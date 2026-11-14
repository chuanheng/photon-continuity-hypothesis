# v0.83 — Independent AR(1) noise calibration and refitting bootstrap

This version extends v0.82 Poisson detector counts: estimate AR(1) correlation and innovation variance from an INDEPENDENT noisy phase sensor using the exact Gaussian Kalman innovations likelihood, then for EACH parametric bootstrap replicate refit rho and sigma on a new calibration record and refit BOTH optical null/alternative penalized-MAP models on new counts.

**Scientific caveats:** This is a toy statistical model; not QED, not a proof of original photon persistence, not evidence of a new interaction. Sensor noise standard deviation 0.03 is known; optical and sensor latent paths are independent but share AR(1) distribution parameters; a free ordinary group-specific phase b exactly absorbs the hypothesized identity phase delta. Bootstrap B=24 is a method check only.

Dependencies: Python 3.10+, numpy, scipy. Version v0.82 model code is a dependency, already in the branch.

Run from repository root:

```bash
python -m unittest discover -s tests -p 'test_calibrated_bootstrap_v083.py' -v
python -m experiments.run_v083
```

Files:
- `docs/calibrated_bootstrap_v083_zh.md` — Chinese report
- `models/calibrated_bootstrap_v083.py` — calibration/Bootstrap model
- `models/count_hierarchy_v082.py` — existing Poisson optics dependency
- `tests/test_calibrated_bootstrap_v083.py` — 26 unittest cases
- `experiments/run_v083.py` — numerical experiment
- `results/calibrated_bootstrap_v083.json` — summary
- `results/test_results_v083.txt` — local test execution record

Locally 26/26 tests passed. No GitHub-hosted CI run is claimed.
