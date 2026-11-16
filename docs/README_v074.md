# v0.74 – Gauge redundancy, Gauss constraints, identity labels

This version includes a three-qubit Z2 lattice gauge toy example: two matter qubits and one gauge link.

Files:
- `docs/gauge_redundancy_v074_zh.md` – Chinese research writeup
- `models/gauge_redundancy_v074.py` – full numerical model
- `tests/test_gauge_redundancy_v074.py` – 33 independent unit tests
- `experiments/run_study_v074.py` – experiment script
- `results/gauge_redundancy_v074.json` – numerical summary

Dependencies: Python 3.10+, numpy.

From repository root:

```bash
python -m unittest discover -s tests -p 'test_gauge_redundancy_v074.py' -v
python experiments/run_study_v074.py
```

Locally executed: 33 passed. The repository's tests were not independently executed by GitHub Actions.

This is NOT a derivation from quantum electrodynamics, nor evidence that a photon has a permanent identity label.
