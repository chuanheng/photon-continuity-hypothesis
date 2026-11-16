# v0.96 — Genuine three-boson Fock splitting and externally monitored HOM calibration

**Physics:** The ideal 50:50 beam splitter transforms |2,1> into probabilities (3/8,1/8,1/8,3/8) across output |0,3>,|1,2>,|2,1>,|3,0>. Three mutually distinguishable photons instead give (1/8,3/8,3/8,1/8). The model uses actual bosonic Fock amplitudes, not the distinguishable-photon approximation of v0.95.

**Synthetic, no actual optical measurements:** The corrected statistical fit includes an explicitly ideal five-class photon-number-resolving source monitor (recognizes |2,1> contamination), a matched-electronic-trigger no-light monitor for correlated clicks, and an **exact, noise-free oracle** measurement of the complete environmental drift path.

**Two distinct estimands** are the experiment-period average optical overlap and the intrinsic zero-drift overlap M0. A near/far optical-only experiment with free (Mbar,triplet fraction,extra click probability) has a rank-deficient 2x3 Jacobian; independent calibration is essential.

**Local complete, actually executed package**: photon_v096_complete.zip — 44/44 successful Python tests, source code, 60 outer datasets with 99 refit bootstraps each, complete numerical JSON, figures and SHA-256 verified manifest. Truth M0=.72; average calibrated estimate .722060 and older misspecified estimate .531165; 57/60 nominal 95% intervals covered M0 and 57/60 covered the experiment-period mean. The exact 95% binomial uncertainty interval for 57/60 is ~[.8608,.9896].

**Scientific limitation:** Source PNR monitoring and perfect environmental phase sensing are strong assumptions, not properties of ordinary threshold optical detectors. This analysis does NOT establish a permanent historical photon identity or a novel QED prediction.

**Repo counterpart** (independently authored, NOT byte-identical; remote CI NOT verified): 
```bash
python -m pip install numpy scipy
python -m unittest discover -s tests -p 'test_fock_calibration_v096.py' -v
python -m experiments.run_v096
```

Research: docs/fock_calibration_v096_zh.md, model: models/fock_calibration_v096.py, regression: tests/test_fock_calibration_v096.py, results: results/fock_calibration_v096_summary.json. The full local ZIP contains 44 actual test cases; the GitHub regression suite contains 31 tests which have not been separately executed on GitHub.

References: USC EE539 Fock states https://bpb-us-w1.wpmucdn.com/sites.usc.edu/dist/e/127/files/2024/08/EE_539_Primer-2.pdf ; multi-photon coalescence in an optical tritter (distinct geometry) https://doi.org/10.1038/ncomms2616 .
