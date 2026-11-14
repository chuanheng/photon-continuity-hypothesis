# PCH-A v1.06 — Continuous hyperprior and restricted partially distinguishable triplets

All numerical observations are synthetic standard quantum optics. This does not provide evidence for a permanently surviving historical individual photon.

**Main result:** Under the explicitly restricted Fock input |2_phi,1_psi>, where two photons share internal mode phi and the third has squared overlap rho with phi, the ideal 50:50 output occupation distribution is rho*(3,1,1,3)/8 + (1-rho)*(1,3,3,1)/8. This interpolation is NOT generic three-photon Gram-matrix physics.

Local actual execution: **43/43 tests passed**, 500 fixed-M0 synthetic outer datasets, 21 research source/result files independently SHA-256 validated inside the ZIP, 3 numerical PNGs. Genuine M0=.72. In 100 paired trials with true rho=.1 and larger triplet pollution, incorrectly assuming rho=1 gave estimated M0 mean .4496 and 95%-interval coverage **4/100**; externally oracle-known true rho=.1 gave mean .6974 and **94/100**. The latter is NOT rho estimation from these HOM data. The near/far Jacobian for (M0,rho) has rank one, so independent optical-mode reference data is essential.

A fixed-truth off-support phase sensor study had 94/100 coverage but mean interval width .423 and hyperproposal median ESS 23.5/160, vs width .255 and ESS 104/160 for matched model; high coverage can obscure weak information. A separate 8% outlier stress is not a general robustness proof. None of this is full joint-prior SBC; v1.05 tested a different matched restricted generative prior model.

Full actual local package: photon_v106_complete.zip; SHA256:
700f92e96730aaf733fc7bb05126fc420e841cae9e076b33030f7010b2e6006f

GitHub companion files are **independently authored**, not byte-identical to exact locally executed sources, and remote CI is NOT confirmed. To execute the GitHub companion from repository root (Python 3.10+, numpy/scipy):

```bash
python -m pip install numpy scipy
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -p 'test_continuous_partial_v106.py' -v
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v106
```

Paths: docs/continuous_partial_v106_zh.md; models/continuous_partial_v106.py; tests/test_continuous_partial_v106.py; experiments/run_v106.py; results/continuous_partial_v106_summary.json; results/test_results_v106.txt.

Background: https://arxiv.org/abs/1410.1506 and https://mc-stan.org/docs/stan-users-guide/simulation-based-calibration.html
