# v0.90 — Gauge-invariant scalar–photon EFT consistency checks

**Scientific status:** Elementary effective-field-theory audit; no claimed new QED prediction, no experimental proof that a historical photon survives absorption and re-emission.

An electromagnetic-neutral complex scalar S can couple through a dimension-six, Lorentz and electromagnetic gauge invariant operator (c6/Lambda^2)|S|^2 F_mu_nu F^mu_nu. Its global U(1)_S conserved charge is not an individual photon's history label.

The two-real-photon contact tensor V^{mu nu}=(k1.k2)g^{mu nu}-k2^mu k1^nu is transverse on both legs; the model checks symbolic Ward identities, physical polarization sums, Lorentz boosts, operator dimensions and the constant-background photon kinetic term Z=1-4c6|S|^2/Lambda^2. A constant healthy Z does not change the massless free-photon dispersion.

Python 3.10+, NumPy, SymPy. Run from repository root:

```bash
python -m pip install numpy sympy
python -m unittest discover -s tests -p 'test_eft_audit_v090.py' -v
python -m experiments.run_v090
```

Files: docs/eft_audit_v090_zh.md, models/eft_audit_v090.py, tests/test_eft_audit_v090.py, experiments/run_v090.py, results/eft_audit_v090_summary.json and results/test_results_v090.txt.

The **local complete v0.90 ZIP** contains the exact code used in the 39/39 successful local unit tests, complete numeric output and SHA-256 manifest. Repository model/test files are functionally matching authoring of the same tests and were not executed in GitHub Actions; do not claim exact byte-for-byte match or remote CI success.

References: https://doi.org/10.1140/epjc/s10052-025-13879-7 ; https://www.mdpi.com/2218-1997/11/5/134 ; https://web.physics.ucsb.edu/~mark/ms-qft-DRAFT.pdf .
