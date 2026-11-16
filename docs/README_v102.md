# PCH-A v1.02: Continuous phase inference and decomposed optical calibration

**Status:** All data synthetic, using standard 50:50 bosonic Fock scattering; not experimental evidence for an individual permanent photon identity, and no new QED predictions.

This extends v1.01 from a fixed 27-point phase hyperparameter grid to continuous bounded maximum likelihood estimation of walk strength, sensor readout noise and sensor zero bias. The latent random-walk phase PATH is subsequently Gaussian-smoothed and sampled conditional on the fitted hyperparameters. **The hyperparameter MLE's uncertainty is NOT integrated. Thus this is NOT a complete continuous Bayesian posterior.**

Rather than aggregate all optical nuisance in two external probabilities, the simulation now independently calibrates PNR misclassification (the 11 and 21 rows of a five-class PNR response), source photon class populations, two threshold detector efficiencies/dark clicks, and illumination-triggered correlated electronic coincidences. It uses real bosonic Fock |2,1> near-simultaneous splitting versus an explicitly fully distinguishable far-delay limit. This is a simplified but decomposed forward model, not the arbitrary partially distinguishable three-boson theory.

Local exact research package: `photon_v102_complete.zip`. The 37 actual Python unit tests passed, all 21 content files were validated against a SHA-256 manifest, full 80+40 synthetic per-dataset results and two PNG plots included. ZIP SHA-256: `463f731f042cc8909d402e94d2d6a83122b4f3429123fca43de6c834fa9e5013`.

| Experiment | Trials | True M0 | Mean estimated M0 | RMSE | Bayesian 95% interval empirical coverage | Mean interval width |
|---|---:|---:|---:|---:|---:|---:|
| Base | 80 | .72 | .720144 | .019275 | 72/80=90% | .068134 |
| Outside v1.01 prior grid | 40 | .72 | .717306 | .025275 | 39/40=97.5% | .102616 |

The out-of-grid truth uses (walk=.18,read=.24,bias=.08). Means of fitted values are (.179192,.242093,.075460). The base truth (.095,.15,.015) yields average fits (.093990,.149316,.015314).

The local optical near/far coincidence Jacobian for five free variables (M0, triplet fraction, electronic background, efficiency A/B) is 2x5 of **rank 2**. Therefore the extra independent known-source/calibration references are necessary; near/far HOM coincidences alone cannot identify those five physical parameters.

**Caveat:** Base 72/80 coverage falls below nominal 95%; neither observed fraction is a universal coverage guarantee. MLE plug-in ignores hyperparameter uncertainty; this and sampling/grid approximations require further auditing. The independent GitHub counterpart has 25 tests defined but not confirmed to have run on CI.

## Run (GitHub companion)
```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_continuous_calibration_v102.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v102
```

See `docs/continuous_calibration_v102_zh.md`, `models/continuous_calibration_v102.py`, `tests/test_continuous_calibration_v102.py`, `results/continuous_calibration_v102_summary.json`, and `results/test_results_v102.txt`.

References: https://pmc.ncbi.nlm.nih.gov/articles/PMC4879567/ ; https://doi.org/10.1103/PhysRevLett.126.063602 .
