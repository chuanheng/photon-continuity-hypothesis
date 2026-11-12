"""Relativistic thresholds for photon-induced ionization of a stationary atom.

All energies use consistent units with c=1. Electron and ion rest energies
are positive; initial atomic rest energy must be below their sum.
No cross sections, photon identity, or matrix elements are inferred.
"""
import math


def ionization_threshold(atom_rest, ion_rest, electron_rest, successor_energy=0.0):
    """Minimum incident photon energy for a specified outgoing photon energy.

    A + gamma(E) -> ion + electron + gamma'(s), where s>=0.
    Optimizes over final-state angles and momenta. For s>0, the minimum
    occurs for collinear outgoing gamma' and incoming gamma, with final
    ion+electron sharing the same velocity (minimal invariant mass).

    For collinear outgoing photons, (P_i-k')^2=W^2 gives:
    M^2+2*M*(E-s)=W^2, hence E=s+(W^2-M^2)/(2*M).
    This is a global threshold since k_i.k' >=0, and other angles raise E.
    """
    vals=(atom_rest,ion_rest,electron_rest,successor_energy)
    if any(not math.isfinite(x) for x in vals):
        raise ValueError('all inputs must be finite')
    if min(atom_rest,ion_rest,electron_rest)<=0 or successor_energy<0:
        raise ValueError('rest energies must be positive; successor >= 0')
    w=ion_rest+electron_rest
    if w<=atom_rest:
        raise ValueError('ionization must require positive energy')
    # stable expression for (W^2-M^2)/(2M)
    standard=(w-atom_rest)*(w+atom_rest)/(2*atom_rest)
    return standard+successor_energy


def max_successor_energy(incident,atom_rest,ion_rest,electron_rest):
    if not math.isfinite(incident) or incident<=0:
        raise ValueError('incident must be positive and finite')
    return incident-ionization_threshold(atom_rest,ion_rest,electron_rest)


def successor_is_kinematically_allowed(incident,atom_rest,ion_rest,electron_rest,successor_energy):
    if not math.isfinite(successor_energy) or successor_energy<=0:
        return False
    return incident>=ionization_threshold(atom_rest,ion_rest,electron_rest,successor_energy)
