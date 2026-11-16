# v0.79 — Nuisance-parameter identifiability

A three-outcome interferometer model with loss, dephasing, normalized dark-count background, phase drift, and a hypothetical identity-dependent phase shift. Without an independently justified differential intervention, identity phase δ and ordinary phase β are perfectly confounded. A mathematical switch z∈{0,1} can lift degeneracy in a toy model; no physical identity switch is established.

Requires Python 3.10+ and numpy. From the GitHub repository root:

```bash
python -m unittest discover -s tests -p 'test_identifiability_v079.py' -v
python -m experiments.run_v079
```

Documents: `docs/identifiability_v079_zh.md`. Code: `models/identifiability_v079.py`. Output: `results/identifiability_v079.json`. Local development folder ran 25 tests successfully (0.012 seconds); no GitHub CI run is claimed.

The full local package includes expanded Chinese report and the actual unittest log: `photon_v079_complete.zip`.
