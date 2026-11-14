# v1.00 — Gaussian latent phase smoothing and marginalized HOM likelihood

This version replaces the v0.99 *fixed plug-in phase path* assumption with an explicit **Gaussian random-walk latent-state posterior** for 40 environmental phase blocks. A tridiagonal precision matrix yields the exact linear-Gaussian smoother. The nonlinear phase attenuation `A=mean(exp(-abs(u)))` is propagated by samples from the full smoothed path distribution and integrated into a binomial HOM near-delay likelihood on a 401-point intrinsic-overlap grid.

**Scientific scope:** This is a useful **conditional hierarchical model** with KNOWN detector/source/PNR/trigger-electronics nuisance and known random-walk/readout noise hyperparameters, NOT a full joint posterior over the unknown calibration channels of v0.99. No laboratory evidence for permanent historical photon identity or new QED physics is asserted.

Local actual execution: 27/27 Python tests passed; three sensor-read budgets (1,2,20 per block), 100 synthetic outer datasets each, 700 latent paths for each optical likelihood.

| Repeated sensor reads | Fixed phase coverage | Marginalized phase coverage | Fixed mean 95% interval width | Marginalized mean width |
|---|---:|---:|---:|---:|
| 1 | 79/100 | 99/100 | 0.05697 | 0.08005 |
| 2 | 82/100 | 94/100 | 0.05699 | 0.07042 |
| 20 | 92/100 | 97/100 | 0.05714 | 0.05895 |

Intervals are Bayesian **95% equal-tail credible intervals**, with their frequentist coverage empirically checked on fixed synthetic truth M0=0.72. Hundred-run finite simulation uncertainty prevents a categorical nominal-coverage guarantee.

**Original complete ZIP:** `photon_v100_complete.zip`, 17 SHA-256 verified research files plus manifest, exact locally executed source and 27 tests, 300 full per-dataset results, two PNG figures. SHA-256 of ZIP: `f379fcef8843248e7f69d4f317a4af4a4d55d1b7199001a0844135e7fe2ef9d1`.

GitHub model and tests are separately authored companion files; not claimed to be byte-identical or GitHub CI-tested. Its test file has 22 independent regression methods.

Run from repo root (Python 3.10+, NumPy, SciPy):
```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_latent_phase_v100.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v100
```

Research: `docs/latent_phase_v100_zh.md`, model: `models/latent_phase_v100.py`, tests: `tests/test_latent_phase_v100.py`, results: `results/latent_phase_v100_summary.json`, provenance: `results/test_results_v100.txt`.

Prior literature: https://doi.org/10.1364/AO.49.002173 ; https://doi.org/10.1103/PhysRevA.102.033714 .
