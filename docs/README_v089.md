# v0.89 — Informationally complete multitime process test

A finite two-step qubit model compares a reused hidden bit to freshly sampled bits. Both models have the same one-step channel but different multitime statistics. A correctly relabeled hidden variable does not change any statistics.

16 intermediate rank-one Kraus CP branches span the qubit-operation Choi Hermitian space (rank 16); 4 terminal rank-one effects span qubit Hermitian effects (rank 4). Their 64 probabilities define an informationally complete linear tester for **fixed initial state with one intermediate intervention**.

This is an ordinary environmental memory example from known process-tensor methods, not evidence for historical individual photons or new QED.

Python 3.10+, NumPy; run from repository root:

```bash
python -m unittest discover -s tests -p 'test_process_access_v089.py' -v
python -m experiments.run_v089
```

Local full package: [conversation download photon_v089_complete.zip]. Local Python actually ran 33/33 tests in 0.028 sec. GitHub CI has not been run or verified.

Files: docs/multitime_access_v089_zh.md; models/process_access_v089.py; tests/test_process_access_v089.py; experiments/run_v089.py; results/process_access_v089_summary.json; results/test_results_v089.txt.

References: https://doi.org/10.1103/PhysRevLett.120.040405 and https://doi.org/10.1103/PRXQuantum.2.030201 .
