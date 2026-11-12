"""Coherent two-path absorption in a resonant three-state toy model.

The two complex amplitudes must lead to the SAME indistinguishable final state.
This model does not derive microscopic QED matrix elements or photon identity.
"""
import cmath
import math


def effective_absorption(g1, g2, phase):
    """Return complex absorption coupling g1 + g2 exp(i phase)."""
    if any(not math.isfinite(v) for v in (g1, g2, phase)):
        raise ValueError('all parameters must be finite')
    if g1 < 0 or g2 < 0:
        raise ValueError('coupling magnitudes must be nonnegative')
    return g1 + g2 * cmath.exp(1j * phase)


def populations(kappa, g1, g2, phase, time):
    """Return (P_initial, P_successor, P_absorbed) at time t, hbar=1.

    H=[[0,kappa,g_eff],[kappa,0,0],[conj(g_eff),0,0]].
    The Hermitian H yields Omega=sqrt(kappa^2+abs(g_eff)^2).
    """
    if not math.isfinite(kappa) or not math.isfinite(time) or kappa < 0 or time < 0:
        raise ValueError('kappa and time must be finite and nonnegative')
    g = effective_absorption(g1, g2, phase)
    omega = math.hypot(kappa, abs(g))
    if omega == 0:
        return (1., 0., 0.)
    transfer = math.sin(omega * time) ** 2
    return (1-transfer, (kappa/omega)**2 * transfer, (abs(g)/omega)**2 * transfer)


def first_transfer_absorption_fraction(kappa, g1, g2, phase):
    if not math.isfinite(kappa) or kappa < 0:
        raise ValueError('kappa must be finite and nonnegative')
    g = effective_absorption(g1, g2, phase)
    omega = math.hypot(kappa, abs(g))
    if omega == 0:
        raise ValueError('zero coupling: no transfer maximum')
    return (abs(g)/omega)**2


if __name__ == '__main__':
    for phase_error in (0., .01, .1, .5):
        p = first_transfer_absorption_fraction(1., 1., 1., math.pi+phase_error)
        print(f'phase error={phase_error:.3f} rad, P_abs={p:.9f}')
