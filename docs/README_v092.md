# v0.92 — Wigner–Weisskopf multi-mode spontaneous emission

**Science status:** established quantum optics; not QED innovation and not evidence for permanent historical individual photon identity.

Markov approximation: atomic population exp(-Gamma t), emitted probability 1-exp(-Gamma t); ideal temporal mode sqrt(Gamma) exp(-Gamma t/2) Theta(t); Lorentzian spectral FWHM Gamma in angular-frequency units. Ordinary photon modes can have different overlaps without historical identity tags.

A finite **401 mode** Hermitian reservoir model directly propagates the atom+field one-excitation state and conserves probability (max numeric deviation 2.53e-14). Early closed-unitary population decay is quadratic rather than Markov linear in t; finite bandwidth and discrete frequencies impose limitations.

**Local complete ZIP**: photon_v092_complete.zip includes the actual 46-passing-test source, SHA-256 manifest, full 81-point decay and 1001-point spectrum datasets, and figures.

GitHub model/tests are separately authored matching mathematical implementations, not byte-identical copies. Remote GitHub CI has NOT been verified.

Run from repository root, Python 3.10+, numpy, scipy:

```bash
python -m unittest discover -s tests -p 'test_wigner_weisskopf_v092.py' -v
python -m experiments.run_v092
```

Files:
- docs/wigner_weisskopf_v092_zh.md — full Chinese report
- models/wigner_weisskopf_v092.py — Markov + Hermitian finite-mode model
- tests/test_wigner_weisskopf_v092.py — standalone regression suite
- experiments/run_v092.py — numerical data regeneration
- results/wigner_weisskopf_v092_summary.json — audited numeric highlights
- results/test_results_v092.txt — local execution record

References: https://wp.optics.arizona.edu/opti544/wp-content/uploads/sites/54/2021/04/OPTI-544-Lecture-Posted-Friday-04302021.pdf and https://mochizuki-tus.github.io/QM_Textbook_EN/ch60_photons_phonons.html .
