# v0.82 — Raw Poisson detector counts with AR(1) correlated drift

This research edition uses an effective two-port Poisson counting model, paired test/calibration conditions, separate dark frames, and latent AR(1) drift. Every null-model parametric bootstrap replication RE-FITS both null and alternative models, including fitted eta, visibility, dark-count mean, common phase, and the latent trajectory.

**Important:** rho and innovation sigma are treated as independently known and are not re-estimated. The profile statistic is a penalized likelihood/MAP difference, NOT an exact marginalized likelihood ratio. There is no new QED photon-identity prediction here.

Local Python run: **29/29** unit tests passed; bootstrap 60/60 optimizations reported convergence. Bootstrap p-value for one simulated null dataset 0.1803278689; this is not a measured experimental discovery.

Dependencies: Python 3.10+, NumPy, SciPy.

Run from repository root:
```bash
python -m unittest discover -s tests -p 'test_count_hierarchy_v082.py' -v
python -m experiments.run_v082
```

Files:
- docs/count_hierarchy_v082_zh.md
- models/count_hierarchy_v082.py
- tests/test_count_hierarchy_v082.py
- experiments/run_v082.py
- results/count_hierarchy_v082.json
- results/test_results_v082.txt

The original full local ZIP contains the 60 replicate statistics and verbose unittest output. No remote GitHub CI execution is claimed.
