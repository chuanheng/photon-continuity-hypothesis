"""Two-qubit identity-charge toy model; hbar=1. Not a theory of photon identity."""
import numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Z=np.diag([1.,-1.]).astype(complex)

def hamiltonian(g=1.,lam=0.):
    if not np.all(np.isfinite([g,lam])): raise ValueError('finite parameters required')
    return g*np.kron(X,I)+lam*np.kron(Z,Z)

def charge(): return np.kron(I,Z)

def commutator(a,b): return a@b-b@a

def evolution(h,t):
    if not np.isfinite(t): raise ValueError('finite time required')
    e,v=np.linalg.eigh(h)
    return (v*np.exp(-1j*e*t))@v.conj().T

def jc_probability(g,lam,t,identity_z=1):
    """Probability to flip JC qubit from |0> to |1> for identity Z eigenstate."""
    if identity_z not in (-1,1): raise ValueError('identity_z must be +/-1')
    if not np.all(np.isfinite([g,lam,t])): raise ValueError('finite parameters required')
    r=np.hypot(g,lam)
    return 0. if r==0 else float((g*g/r**2)*np.sin(r*t)**2)

def reduced_jc(rho):
    rho=np.asarray(rho,dtype=complex)
    if rho.shape!=(4,4): raise ValueError('4x4 density matrix required')
    return np.trace(rho.reshape(2,2,2,2),axis1=1,axis2=3)

def physical_expectation(rho,observable):
    if np.asarray(observable).shape!=(2,2): raise ValueError('2x2 observable required')
    return np.trace(reduced_jc(rho)@observable)
