# PCH-A v1.04 — Rigorous restricted SBC and out-of-sample model checks

This release audits the statistical machinery used in a conventional HOM quantum-optics simulation. It does NOT provide any experimentally identifiable permanent historical photon labels.

**Three separate audits — do not conflate them:**
1. **Formal prior-predictive SBC only for an explicitly specified one-parameter binomial optical submodel**: M~Uniform(0,1), k~Binomial(280,0.25−0.17×0.76×M). 450 replicate joint prior simulations, 49 posterior draws each. Results: 430/450 nominal 95% credible intervals covered their sampled truths; 10-bin rank chi-square p=0.19633. This does NOT validate the full v1.03 HOM detector/source/phase model.
2. **Held-out predictive check of the complex sensor hypermodel**, using only the first 70 of 100 zero-reference sensor readings for inference and testing extreme (>3sigma) tail events on the final 30. 75 ordinary Gaussian cases flagged 6/75 at diagnostic threshold <=.05; 75 cases with deliberately added 9% corruption ONLY IN THE HOLDOUT flagged 51/75. This controlled train/test shift does NOT establish the detection rate of general real sensor faults.
3. **Hyperparameter proposal scale sensitivity** in 32 paired fixed-truth synthetic full-HOM datasets, 90 proposal particles each: scales .8, 1.4, 2.2 led to median ESS 64.54, 59.17 and 19.86. All three settings had mean M0 estimates close to .717. ESS is a numerical diagnostic, not an SBC result.

**Actual local research package:** `photon_v104_complete.zip`, 21 SHA-256 validated research content files plus manifest, **34/34 actually passed Python unit tests**, complete 450-replicate rank data, 150 heldout predictive data sets, 32 paired proposal tests, three PNG diagnostic plots, and a full Chinese research report.
ZIP SHA-256: `f4daa44e20b00d42eb8abffbf1c8915c1225c964030d88c78a55486203b069ea`.

**GitHub counterparts** of the model and its 20 separate regression tests are independently authored; they are NOT byte-identical to the actually tested source and remote GitHub CI has NOT been verified.

Run from repository root (Python >=3.10, numpy, scipy):
```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_validation_v104.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v104
```

- Full Chinese report: `docs/validation_v104_zh.md`
- Corresponding model: `models/validation_v104.py`
- Regression: `tests/test_validation_v104.py`
- Run: `experiments/run_v104.py`
- Numeric summary: `results/validation_v104_summary.json`
- Local run provenance: `results/test_results_v104.txt`

Next: v1.05 should establish a completely matched joint-prior generative process for full-model SBC and challenge both training and holdout data with non-Gaussian errors.

Methodology: https://mc-stan.org/docs/stan-users-guide/simulation-based-calibration.html and https://quantitative.emory.edu/documents/Bayesian_Workflow_article_Gelman.pdf .
