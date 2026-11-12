"""Two-path visibility from hypothetical normalized ancillary identity states.
This is standard Hilbert-space mathematics, not evidence for photon identity.
"""
import cmath
import math

def normalize(state):
    z=tuple(complex(v) for v in state)
    if not z or any(not math.isfinite(v.real) or not math.isfinite(v.imag) for v in z):
        raise ValueError('invalid state')
    norm=math.sqrt(sum(abs(v)**2 for v in z))
    if norm==0 or not math.isfinite(norm):
        raise ValueError('zero or invalid norm')
    return tuple(v/norm for v in z)

def overlap(first, second):
    a,b=normalize(first),normalize(second)
    if len(a)!=len(b):
        raise ValueError('dimension mismatch')
    return sum(x.conjugate()*y for x,y in zip(a,b))

def visibility(first,second):
    return min(1.0,abs(overlap(first,second)))

def path_probability(first,second,phase):
    """Probability of one output port for a balanced Mach-Zehnder toy model."""
    if not math.isfinite(phase):
        raise ValueError('invalid phase')
    inner=overlap(first,second)
    return max(0.0,min(1.0,0.5*(1+(inner*cmath.exp(1j*phase)).real)))

def reduced_path_purity(first,second):
    """Tr(rho_path**2) after tracing out ancillary state."""
    v=visibility(first,second)
    return (1+v*v)/2

def identity_information_bound(first,second):
    """Helstrom optimal success for equally likely pure ancilla states."""
    v=visibility(first,second)
    return (1+math.sqrt(max(0.0,1-v*v)))/2
