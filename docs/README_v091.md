# v0.91 — Photon absorption, storage, re-emission and operational identity

Scientific status: Standard Jaynes–Cummings/RWA quantum-optics model, **not a claim that a historical individual photon survives absorption and not a novel QED prediction**.

Basis: |g,1_a,0_b>, |e,0_a,0_b>, |g,0_a,1_b>. Two controlled pi/2-area coupling pulses transfer |a> to -i|e> then to -|b>. The photonic field occupation is 1 -> 0 -> 1; atomic excitation is 0 -> 1 -> 0; total excitation remains one under RWA. The commutator relations are also verified in an 8D truncated atom x mode-a x mode-b Fock space to avoid relying only on the trivial one-excitation sector.

Related checks: amplitude-damping Kraus completeness; coherent transfer with an uncoupled reference mode; non-observability of a fully decoupled auxiliary historical identity label.

Dependencies: Python 3.10+, NumPy, SciPy.

```bash
python -m unittest discover -s tests -p 'test_absorption_emission_v091.py' -v
python -m experiments.run_v091
```

Files: `docs/absorption_reemission_v091_zh.md`, `models/absorption_emission_v091.py`, `tests/test_absorption_emission_v091.py`, `experiments/run_v091.py`, `results/absorption_emission_v091_summary.json`, `results/test_results_v091.txt`.

**Reproducibility:** Full exact tested source/49 verbose unittest log and SHA-256 list are in the local `photon_v091_complete.zip`. The GitHub model/tests are independently authored matching versions; remote GitHub CI has not been run and byte-for-byte identity with the local code is not claimed.
