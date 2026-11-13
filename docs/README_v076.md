# v0.76 reproduction
Requires Python 3.10+ and numpy.

From repository root:
```bash
python -m unittest discover -s tests -p 'test_eft_identity_v076.py' -v
python -m experiments.run_v076
```

The model file is `models/eft_identity_v076.py`; the tests are `tests/test_eft_identity_v076.py`. The original local research folder also contains `test_results.txt` and a zipped archive linked in the research discussion.

The model consists of two **separate** checks: a classical neutral-scalar EFT operator that is gauge invariant, and a truncated finite-mode Hamiltonian that preserves a carrier charge but **does not implement QED gauge invariance**. Do not conflate them or claim they prove permanent photon identity.
