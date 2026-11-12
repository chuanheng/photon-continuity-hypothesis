"""Hydrogen 1s nonrelativistic electric-dipole photoionization cross section.
Analytic Coulomb-continuum formula; infinite nuclear mass, no relativistic or radiative corrections.
Energies in eV, cross sections in cm^2.
"""
import math
ALPHA=1/137.035999084
BOHR_RADIUS_CM=5.29177210903e-9
IONIZATION_EV=13.605693122994
MEGABARN_CM2=1e-18
_PREFACTOR=(512*math.pi**2/3)*ALPHA*BOHR_RADIUS_CM**2

def threshold_cross_section_cm2():
    return _PREFACTOR*math.exp(-4)

def cross_section_cm2(photon_energy_ev):
    if not math.isfinite(photon_energy_ev) or photon_energy_ev<0:
        raise ValueError('photon energy must be finite and nonnegative')
    if photon_energy_ev<IONIZATION_EV:
        return 0.0
    if photon_energy_ev==IONIZATION_EV:
        return threshold_cross_section_cm2()
    ratio=photon_energy_ev/IONIZATION_EV
    eta=1/math.sqrt(ratio-1)
    coulomb=math.exp(-4*eta*math.atan(1/eta))/(-math.expm1(-2*math.pi*eta))
    return _PREFACTOR*ratio**-4*coulomb

def cross_section_megabarn(photon_energy_ev):
    return cross_section_cm2(photon_energy_ev)/MEGABARN_CM2
