"""v0.68: two-photon HOM distinguishability and dephasing equivalence."""
import numpy as np

def normalized(v):
    v=np.asarray(v,dtype=complex)
    if v.ndim!=1 or np.linalg.norm(v)==0: raise ValueError('invalid state')
    return v/np.linalg.norm(v)

def overlap_squared(a,b):
    return float(np.clip(abs(np.vdot(normalized(a),normalized(b)))**2,0,1))

def hom_probability(a,b):
    return (1-overlap_squared(a,b))/2

def phase_damping(rho,eta):
    if not 0<=eta<=1: raise ValueError('eta outside [0,1]')
    rho=np.asarray(rho,dtype=complex)
    if rho.shape!=(2,2): raise ValueError('requires qubit density matrix')
    return np.array([[rho[0,0],eta*rho[0,1]],[eta*rho[1,0],rho[1,1]]])

def visibility_from_environment_overlap(overlap):
    if not 0<=overlap<=1: raise ValueError('invalid overlap')
    return float(overlap)

def visibility_from_hidden_label(overlap):
    return visibility_from_environment_overlap(overlap)

def coincidence_from_visibility(visibility):
    if not 0<=visibility<=1: raise ValueError('invalid visibility')
    return (1-visibility)/2

def binomial_kl(p,q):
    if not 0<=p<=1 or not 0<q<1: raise ValueError('invalid probability')
    result=0.
    if p>0: result+=p*np.log(p/q)
    if p<1: result+=(1-p)*np.log((1-p)/(1-q))
    return float(result)

def expected_llr(p,q,shots):
    if shots<0: raise ValueError('negative shots')
    return 2*shots*binomial_kl(p,q)
