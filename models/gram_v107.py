"""v1.07 GitHub companion: exact bosonic creation operators for arbitrary
three pure internal states, entering spatial ports a,a,b. Standard QO.
The actual full 44/44 locally tested implementation is in v1.07 ZIP.
"""
from collections import defaultdict
import numpy as np

def gram(states):
    V=np.asarray(states,complex)
    if V.ndim!=2 or V.shape[0]!=3 or not np.all(np.isfinite(V)):
        raise ValueError('three finite normalized internal states')
    if not np.allclose(np.linalg.norm(V,axis=1),1,atol=1e-9):
        raise ValueError('normalized vectors')
    return V.conj()@V.T

def gram_states(G):
    G=np.asarray(G,complex)
    if G.shape!=(3,3) or not np.allclose(G,G.conj().T,atol=1e-9):
        raise ValueError('Hermitian Gram')
    if not np.allclose(np.diag(G),1,atol=1e-9):raise ValueError('diagonal')
    ev,V=np.linalg.eigh(G)
    if min(ev)<-1e-9:raise ValueError('positive semidefinite Gram needed')
    state=(np.diag(np.sqrt(np.maximum(ev,0)))@V.conj().T).T
    if not np.allclose(gram(state),G,atol=1e-8):raise ValueError('bad Gram factor')
    return state

def _add_creation(current,operator):
    output=defaultdict(complex)
    for fock,amplitude in current.items():
        for i,c in enumerate(operator):
            if abs(c)<1e-14:continue
            occ=list(fock);occ[i]+=1
            output[tuple(occ)]+=amplitude*c*np.sqrt(occ[i])
    return output

def split_three(states,ports=(0,0,1)):
    states=np.asarray(states,complex);gram(states)
    if len(ports)!=3 or sorted(ports) not in ([0,0,1],[0,1,1]):
        raise ValueError('two photons in one input, one in the other')
    d=states.shape[1];out={(0,)*(2*d):1+0j}
    for state,port in zip(states,ports):
        transform=np.r_[state/np.sqrt(2),(1 if port==0 else -1)*state/np.sqrt(2)]
        out=_add_creation(out,transform)
    P=np.zeros(4);norm=0.
    for occ,amp in out.items():
        w=abs(amp)**2;norm+=w;P[sum(occ[:d])]+=w
    if norm<=0:raise ValueError('null Fock state')
    return P/norm

def restricted_rho(rho):
    if not np.isfinite(rho) or not 0<=rho<=1:raise ValueError('rho')
    return rho*np.array([3,1,1,3])/8+(1-rho)*np.array([1,3,3,1])/8

def triad_phase(G):
    G=np.asarray(G,complex)
    return float(np.angle(G[0,1]*G[1,2]*G[2,0]))

def gram_phase_demo(r=.5):
    G0=np.array([[1,r,r],[r,1,r],[r,r,1]],complex)
    G1=np.array([[1,r,r],[r,1,1j*r],[r,-1j*r,1]],complex)
    return {'magnitudes_same':bool(np.allclose(abs(G0),abs(G1))),
       'pairwise_overlap_squares':[r*r]*3,
       'triad_phase_0':triad_phase(G0),'triad_phase_pi2':triad_phase(G1),
       'distribution_0':split_three(gram_states(G0)).tolist(),
       'distribution_pi2':split_three(gram_states(G1)).tolist()}
