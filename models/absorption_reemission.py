"""Closed resonant Jaynes-Cummings one-excitation subspace; hbar=1.

This is a standard two-state unitary toy model, not an open-system
spontaneous emission model and not a test of individual photon identity.
"""
import math

def populations(coupling, time):
    """Return (P_atom_ground_one_photon, P_atom_excited_vacuum)."""
    if not math.isfinite(coupling) or not math.isfinite(time) or coupling < 0 or time < 0:
        raise ValueError('coupling and time must be finite and nonnegative')
    angle = coupling * time
    return math.cos(angle) ** 2, math.sin(angle) ** 2

def field_number_expectation(coupling, time):
    return populations(coupling, time)[0]

def excitation_expectation(coupling, time):
    p_one, p_excited = populations(coupling, time)
    return p_one + p_excited

def survival_amplitude(coupling, time):
    """Return amplitude <g,1|psi(t)> in the resonant interaction picture."""
    populations(coupling, time)  # validate
    return math.cos(coupling * time)

def return_fidelity(coupling, time):
    """State fidelity with the initial joint atom-field state."""
    return survival_amplitude(coupling, time) ** 2
