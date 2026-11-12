"""Exact two-body relativistic kinematics, using energy units with c=1.

Initial: photon E + stationary target rest energy R.
Final: photon E' at angle theta + excited target rest energy R+U.
This tests kinematic permission only, NOT photon identity or scattering rate.
"""
import math

def outgoing_energy(incident, excitation, target_rest, angle_radians=0.0):
    values = (incident, excitation, target_rest, angle_radians)
    if any(not math.isfinite(x) for x in values):
        raise ValueError('all inputs must be finite')
    if incident <= 0 or excitation < 0 or target_rest <= 0:
        raise ValueError('incident and target rest energy positive; excitation nonnegative')
    if not 0 <= angle_radians <= math.pi:
        raise ValueError('angle must be in [0, pi]')
    numerator = target_rest * (incident - excitation) - excitation**2 / 2
    if numerator <= 0:
        raise ValueError('no strictly positive outgoing photon energy for this excitation')
    denominator = target_rest + incident * (1-math.cos(angle_radians))
    return numerator / denominator

def recoil_energy(incident, excitation, target_rest, angle_radians=0.0):
    outgoing = outgoing_energy(incident, excitation, target_rest, angle_radians)
    return incident - excitation - outgoing

def invariant_residual(incident, excitation, target_rest, angle_radians=0.0):
    """Return (P_target_final)^2 - (R+U)^2 in squared energy units.

    Factorization reduces catastrophic cancellation for a heavy target.
    """
    outgoing = outgoing_energy(incident, excitation, target_rest, angle_radians)
    return ((incident - outgoing - excitation) *
            (2*target_rest + incident - outgoing + excitation)
            - (incident**2 + outgoing**2 - 2*incident*outgoing*math.cos(angle_radians)))

if __name__ == '__main__':
    for angle in (0, math.pi/2, math.pi):
        out = outgoing_energy(60, 40, 25_000_000, angle)
        print(f'angle={angle:.5f} rad, outgoing={out:.9f} keV, recoil={recoil_energy(60,40,25_000_000,angle):.9f} keV')
