# PCH-A v1.05 — Joint-prior multi-parameter HOM SBC + robust sensor heldout predictions

**Science status:** Conventional synthetic quantum-optics/statistical research only. No actual photon measurements, independent permanent-photon-history evidence, or novel QED prediction.

v1.04 formally SBC-validated only a one-dimensional known-optics binomial submodel. v1.05 goes further: define a *matched joint prior and data-generating mechanism* covering intrinsic overlap M, source triplet fraction r, two PNR misclassification rates, electronically correlated coincidences q, detector efficiencies and dark clicks, plus latent Gaussian phase walk/readout parameters. The source PNR report probability is `r*(1-alpha)+(1-r)*beta`, so source pollution and misclassification are coupled through the same observation. The near/far HOM likelihood further reweights optical and environmental nuisance particles.

Physical model: ideal 50:50 beamsplitter and standard bosonic Fock |2,1> near-simultaneous triplet split probabilities (3,1,1,3)/8; far-delay fully distinguishable split (1,3,3,1)/8. Five photon-number input event families, threshold detectors, and a specified per-gate matched-electronics extra-click model. Actual prepared independent standards and trusted detector references are assumed available; arbitrary partial triplet indistinguishability, dead time and higher photon numbers are not included.

**Locally executed results (complete ZIP `photon_v105_complete.zip`):**
- **40/40 Python unittest methods passed.**
- 450 true prior-predictive joint simulations, 850 nuisance/proposal particles and 49 joint posterior draws per dataset.
- Intrinsic HOM M: **428/450** (95.11%) of nominal Bayesian 95% equal-tail credible intervals covered their prior-sampled true M. Exact-binomial 95% uncertainty interval [92.69%, 96.91%].
- All 12 tracked marginal SBC rank uniformity chi-square p-values exceeded 0.05 in 10-bin diagnostics (M p=0.4771). Not mathematical proof of unbiased or exact posterior sampling, not fixed-truth coverage and NOT real optical system validation.
- Median particle ESS **582.41/850**.
- Separate robust zero-phase sensor experiment with 100 training and 80 heldout readings per dataset, 180 datasets per condition: Student-t(df=4) minus Gaussian mean heldout predictive log-score **−0.0241** on pure Gaussian (Student-t wins 17/180); **+0.4187** under 8% Gaussian-mixture contamination in BOTH train and heldout (Student-t wins 180/180).

**Important scope:** The Student-t comparison is a separate *zero-phase sensor reference* predictive submodel. The FULL HOM state-space posterior has NOT been reimplemented with Student-t transitions/observations or SBC-audited for that robust model. The finite 27-value phase hyperprior and numerical integration grids are restricted, intentionally matching the synthetic prior generator.

## GitHub counterpart

These GitHub text files were independently authored companions to the exact locally tested project, not byte-for-byte copies; GitHub Actions CI has NOT been verified.

- `docs/full_sbc_robust_v105_zh.md` — detailed Chinese methods report
- `models/full_sbc_v105.py` — joint-prior generator, coupled PNR source calibration and approximate posterior
- `models/robust_sensor_v105.py` — robust heldout sensor scoring
- `tests/test_v105.py` — **27 independent GitHub regressions**, not the 40 local tests
- `experiments/run_v105.py` — regeneration
- `results/full_sbc_v105_summary.json` — validated local numerical highlights
- `results/test_results_v105.txt` — exact local provenance

Run GitHub counterpart (Python 3.10+, NumPy, SciPy):
```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_v105.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v105
```

The exact **LOCAL ZIP** also contains `results/full_sbc_v105.json` with all 450 rank records, `results/robust_sensor_v105.json` with all 360 sensor comparisons, three original PNG plots, original sources, a SHA-256 file manifest, and 40-case actual unittest log. ZIP SHA256: `8ec24b75bd67f011d2c2ca11b95a53a2668a5df9696468885721d0ed2264df9c`.

References: Stan SBC https://mc-stan.org/docs/stan-users-guide/simulation-based-calibration.html ; imperfect-photon HOM https://doi.org/10.1103/PhysRevLett.126.063602 .

Next v1.06: off-prior/noise misspecification stress, a continuous phase hyperprior, more realistic partially distinguishable triplets, and actual instrument identifiability requirements.
