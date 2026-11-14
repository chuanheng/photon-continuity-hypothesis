# v0.95 — HOM uncertainty coverage under model misspecification

**Status:** Synthetic-data statistics, not experimental photon physics. No novel QED claim or original historical-photon identity prediction.

The v0.94 source/detector calibration assumes four photon-event categories, independent online/offline detector clicks, and stationary HOM overlap. We construct three ordinary violations:

1. Illumination-triggered simultaneous extra clicks with probability q=0.014, invisible to separate blocked dark frames.
2. 6.5% unresolved distinguishable *three-photon* contamination, mislabeled as ordinary |1,1> during four-class source calibration. The toy triplet splits binomially because contamination photons are **assumed distinguishable** — this is NOT a three-identical-boson Hong–Ou–Mandel law.
3. Random-walk optical-mode drift, M(t)=M0 exp(-|u_t|), u increments N(0,.095^2), with 40 time blocks.

Each of five scenarios: 60 independently simulated datasets, each with 79 parametric bootstrap replicates **refitting and resimulating all modeled calibrations**. Target M0=.72; nominal 95% interval coverage counts:

- Correct model 55/60 (91.67%).
- Correlated online clicks 0/60.
- Unresolved triplets 0/60.
- Nonstationary mode drift 0/60 **for intrinsic M0**, but **57/60 for experiment-period mean mode overlap**.
- All three mechanisms combined 0/60.

Model-correct 55/60 has large binomial Monte Carlo uncertainty (95% exact interval about 81.6–97.2%). Zero coverage in 60 trials does NOT establish population probability identically zero (upper 95% bound 5.96%).

**Crucial estimand distinction:** The time-averaged mode overlap is not intrinsic zero-drift M0; interval targeting one need not cover the other.

This is a structured stress test, not a proof that any real system has these error rates. It contains no empirical data. Ordinary environmental modes and electronic artifacts do not establish permanent individual photon identity.

From GitHub repository root:
```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_robustness_v095.py' -v
python -m experiments.run_v095
```

GitHub source/regression versions are independently authored for the same model and are **not claimed byte-for-byte identical** to the actual locally tested ZIP. Local complete file `photon_v095_complete.zip` includes full mathematical report, exact 30/30 passing local tests, full 300-dataset result JSON, two figures and SHA-256 verified 16 research files. No GitHub-hosted CI execution is asserted.

Sources: https://doi.org/10.1103/PhysRevLett.126.063602 ; https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8486r1.pdf .
