# Photon Continuity Hypothesis | 光子连续存在假说

**Author / 作者:** Chuanheng Wang（王传恒）, Independent Researcher  
**Status:** Working research draft v0.1 (2026-11-11). **Speculative, unverified, and not peer reviewed.**

An open research workspace for a conjecture that putatively persistent incident photons may transfer energy to matter while retaining a continuing identity and forward propagation direction. The conjecture **departs from established quantum electrodynamics**. This repository aims to formulate mathematical predictions, test conservation constraints and design falsifiable experiments—not to claim the hypothesis has been proven.

本项目公开整理“光子连续存在假说”的假设、数学模型、模拟代码和可证伪实验提案。**目前没有支持该假说的实验验证；现有光电吸收和散射理论已得到广泛实验证实。**

## Contents / 项目结构

- [English working preprint](paper/preprint.md) — scientific scope, derivation, proposed tests and limitations.
- [中文假设清单](docs/hypotheses_zh.md) — author's hypotheses and unresolved questions.
- [Proposed X-ray experiment](experiments/protocol.md) — energy-resolved transmission test and controls.
- [Python toy simulation](models/attenuation.py) — reproducible, illustrative Monte Carlo; **not a validated transport code**.
- [Exact forward-target kinematics](docs/bound_target_kinematics_zh.md) — conservation constraints and composite-target excitations.
- [Standard scattering baseline](docs/standard_scattering_baseline_zh.md) — NIST coefficients, dynamic structure factor, and falsifiable extra-signal criteria.
- [Reference baseline code](models/standard_baseline.py) — NIST-based uncollided flux only.
- [Synthetic spectral identifiability study](docs/spectral_identifiability_zh.md) — likelihood and nuisance degeneracy, **not real experimental data**.
- [Synthetic spectral analysis code](models/spectral_discrimination.py) — self-contained Poisson counting demonstration.
- [Photoelectric absorption challenge (中文)](docs/photoelectric_absorption_zh.md) — energy accounting, alternative final states and the identity problem.
- [Photoelectric energy-budget toy code](models/photoelectric_energy_budget.py) — simplified bookkeeping, **not a physical emission model**.

## Mathematical starting point

Standard uncollided narrow-beam attenuation: `N_u(x) = N_0 exp(-μx)`.

Alternative toy model: `K ~ Poisson(λx)`, `E_K = E_0(1-α)^K`, giving `E[E(x)] = E_0 exp(-λαx)`.

**These formulas describe different observables.** An exponential shape does not demonstrate photon survival. λ and α are unmeasured toy parameters, not inferred from μ.

## Run the toy simulation

```bash
python3 models/attenuation.py
```

Run tests with `python3 -m unittest discover -s tests -v` (Python standard library only). Tests check mathematical implementation, **not the truth of the hypothesis**.

Requires Python 3 standard library only. Produces `results.csv` (ignored by Python .gitignore where applicable).

## Research priorities

1. Compare with full standard X-ray interaction spectra, not only uncollided flux.
2. Formulate energy/momentum-conserving microscopic transitions.
3. Define measurable observables that distinguish the hypothesis from standard predictions.
4. Specify a priori falsification criteria and detector sensitivity.
5. Invite critical peer feedback and independent reproduction.

## Sources

- [NIST X-ray attenuation theory](https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html)
- [NIST Aluminum coefficients](https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z13.html)
- [NIST XCOM](https://www.nist.gov/pml/xcom-photon-cross-sections-database)

## Attribution and licensing

The repository's existing MIT LICENSE governs code; paper and documentation licensing will be clarified in a separate version. Please cite a specific commit or eventual archival DOI. A DOI records a public version, **not scientific endorsement**. Contributions and critical review are welcome.

## Direction A (v0.9)

The working research direction retains the **permanent-original-photon postulate as a hypothesis**, not an established fact. See [Chinese postulates and falsifiability constraints](docs/direction_a_postulates_zh.md) and [mathematical sequence demonstrations](models/persistence_sequences.py). The mathematical positivity of finite-step energy sequences does not establish photon persistence in nature.
