"""Two-qubit identity-ancilla toy: standard QM, not a QED photon theory."""
import cmath
import math

def _validate(g, t, hbar):
    if not all(math.isfinite(x) for x in (g,t,hbar)) or t < 0 or hbar <= 0:
        raise ValueError('invalid physical parameters')

def reduced_system(g, t, hbar=1.0):
    """Reduced 2x2 density matrix for |+>|+> under g Z⊗Z."""
    _validate(g,t,hbar)
    coherence=0.5*math.cos(2*g*t/hbar)
    return ((0.5+0j,complex(coherence)),(complex(coherence),0.5+0j))

def visibility(g,t,hbar=1.0):
    _validate(g,t,hbar)
    return abs(math.cos(2*g*t/hbar))

def purity(g,t,hbar=1.0):
    v=visibility(g,t,hbar)
    return (1+v*v)/2

def x_plus_probability(g,t,hbar=1.0):
    _validate(g,t,hbar)
    return (1+math.cos(2*g*t/hbar))/2

def uncoupled_probability(system_rho, measurement):
    """Born probability for any reduced system state, independent of ancilla."""
    if len(system_rho)!=2 or len(measurement)!=2 or any(len(r)!=2 for r in system_rho+measurement):
        raise ValueError('2x2 matrices required')
    return sum(measurement[i][j]*system_rho[j][i] for i in range(2) for j in range(2)).real
