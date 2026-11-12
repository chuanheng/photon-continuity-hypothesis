"""Exactly soluble resonant three-state toy Hamiltonian, hbar=1.

Basis H (input photon), L (excited matter + photon), A (excited matter,
zero photons). Hamiltonian [[0,k,g],[k,0,0],[g,0,0]].
Not a QED amplitude, cross section, or experimental prediction.
"""
import math

def populations(kappa, absorption, time):
    if any(not math.isfinite(v) for v in (kappa, absorption, time)):
        raise ValueError('parameters must be finite')
    if kappa < 0 or absorption < 0 or time < 0:
        raise ValueError('couplings and time must be nonnegative')
    omega = math.hypot(kappa, absorption)
    if omega == 0:
        return (1.0, 0.0, 0.0)
    transition = math.sin(omega * time)**2
    return (1-transition, (kappa/omega)**2 * transition,
            (absorption/omega)**2 * transition)

def absorption_fraction_at_first_transfer(kappa, absorption):
    """Fraction of zero-photon outcome at t=pi/(2 omega), omega>0."""
    if any(not math.isfinite(v) or v < 0 for v in (kappa, absorption)):
        raise ValueError('couplings must be finite and nonnegative')
    if kappa == 0 and absorption == 0:
        raise ValueError('no transfer with zero couplings')
    return (absorption / math.hypot(kappa, absorption))**2

if __name__ == '__main__':
    for g in (0, 0.1, 0.5, 1):
        omega=math.hypot(1,g)
        print('kappa=1, g=',g,'populations=',populations(1,g,math.pi/(2*omega)))
