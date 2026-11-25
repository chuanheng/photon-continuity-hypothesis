# A Testable Toy Model for a Photon-Continuity and Discrete Energy-Transfer Hypothesis

[v7.21 匹配标定](../v712_v721/README.md)　后续两项锗符合实验提供其他入射能量下的散射对照。即使将其理想化为两个精确标定点，仍有在两点消失的普通响应扰动可复现原交叉比。要检验这一解释，需要在原两条线的反冲能窗内独立约束能量与方向的交互。

[v7.02–v7.11 工作论文](../v702_v711/manuscript_zh.md) · [复现](../v702_v711/README.md)。公共能窗的方向交叉比为 1.346，可消去可分离的探测器增益和各入射线的共同强度。加入一个普通的入射线与探测器交互响应参数，可逐格重现四个均值。现有数据不能将这项交互归因于永久光子身份。

[v6.92–v7.01 工作论文](../v692_v701/manuscript_zh.md) · [复现](../v692_v701/README.md)。在 34.5–36.5 keV 固定窗口，以带平均截面衡量，55.791 keV 入射时两台探测器都更接近脉冲近似；54.612 keV 时两台给出不同排序。结果表明上批的低能点排序不能推广至所有探测方向和汇总方法。

[v6.82–v6.91 工作论文](../v682_v691/manuscript_zh.md) · [复现](../v682_v691/README.md)。55.791 keV 的四个点较接近 Born 曲线，54.612 keV 的四个点较接近脉冲近似。两组横坐标和精度不同，局部排序无法外推到完整谱。

[v6.72–v6.81 工作论文](../v672_v681/manuscript_zh.md) · [复现](../v672_v681/README.md)。约 8 keV 的触发阈值裁切高能端，共同尺度则允许普通装置响应精确重现乘性候选信号。八个公开图上点可用于谱形比较；逐事件能量与时间的联合似然仍缺输入。

For current evidence, see the [v6.71 Chinese manuscript and reproduction index](../v662_v671/README.md). The historical preprint follows.

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

## 6b. Inelastic forward scattering on a composite target

The free-electron restriction does **not** extend to every target with internal states. For an initially stationary composite target of rest energy R=Mc² that transitions to an excited invariant rest energy R+U, exact four-momentum conservation for strictly forward outgoing photon gives

(R+Δ)²−Δ²=(R+U)², hence **Δ=U+U²/(2R)**, subject to E_in>Δ.

Thus forward inelastic energy loss is **kinematically allowed** if U>0. Whether it occurs, and with what probability, requires a material-specific interaction matrix element and dynamical structure factor. Such processes are already within conventional scattering theory and do not imply universal photon survival. See [derivation](../docs/bound_target_kinematics_zh.md) and [reference code](../models/forward_kinematics.py).

## 6c. Operational distinguishability

An energy-resolved detector measures outgoing excitations, not a persistent label identifying a specific incident photon. The proposed test therefore constrains **parameterized additional spectral components**, not the metaphysical persistence of an individually labeled photon. The latter needs an operational definition to become testable.

## 7. Next steps

Replace the uncollided-only baseline with cross-section-based transport; include detector response and uncertainty; derive conservation-consistent dynamics; invite independent critique before any radiation experiments.

## References

- NIST, X-Ray Mass Attenuation Coefficients: https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
- NIST, Aluminum (Z=13): https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z13.html
- NIST, XCOM: https://www.nist.gov/pml/xcom-photon-cross-sections-database
