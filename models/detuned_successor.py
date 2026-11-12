"""Hermitian detuned three-state effective model, not microscopic QED. hbar=1."""
import math
import numpy as np

def detunings(incident, successor, matter_successor, matter_absorption):
    vals=(incident,successor,matter_successor,matter_absorption)
    if not all(math.isfinite(v) for v in vals) or incident<=0 or successor<=0 or matter_successor<0 or matter_absorption<0:
        raise ValueError("invalid energies")
    return matter_successor+successor-incident,matter_absorption-incident

def hamiltonian(kappa, absorption, delta_successor, delta_absorption):
    vals=(kappa,absorption,delta_successor,delta_absorption)
    if not all(math.isfinite(v) for v in vals) or kappa<0 or absorption<0:
        raise ValueError("invalid parameters")
    return np.array([[0.,kappa,absorption],[kappa,delta_successor,0.],[absorption,0.,delta_absorption]])

def evolve(kappa, absorption, delta_successor, delta_absorption, time):
    if not math.isfinite(time) or time<0:
        raise ValueError("invalid time")
    h=hamiltonian(kappa,absorption,delta_successor,delta_absorption)
    eigenvalues,eigenvectors=np.linalg.eigh(h)
    return eigenvectors @ (np.exp(-1j*eigenvalues*time)*eigenvectors[0,:].conj())

def probabilities(kappa, absorption, delta_successor, delta_absorption, time):
    return tuple(float(x) for x in np.abs(evolve(kappa,absorption,delta_successor,delta_absorption,time))**2)
