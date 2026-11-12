"""Hermitian commutants of detuned two-state JC Hamiltonians; hbar=1."""
import math
def _finite(*xs):
    if not all(math.isfinite(x) for x in xs): raise ValueError('parameters must be finite')
def commutator_coefficients(delta,g,a,b,c,d):
    _finite(delta,g,a,b,c,d)
    return (-delta*c/2,delta*b/2-g*d,g*c)
def commutator_norm(delta,g,a,b,c,d):
    x,y,z=commutator_coefficients(delta,g,a,b,c,d)
    return 2*math.sqrt(2)*math.sqrt(x*x+y*y+z*z)
def conserved(delta,g,a,b,c,d,tolerance=1e-12):
    _finite(tolerance)
    if tolerance<0: raise ValueError('negative tolerance')
    return commutator_norm(delta,g,a,b,c,d)<=tolerance
def fixed_commutant_basis(delta,g):
    _finite(delta,g)
    identity=(1.,0.,0.,0.)
    if delta==0 and g==0:
        return (identity,(0.,1.,0.,0.),(0.,0.,1.,0.),(0.,0.,0.,1.))
    return (identity,(0.,g,0.,delta/2))
def common_commutant_basis(parameter_pairs):
    pairs=tuple(parameter_pairs)
    if not pairs: raise ValueError('at least one Hamiltonian required')
    for delta,g in pairs: _finite(delta,g)
    active=[(delta,g) for delta,g in pairs if delta!=0 or g!=0]
    if not active: return fixed_commutant_basis(0,0)
    d0,g0=active[0]
    if any(g0*d-d0*g!=0 for d,g in active[1:]):
        return ((1.,0.,0.,0.),)
    return fixed_commutant_basis(d0,g0)
def eigenvalues(delta,g):
    _finite(delta,g)
    r=math.hypot(g,delta/2)
    return (-r,r)
