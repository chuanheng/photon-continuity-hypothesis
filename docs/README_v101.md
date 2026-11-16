# PCH-A v1.01 — Unknown phase hyperparameters and calibrated optical controls

This version extends the conventional HOM optical calibration analysis through a **finite hierarchical Bayesian model** for unknown phase random-walk strength, sensor readout noise and zero bias. It integrates conditional Gaussian latent phase paths with independently calibrated optical control probabilities, using an explicit 27-point hyperparameter prior grid and 251-point HOM intrinsic overlap grid.

**Research status:** Entirely synthetic calculations. This is not a new QED prediction and does not establish the permanent historical identity of any individually labeled photon.

The sensor zero phase is externally calibrated with 80 references. The two optical control probabilities for known HOM overlaps M=0 and M=1 each receive 15,000 independent shots and Beta posterior updates. These controls aggregate ordinary source PNR, detector efficiency and electronics nuisance into the two measurable probabilities c0 and c1. **The underlying nuisance channels are not separately estimated in this version**, despite being physically present in the forward model. The known optical control states themselves are strong laboratory assumptions.

### Tested local release

The full downloadable `photon_v101_complete.zip` includes 21 SHA-256 verified research files plus a manifest, exact locally executed code, full Chinese report, 38/38 actually passed Python unittests, 120 main synthetic datasets, 80 prior-support stress datasets, two PNG plots and complete reproducibility logs.

True intrinsic overlap M0=0.72; 40 main datasets per sensor repeated-reading setting.

| Readings/block | Plug-in 95% interval covered | Joint Bayesian 95% interval covered | Plug-in mean width | Joint mean width |
|---:|---:|---:|---:|---:|
| 1 | 25/40 | 40/40 | 0.05649 | 0.09894 |
| 2 | 34/40 | 40/40 | 0.05644 | 0.09118 |
| 10 | 32/40 | 39/40 | 0.05716 | 0.08257 |

**Wider credible intervals** explain part of higher coverage; 40/40 is not evidence of population coverage=100%. The true hyperparameter values are inside the prior grid in these runs, an advantageous assumption. Under an off-grid configuration (sigma_walk=.18, sigma_read=.24, bias=.08), 37/40 joint credible intervals covered M0, but the estimate was biased low and mean interval width increased to 0.12421.

### Run the GitHub companion

Python 3.10+, NumPy and SciPy; from repo root:
```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_hierarchical_v101.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v101
```

The GitHub test file contains 24 independently authored regression test methods; **remote GitHub CI has not been run or verified**. The exact 38 locally tested cases and their source are in the local ZIP, and Github source byte-equivalence is not claimed.

- Full Chinese report: `docs/hierarchical_v101_zh.md`
- Model: `models/hierarchical_v101.py`
- Tests: `tests/test_hierarchical_v101.py`
- Numerical summary: `results/hierarchical_v101_summary.json`
- Local validation provenance: `results/test_results_v101.txt`

State-space parameter estimability caveats: https://pmc.ncbi.nlm.nih.gov/articles/PMC4879567/ . HOM uncertainty background: https://doi.org/10.1364/AO.49.002173 .
