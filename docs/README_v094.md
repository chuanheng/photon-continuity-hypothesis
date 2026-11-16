# v0.94 — Mixed-state HOM and independently calibrated threshold detectors

This is a **synthetic quantum-optics statistical study**, not a new physical theory and not experimental evidence that individual photons have permanent historical identities.

For independent mixed one-photon inputs, ideal two-detector HOM coincidence is `P=(1-Tr(rho1*rho2))/2`. The simulated forward model incorporates four source photon-number classes `(1,1), (2,0), (0,2), (0,0)`, two unequal threshold detector efficiencies, and independent per-gate dark click probabilities.

The key identifiability result is that near-delay coincidence alone cannot separately identify the pair fraction `w11` and overlap `M`; far-delay coincidence plus calibrated nuisance parameters restores local rank in this restricted model. A putative historical identity factor multiplying the overlap is still exactly reproducible using an ordinary mixed optical state.

**Local tested research package:** `photon_v094_complete.zip`
- 52/52 Python unittest checks passed, 16 data/source/research files verified by SHA-256 before archive closure.
- True M = 0.72; one simulated calibrated estimate 0.7239956322.
- Source weights 0.90, 0.04, 0.04, 0.02; efficiencies 0.74, 0.68; dark probabilities 0.002, 0.003.
- Near/far predicted unconditional coincidences 0.0855775488 / 0.2482151125.
- 500-refit-bootstrap 95% percentile interval [0.714096, 0.733751] for the example.
- 120 independent outer simulations with 120 full-refit inner bootstraps each: 114/120 CI coverage of the true synthetic M. Monte Carlo 95% binomial uncertainty interval approximately [0.8943, 0.9814].
- Incorrect ideal inversion of raw unconditioned coincidence gave 0.829275.

Important limitation: the source calibration assumes **independent ideal photon-number-resolving identification** of the four source event classes; ordinary threshold detectors cannot supply it without additional assumptions. The 95% coverage observation only applies under the matching simulated data-generating model.

GitHub model/test files were independently authored for the same mathematical model, not claimed to be byte-for-byte copies of the local package. Local test success does not establish GitHub CI success.

Python 3.10+, NumPy, SciPy:
```bash
python -m unittest discover -s tests -p 'test_mixed_hom_v094.py' -v
python -m experiments.run_v094
```

Detailed report: `docs/mixed_hom_v094_zh.md`. Numerical summary: `results/mixed_hom_v094_summary.json`. Full local ZIP adds detailed outer coverage replicates, original executed test logs, source files, and plots.

Prior research: Drago & Branczyk (2024), https://doi.org/10.1139/cjp-2023-0312 ; Ollivier et al. (2021), https://doi.org/10.1103/PhysRevLett.126.063602 .
