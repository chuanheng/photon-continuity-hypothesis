"""Complete Hermitian commutant for resonant one-excitation JC toy; hbar=1."""
import math

def _check(*values):
    if not all(math.isfinite(v) for v in values):
        raise ValueError('finite real parameters required')

def charge_matrix(a,b,c,d):
    _check(a,b,c,d)
    return ((complex(a+d),complex(b,-c)),(complex(b,c),complex(a-d)))

def commutator(g,a,b,c,d):
    """[g sigma_x, Q] in basis |g,1>,|e,0>."""
    _check(g,a,b,c,d)
    return ((2j*g*c, -2*g*d),(2*g*d,-2j*g*c))

def commutator_frobenius(g,a,b,c,d):
    _check(g,a,b,c,d)
    return 2*math.sqrt(2)*abs(g)*math.hypot(c,d)

def conserved(g,a,b,c,d,tol=1e-12):
    _check(g,a,b,c,d,tol)
    if tol<0: raise ValueError('negative tolerance')
    return commutator_frobenius(g,a,b,c,d)<=tol

def eigenvalues(a,b,c,d):
    _check(a,b,c,d)
    r=math.sqrt(b*b+c*c+d*d)
    return (a-r,a+r)

def exact_commutant_basis(g):
    """Pauli coefficient basis, in order (I, X, Y, Z)."""
    _check(g)
    if g==0:
        return ((1.,0.,0.,0.),(0.,1.,0.,0.),(0.,0.,1.,0.),(0.,0.,0.,1.))
    return ((1.,0.,0.,0.),(0.,1.,0.,0.))
