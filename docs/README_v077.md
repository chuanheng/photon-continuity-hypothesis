# v0.77 — Photon absorption and ordinary memory equivalence

A three-mode single-excitation model (signal a, reference b, material excitation e) plus one ancillary qubit. It implements a reversible a↔e absorption, a controlled material phase, and coherent retrieval.

**Scientific caveat:** the ancillary qubit is NOT evidence that photons have permanently conserved historical identities. Two models related by unitary relabeling of that qubit are operationally indistinguishable.

Requirements: Python 3.10+, numpy.

Run from repo root:

```bash
python -m unittest discover -s tests -p 'test_absorption_memory_v077.py' -v
python -m experiments.run_v077
```

Local full research folder: 31 tests passed (0.029 s); the GitHub version is submitted but not independently CI-verified.

- `docs/absorption_memory_v077_zh.md`
- `models/absorption_memory_v077.py`
- `tests/test_absorption_memory_v077.py`
- `experiments/run_v077.py`
- `results/absorption_memory_v077.json`

References: https://doi.org/10.1080/09500349314551321 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC5020357/
