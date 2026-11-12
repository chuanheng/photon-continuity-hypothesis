"""Exact relativistic forward two-body kinematics, using energy units (keV).

Initial target is at rest, with rest energy R=M*c^2. Its final invariant
rest energy is R+U, where U is internal excitation energy.
Photon direction is exactly unchanged. Kinematics alone does not imply
a nonzero interaction amplitude or cross section.
"""
from math import sqrt

ELECTRON_REST_KEV = 510.99895000
PROTON_REST_KEV = 938272.08816


def forward_energy_loss(rest_energy_kev: float, excitation_kev: float) -> float:
    """Exact positive photon energy loss for a target initially at rest.

    Derived from (R+delta)^2 - delta^2 = (R+U)^2.
    Returns delta = U + U^2/(2R). The process requires E_in > delta.
    """
    if rest_energy_kev <= 0 or excitation_kev < 0:
        raise ValueError("rest energy must be positive and excitation nonnegative")
    return excitation_kev + excitation_kev**2 / (2 * rest_energy_kev)


def final_photon_energy(incident_kev: float, rest_energy_kev: float,
                        excitation_kev: float) -> float:
    if incident_kev <= 0:
        raise ValueError("incident photon energy must be positive")
    loss = forward_energy_loss(rest_energy_kev, excitation_kev)
    if loss >= incident_kev:
        raise ValueError("final photon energy must be positive")
    return incident_kev - loss


def invariant_residual(rest_energy_kev: float, excitation_kev: float) -> float:
    """Energy-squared residual in keV^2; should be near zero."""
    delta = forward_energy_loss(rest_energy_kev, excitation_kev)
    # Stable expression for invariant relation
    return 2 * rest_energy_kev * (delta - excitation_kev) - excitation_kev**2


def compton_scattered_energy(incident_kev: float, theta_rad: float,
                             rest_energy_kev: float = ELECTRON_REST_KEV) -> float:
    """Standard free-electron Compton result for comparison."""
    if incident_kev <= 0 or rest_energy_kev <= 0:
        raise ValueError("energies must be positive")
    from math import cos
    return incident_kev / (1 + (incident_kev / rest_energy_kev) * (1 - cos(theta_rad)))


if __name__ == "__main__":
    from math import pi
    r = PROTON_REST_KEV
    u = 0.001  # 1 eV internal excitation, illustrative hypothetical target
    delta = forward_energy_loss(r, u)
    print(f"Forward inelastic target: U={u*1000:g} eV, photon loss={delta*1000:.12g} eV")
    print(f"Standard free-electron Compton at 0 degrees: {compton_scattered_energy(60, 0):g} keV")
    print(f"Standard free-electron Compton at 90 degrees: {compton_scattered_energy(60, pi/2):.6f} keV")
