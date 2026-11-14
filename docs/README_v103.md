# PCH-A v1.03 — Continuous hyperparameter importance-sampled HOM inference

**Research status:** entirely synthetic standard quantum optics and statistics, no empirical photon measurements and no independent evidence for permanent historical photon individuality.

v1.02 plugged in a point maximum-likelihood estimate for the continuous sensor random-walk strength, readout error and phase zero offset. v1.03 instead defines a bounded continuous prior uniform in (log walk_sd, log read_sd, bias), constructs a Hessian-based Gaussian proposal around the sensor MLE, and **importance-weights each proposed hyperparameter using the full sensor likelihood**. For each proposal, it samples the conditional Gaussian latent phase trajectory and physical calibration nuisance (PNR category response, source photon-number fractions, two detector efficiencies/dark counts, triggered electronics backgrounds). The near/far HOM optical likelihood reweights the combined samples, and the final estimator reports Bayesian equal-tail 95% credible intervals on intrinsic optical mode overlap M0.

**Numerical limitations:** this uses 120 importance proposals per outer dataset, a finite discrete M0 grid and approximate reference-based calibration posterior samples. It is not an exact analytic full Bayesian posterior, and Gaussian phase readout is an assumption which is deliberately violated in one stress case. Hyperprior is uniform in the transformed log scales, not in linear standard deviations. Sample effective size (ESS) is reported.

**Actually tested LOCAL ZIP**: `photon_v103_complete.zip`, with 38/38 passed unittests, 18 SHA-256 verified content files, two PNG plots, complete 170-dataset records, and detailed Chinese report.

| Case | Dataset count | Hyperparameter MLE plug-in coverage | Joint continuous hyperparameter marginal coverage | Mean joint interval width |
|---|---:|---:|---:|---:|
| Gaussian baseline | 70 | 61/70 | 63/70 | 0.074549 |
| Stronger Gaussian sensor | 50 | 45/50 | 49/50 | 0.120998 |
| 5% unmodeled readout outliers | 50 | 45/50 | 47/50 | 0.082057 |

Nominal Bayesian 95% credible intervals do not guarantee exact 95% frequentist coverage; repeated sample sizes are small and higher coverage accompanies wider intervals. The numerical methods do **not** identify a permanently surviving photon identity.

**Independent GitHub companion** (NOT byte-identical to exact local tested ZIP, remote GitHub CI NOT confirmed):

```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_hyperposterior_v103.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v103
```

- Chinese report: `docs/hyperposterior_v103_zh.md`
- Model: `models/hyperposterior_v103.py`
- Regression: `tests/test_hyperposterior_v103.py`
- Numeric local highlights: `results/hyperposterior_v103_summary.json`
- Reproduction: `experiments/run_v103.py`
- Local validation provenance: `results/test_results_v103.txt`

Sources: https://doi.org/10.1103/PhysRevLett.126.063602 ; https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf ; https://www.sciencedirect.com/science/article/pii/S0045782518300616 .
