"""Finite Fock truncation of the quantum Rabi model (hbar=1).
The boundary is an approximation; never identify truncation artifacts as physics.
"""
import numpy as np

def operators(cutoff, omega=1.0, omega0=1.0, g=0.1):
    if not isinstance(cutoff, int) or isinstance(cutoff,bool) or cutoff < 2:
        raise ValueError('cutoff must be integer >=2')
    if not np.all(np.isfinite([omega,omega0,g])):
        raise ValueError('finite parameters required')
    a=np.diag(np.sqrt(np.arange(1,cutoff,dtype=float)),1)
    ad=a.T
    num=ad@a
    sz=np.diag([-1.,1.]); sx=np.array([[0.,1.],[1.,0.]])
    excite=np.diag([0.,1.]); eye=np.eye(cutoff)
    H=omega*np.kron(np.eye(2),num)+(omega0/2)*np.kron(sz,eye)+g*np.kron(sx,a+ad)
    N=np.kron(np.eye(2),num)+np.kron(excite,eye)
    parity=np.kron(sz,np.diag((-1.)**np.arange(cutoff)))
    return H,N,parity

def commutator(A,B):
    return A@B-B@A

def norm(A):
    return float(np.linalg.norm(A))

def transition(H,atom_from,n_from,atom_to,n_to,cutoff):
    for atom,n in ((atom_from,n_from),(atom_to,n_to)):
        if atom not in (0,1) or not isinstance(n,int) or not 0<=n<cutoff:
            raise ValueError('invalid basis state')
    return float(H[atom_to*cutoff+n_to,atom_from*cutoff+n_from])
