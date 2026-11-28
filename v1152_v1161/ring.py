"""Unit hopping and hbar=1. Matrix columns are preparations."""
import numpy as np
from scipy.linalg import expm


def hamiltonian(flux, link=1., detuning=0.):
    phase = link * np.exp(1j * flux)
    return np.array([[0, 1, phase], [1, detuning, 1], [phase.conjugate(), 1, 0]])


def probabilities(h, time):
    return abs(expm(-1j * time * h))**2


def solve():
    flux, time = .7, .83
    h = hamiltonian(flux)
    p = probabilities(h, time)
    gauge = np.diag(np.exp(1j * np.array([.2, -.3, .9])))
    line = hamiltonian(0, link=0)
    spectrum = np.linalg.eigvalsh(h)
    direction = p[1,0] - p[0,1]
    short = .001
    ps = probabilities(h, short)
    # Eliminate material site 1 at a complex probe frequency.
    z = 1.3 + .2j
    endpoints = [0,2]
    direct = h[np.ix_(endpoints,endpoints)]
    coupling = h[endpoints,1:2]
    reduced = np.linalg.inv(z*np.eye(2)-direct-coupling@coupling.conj().T/z)
    full = np.linalg.inv(z*np.eye(3)-h)[np.ix_(endpoints,endpoints)]
    dark = np.array([1,0,-1])/np.sqrt(2)
    leak = abs((expm(-1j*time*h)@dark)[1])**2
    efficiencies = np.array([.71,.9,.8])
    reciprocal = probabilities(hamiltonian(0),time)
    measured = efficiencies[:,None]*reciprocal
    rng = np.random.default_rng(115261)
    grid = rng.uniform(.1,2,24)
    label, material = .19, .51
    residuals = [np.max(abs(probabilities(hamiltonian(label+material),t)-
                            probabilities(hamiltonian(0.+flux),t))) for t in grid]
    return {
        'tree_gauge': float(np.max(abs(probabilities(line,time)-probabilities(gauge@line@gauge.conj().T,time)))),
        'flux_spectrum': spectrum.tolist(),
        'direction': float(direction),
        'short_time': float((ps[1,0]-ps[0,1])/short**3),
        'material_elimination': float(np.max(abs(full-reduced))),
        'dark_leak': float(leak),
        'efficiency': [float(measured[1,0]-measured[0,1]),float(measured[1,0]/efficiencies[1]-measured[0,1]/efficiencies[0])],
        'heldout': float(max(residuals))}
