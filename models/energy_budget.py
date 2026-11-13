"""Necessary nonrelativistic energy-budget bounds for hydrogen photoionization.
Not sufficient for momentum conservation or a QED cross-section prediction.
"""
import math
IONIZATION_EV = 13.605693122994

def _valid(*xs):
    if not all(math.isfinite(x) for x in xs):
        raise ValueError('finite values required')

def excess_energy(incident_ev, ionization_ev=IONIZATION_EV):
    _valid(incident_ev, ionization_ev)
    if incident_ev < 0 or ionization_ev <= 0:
        raise ValueError('invalid energies')
    return incident_ev - ionization_ev

def remaining_kinetic(incident_ev, successor_ev, other_radiation_ev=0.0, ionization_ev=IONIZATION_EV):
    _valid(successor_ev, other_radiation_ev)
    if successor_ev < 0 or other_radiation_ev < 0:
        raise ValueError('radiation energies must be nonnegative')
    return excess_energy(incident_ev, ionization_ev) - successor_ev - other_radiation_ev

def energetically_allowed(incident_ev, successor_ev, other_radiation_ev=0.0, ionization_ev=IONIZATION_EV):
    return remaining_kinetic(incident_ev, successor_ev, other_radiation_ev, ionization_ev) >= 0

def electron_kinetic_from_recoil(incident_ev, successor_ev, recoil_ev, other_radiation_ev=0.0, ionization_ev=IONIZATION_EV):
    _valid(recoil_ev)
    if recoil_ev < 0:
        raise ValueError('recoil must be nonnegative')
    electron_ev = remaining_kinetic(incident_ev, successor_ev, other_radiation_ev, ionization_ev) - recoil_ev
    if electron_ev < 0:
        raise ValueError('energy budget violated')
    return electron_ev

def max_successor_energy(incident_ev, recoil_ev=0.0, other_radiation_ev=0.0, ionization_ev=IONIZATION_EV):
    _valid(recoil_ev, other_radiation_ev)
    if recoil_ev < 0 or other_radiation_ev < 0:
        raise ValueError('negative energies')
    return max(0.0, excess_energy(incident_ev, ionization_ev) - recoil_ev - other_radiation_ev)
