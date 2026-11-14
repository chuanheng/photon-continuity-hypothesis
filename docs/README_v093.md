# v0.93 — HOM interference of exponentially emitted single-photon wavepackets

This version extends v0.92 Wigner–Weisskopf emission modes into ideal two-single-photon Hong–Ou–Mandel interference. It calculates squared mode overlaps, 50:50 beamsplitter coincidence probabilities, and ensemble averages for Gaussian arrival-time and frequency jitter with pairwise source correlations.

**Scientific status:** Standard quantum optical mode-interference model. No original photon persistence, new QED interaction or uniquely identifying historical photon label has been shown. Genuine internal optical modes (including polarization) DO change HOM interference; a purely decoupled spectator historical label does not.

Ideal single photon pair: P(coincidence)=(1-|<xi1|xi2>|^2)/2. Some literature reports normalized HOM coincidences as 1-M instead: do not confuse those conventions. The Gaussian noise factorization assumes independence of relative time and relative spectral fluctuations. An optional random-port background fraction is a phenomenological approximation, not a complete detector likelihood.

Dependencies: Python 3.10+, numpy, scipy (matplotlib for figures in the full local ZIP).

Run from repository root:

```bash
python -m unittest discover -s tests -p 'test_hom_wavepackets_v093.py' -v
python -m experiments.run_v093
```

GitHub files: `docs/hom_wavepackets_v093_zh.md`, `models/hom_wavepackets_v093.py`, `tests/test_hom_wavepackets_v093.py`, `experiments/run_v093.py`, `results/hom_wavepackets_v093_summary.json`, `results/test_results_v093.txt`.

The complete LOCAL package `photon_v093_complete.zip` contains the exact **40/40 locally executed tests**, mathematical report, 121-point HOM delay scans, 81-point correlation jitter scans, two PNG figures, original JSON results and a SHA-256 manifest. GitHub copies were separately authored and have not been tested in remote CI.

References: NIST IR 8486 https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf and Drago–Branczyk (2024) https://doi.org/10.1139/cjp-2023-0312.
