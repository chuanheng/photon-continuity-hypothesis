"""Hydrogen 1s -> plane-wave continuum E1 dipole toy, atomic units.

Plane-wave final state omits Coulomb distortion, recoil, and exact cross section.
"""
import math

FOURIER_NORM = 2 * math.sqrt(2) / math.pi

def _momentum(p):
    if len(p) != 3 or not all(math.isfinite(x) for x in p):
        raise ValueError('momentum must be a finite 3-vector')
    return sum(x*x for x in p)

def phi_1s(p):
    p2 = _momentum(p)
    return FOURIER_NORM / (1 + p2)**2

def dipole_z(p):
    p2 = _momentum(p)
    return -1j * (4 * FOURIER_NORM) * p[2] / (1 + p2)**3

def dipole_strength(p):
    return abs(dipole_z(p))**2

def angle_integrated_strength(momentum):
    """Integral dOmega |M(p)|^2 at fixed |p| (not a cross section)."""
    if not math.isfinite(momentum) or momentum < 0:
        raise ValueError('momentum must be finite and nonnegative')
    return (4*math.pi/3) * (4*FOURIER_NORM)**2 * momentum**2 / (1+momentum**2)**6

def radial_strength_density(momentum):
    """p² * integral dOmega |M(p)|², before energy-shell Jacobian."""
    return momentum**2 * angle_integrated_strength(momentum)

def kinetic_momentum(photon_energy, ionization_energy=0.5):
    """Neglecting recoil: p=sqrt(2*(omega-I)) in atomic units."""
    if not all(math.isfinite(x) for x in (photon_energy,ionization_energy)) or ionization_energy <= 0 or photon_energy < ionization_energy:
        raise ValueError('photon energy must be at or above positive threshold')
    return math.sqrt(2*(photon_energy-ionization_energy))
