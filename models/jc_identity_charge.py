"""JC one-excitation identity charge toy. hbar=1, not new physics."""
import math
def _valid(g,q_photon,q_atom):
    if not all(math.isfinite(x) for x in (g,q_photon,q_atom)): raise ValueError('finite parameters required')
def commutator(g,q_photon,q_atom):
    _valid(g,q_photon,q_atom)
    v=g*(q_atom-q_photon)
    return ((0.,v),(-v,0.))
def commutator_norm(g,q_photon,q_atom):
    return math.sqrt(2)*abs(g*(q_atom-q_photon))
def is_conserved(g,q_photon,q_atom,tol=1e-12):
    _valid(g,q_photon,q_atom)
    if not math.isfinite(tol) or tol<0: raise ValueError('invalid tolerance')
    return commutator_norm(g,q_photon,q_atom)<=tol
def photon_probability(g,t):
    if not math.isfinite(g) or not math.isfinite(t): raise ValueError('finite parameters required')
    return math.cos(g*t)**2
def atomic_excitation_probability(g,t):
    if not math.isfinite(g) or not math.isfinite(t): raise ValueError('finite parameters required')
    return math.sin(g*t)**2
def charge_expectation(g,t,q_photon,q_atom):
    _valid(g,q_photon,q_atom)
    return q_photon*photon_probability(g,t)+q_atom*atomic_excitation_probability(g,t)
def charge_variance(g,t,q_photon,q_atom):
    _valid(g,q_photon,q_atom)
    p=photon_probability(g,t)
    return p*(1-p)*(q_photon-q_atom)**2
