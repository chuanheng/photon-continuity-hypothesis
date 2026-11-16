# PCH-A v1.07 — Two-photon rho reference and general three-photon Gram counterexample

**Status:** All results are SYNTHETIC standard quantum-optics/statistics; no individual permanent photon history observable or new QED effect.

The real research goal is to resolve the v1.06 error source: fitting partially distinguishable three-boson contamination as fully indistinguishable can catastrophically bias intrinsic HOM mode overlap. v1.07 adds an independently prepared, ideally calibrated pairwise HOM reference with coincidence likelihood C ~ Binomial(N_ref,(1-rho)/2), rho = |<phi|psi>|² and a Uniform(0,1) prior, and propagates the reference-count posterior into the main near/far optical Bayesian inference.

This rho interpolation assumes **two identical internal-mode phi photons entering the same spatial port, plus one psi photon in the other**. It does NOT characterize general pure three-photon internal states.

Original local full-model execution, **44/44 tests passed**, 100 independent primary physical synthetic datasets each fitted under 6 scenarios (600 paired inferences), 160 importance particles, 25 SHA-256 verified research files, 3 PNGs and detailed Chinese report.

| Independent rho reference | Mean fitted M0 (truth .72) | RMSE | Fixed-truth 95% credible interval coverage |
|---|---:|---:|---:|
| Wrong fixed rho=1 | .4652 | .2640 | **4/100** |
| None; jointly infer rho | .5955 | .1407 | 89/100 |
| 100 ideal shots | .6891 | .0780 | 95/100 |
| 1,000 ideal shots | .6990 | .0754 | 96/100 |
| 10,000 ideal shots | .6996 | .0742 | 96/100 |
| Oracle rho=.10 | .6992 | .0741 | 96/100 |

The reference and main source MUST share the identical prepared internal photon modes; calibration beam splitter losses, dark clicks, timing and source contamination are ideally assumed removed. No claim of an actual optical experiment, exact fixed-truth 95% population coverage, fully unbiased estimation, or prior-average SBC. The **same 100 primary physical datasets** are shared across six fits, NOT 600 independent experiments.

**Full general Gram counterexample:** Two valid pure three-photon internal-state Gram matrices with *all three pairwise overlap squares equal .25* but triad phase 0 vs pi/2 give different port occupation probabilities [.2,.3,.3,.2] vs [.175,.325,.325,.175]. Pairwise squared HOM overlaps alone do not determine general three-body interference.

## Code and provenance

- `docs/rho_gram_v107_zh.md`: detailed Chinese report
- `models/gram_v107.py`: arbitrary three-photon internal pure-state Fock creation operators
- `models/rho_reference_v107.py`: **GitHub simplified known-nuisance companion** for independent rho reference (not full local state-space/PNR)
- `tests/test_v107.py`: 22 GitHub companion regression methods; remote CI NOT verified
- `experiments/run_v107.py`: run simplified independent companion
- `results/rho_gram_v107_summary.json`: numbers from full locally executed synthetic model
- `results/test_results_v107.txt`: actual 44 local test provenance

**Exact full research package:** `photon_v107_complete.zip`, SHA-256
`6badebe6888aae6d076f255f48f5be3a601109c6670ce71deaea2ea3b0b95d07`.

The package contains exact local code, 44 successful tests, 600 individual fits, 25 verified content files and 3 figures. GitHub code was authored separately and is **not byte-identical** to the full local model; GitHub CI has **not** been confirmed.

Run GitHub subset from repo root (Python 3.10+, NumPy, SciPy):
```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_v107.py' -v
python -m experiments.run_v107
```

Relevant published research: https://www.nature.com/articles/s41377-026-02250-4 ; https://doi.org/10.1088/2058-9565/adecbc . Next v1.08: calibration transfer mismatch and a test of triad phase using true three-photon observables.
