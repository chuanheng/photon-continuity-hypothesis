import numpy as np
I=np.eye(2,dtype=complex)
Z=np.diag([1,-1]).astype(complex)
X=np.array([[0,1],[1,0]],complex)
def state(bit):
    if bit not in (0,1):raise ValueError('bit')
    v=np.eye(2,dtype=complex)[:,bit]
    return np.outer(v,v.conj())
def reduced_system(joint):
    return np.trace(np.asarray(joint).reshape(2,2,2,2),axis1=1,axis2=3)
def controlled_phase(theta):
    zz=np.kron(Z,Z)
    return np.cos(theta/2)*np.eye(4)-1j*np.sin(theta/2)*zz
def evolve(system,hidden,theta=0):
    u=controlled_phase(theta)
    return u@np.kron(system,hidden)@u.conj().T
def probability(rho,effect):
    return float(np.real(np.trace(rho@effect)))
def trace_distance(rho,sigma):
    return float(np.sum(np.abs(np.linalg.eigvalsh(rho-sigma)))/2)
def system_distinguishability(a,b,theta=0):
    plus=(I+X)/2
    return trace_distance(reduced_system(evolve(plus,a,theta)),reduced_system(evolve(plus,b,theta)))
