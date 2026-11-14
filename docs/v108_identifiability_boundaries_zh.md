# v1.08 — Identifiability boundaries and three-photon phase (2026-11-14)

**Status:** Independent mathematical toy-model study. Not a re-run of v1.07's 600 paired inferences; the underlying v1.07 dataset/code was not present on the repository default branch when this report was written. Not experimental validation of permanent photon identity.

## 1. Product degeneracy and independent calibration

Let X~Binomial(n, theta*q), Y~Binomial(m,q), independent, with interior theta,q in (0,1). The main experiment only determines theta*q. Define p=theta*q and f=n/[p(1-p)]. The joint Fisher information for (theta,q) is

I = [[f*q^2, f*theta*q],
     [f*theta*q, f*theta^2 + m/(q*(1-q))]].

For m=0, det(I)=0: there is a continuous nonidentifiability direction theta*q=constant. For m>0, det(I)=f*q^2*m/[q*(1-q)]>0, restoring local identification **within this toy model**.

With theta=0.7, q=0.8 and n=1000:
| reference m | smallest Fisher eigenvalue | sqrt((I^-1)[theta,theta]) |
|---:|---:|---:|
| 0 | 0 | undefined/infinite |
| 100 | 332.777713 | 0.040125 |
| 1000 | 1795.704080 | 0.022528 |
| 10000 | 2514.057308 | 0.019931 |

These are analytic information bounds, **not empirical RMSE or posterior coverage rates**. The m->infinity limit of the theta standard-deviation bound is sqrt(p*(1-p)/n)/q, approximately 0.01962.

## 2. Transfer error between experiments

If main experiment uses q_main but independent calibration measures q_ref, while the model incorrectly equates them, the asymptotic fitted theta is theta_true*q_main/q_ref (provided the solution remains in the parameter domain).

For theta_true=0.7 and q_main=0.8:
| q_ref-q_main | asymptotic estimate | bias |
|---:|---:|---:|
| -0.05 | 0.746667 | +0.046667 |
| 0 | 0.700000 | 0 |
| +0.05 | 0.658824 | -0.041176 |

Thus extra reference counts cannot remove *systematic transfer mismatch*. Realistic joint inference must explicitly model/validate whether the two setups share the nuisance parameter.

## 3. Three-photon triad phase counterexample

For normalized pure internal states with Gram matrix G_ij=<phi_i|phi_j>, let each off-diagonal modulus be r=0.3. Choose the product G_12*G_23*G_31=r^3 exp(i Phi). The Gram matrix is Hermitian positive definite for these choices (strict diagonal dominance: 2r<1), and therefore realizable by vectors in a complex Hilbert space. All pairwise **magnitudes** are identical while the triad/Bargmann phase Phi differs.

perm(G)=1+3r^2+2r^3*cos(Phi).

| Phi | permanent |
|---|---:|
| 0 | 1.324 |
| pi/2 | 1.270 |
| pi | 1.216 |

This is a mathematical counterexample to determining all collective interference information from pairwise overlap magnitudes. The Gram permanent alone is **not an arbitrary interferometer's measured probability**; an explicit optical transfer matrix, detector POVM, loss and noise model are required to predict physical observations. Pairwise phase assignments are gauge dependent, while the triad product is gauge invariant.

Existing quantum optics literature has already demonstrated such triad-phase effects; this is **not a novel prediction**:
Menssen et al., *Distinguishability and Many-Particle Interference*, Physical Review Letters 118, 153603 (2017), DOI: https://doi.org/10.1103/PhysRevLett.118.153603 .

## 4. Consequences for the photon-continuity hypothesis

- Independent two-photon references can reduce nuisance uncertainty where the **same calibrated parameter** controls the primary three-photon experiment.
- Reference calibration alone need not identify the collective triad phase or other nonidentifiable parameters.
- Local Fisher rank is not a proof of global identifiability; check parameter symmetries, exact observational equivalence, and boundary cases.
- Nothing here measures persistent photon identity or distinguishes that postulate from standard quantum optics.

## 5. v1.09 action items

1. Implement a specified three-port unitary scattering experiment and detector POVMs; compare full multinomial output distributions, not Gram permanents alone.
2. Compute numerical Jacobian singular values and profile likelihoods across theta, pairwise overlap magnitudes, triad phase and loss.
3. Introduce calibration-to-primary drift delta and compare fitting with/without its hierarchical uncertainty.
4. Test global equivalence classes and pre-register a physically discriminating prediction versus standard quantum optics.
5. Obtain v1.07 simulation files and seeds before attempting numerical reproduction of its claimed coverage and RMSE.

Run: `python3 models/identifiability_v108.py` (Python standard library).
