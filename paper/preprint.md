# A Testable Toy Model for a Photon-Continuity and Discrete Energy-Transfer Hypothesis

**Chuanheng Wang** — Independent Researcher  
**Working preprint v0.1 — 2026-11-11**  
**Speculative; not peer reviewed; no experimental validation claimed.**

## Abstract

We formulate an exploratory photon-continuity conjecture: an incident photon retains a putative identity and forward direction while transferring positive fractions of energy to matter. A simple stochastic model is compared with conventional exponential attenuation of the uncollided X-ray component. We derive a mean-energy law, propose energy-resolved tests, and identify open issues involving conservation laws, photon indistinguishability, coherent optics and background-photon dynamics. The attenuation law does not establish photon survival after absorption.

## 1. Motivation and status

In standard radiation transport, the uncollided monoenergetic narrow-beam component satisfies N_u(x)=N_0 exp(-μx). Photoelectric absorption removes an incident photon excitation; Compton scattering generally changes photon energy and direction. A declining detector count alone cannot distinguish absorption from sub-threshold energy transfer. Our alternative conjecture is not established by existing measurements.

## 2. Hypotheses

H1: incident-photon persistence is postulated. H2: putative surviving excitations preserve their original direction and speed c. H3: conditional energy-transfer events leave strictly positive energy after each finite event. H4: matter may transfer energy to a hypothesized reservoir of pre-existing low-energy photons. H5: operational meaning of original-photon identity and information retention remains unresolved.

## 3. Stochastic toy model

Let K(x) follow a Poisson distribution with mean λx. Each event removes fraction α of the current energy, with 0<α<1. Then

E_K = E_0 (1-α)^K > 0,

and

⟨E(x)⟩ = E_0 exp(-λαx).

The zero-event probability is exp(-λx). The superficial similarity to Beer–Lambert attenuation does not identify mechanisms or imply λ=μ. λ and α are **free toy parameters**, not measured physical constants. Energy-dependent rates, material recoil and a quantum-consistent interaction rule are not yet supplied.

## 4. Reference scenario

For 60 keV incident photons and aluminum of density about 2.699 g/cm³, NIST tabulates μ/ρ≈0.2778 cm²/g, giving μ≈0.7498 cm⁻¹. This provides a standard uncollided-flux reference only. No inference about toy-model λ or α follows from it.

## 5. Experimental proposal

Use a characterized quasi-monochromatic X-ray beam, aluminum samples of multiple thicknesses, energy-resolving transmission detectors, angular scans and blank controls. Compare measured spectra to a **full** standard-physics prediction including photoelectric absorption, coherent and incoherent scattering, secondary radiation and instrument response. Pre-register a concrete alternative signal and its parameter range before collecting data. An unexplained low-energy count alone does not establish original-photon persistence.

## 6. Falsification and limitations

A specified extra forward degraded-energy component may be excluded by sufficiently sensitive null results. An unrestricted assertion that all surviving photons become arbitrarily undetectable is not falsifiable in this setup. The model lacks a microscopic Hamiltonian, momentum accounting, operational photon-identity definition and explanations for coherent reflection, refraction, polarization, dispersion and thermodynamics. It is **not** a complete competing theory of radiation transport.

## 6a. A conservation-law obstruction for free electrons

Suppose an incident photon of energy E exits with energy E'=E-Δ in exactly the same direction, with Δ>0. The target must receive energy Δ and momentum Δ/c in that direction. For a free electron initially at rest, its recoil kinetic energy would be

T = sqrt((m_e c²)² + Δ²) - m_e c².

Energy conservation requires T=Δ, which implies 2 m_e c² Δ=0 and therefore Δ=0. Thus **nonzero strictly forward energy loss to a single initially stationary free electron is forbidden** for this two-body final state. A material with internal excitations and collective recoil may have different kinematics, but requires an explicit final state and transition dynamics. See [Chinese derivation](../docs/conservation_zh.md). This constraint is a challenge to, not a confirmation of, the conjecture.

## 6b. Operational distinguishability

An energy-resolved detector measures outgoing excitations, not a persistent label identifying a specific incident photon. The proposed test therefore constrains **parameterized additional spectral components**, not the metaphysical persistence of an individually labeled photon. The latter needs an operational definition to become testable.

## 7. Next steps

Replace the uncollided-only baseline with cross-section-based transport; include detector response and uncertainty; derive conservation-consistent dynamics; invite independent critique before any radiation experiments.

## References

- NIST, X-Ray Mass Attenuation Coefficients: https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
- NIST, Aluminum (Z=13): https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z13.html
- NIST, XCOM: https://www.nist.gov/pml/xcom-photon-cross-sections-database
