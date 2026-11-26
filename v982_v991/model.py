"""Separable strategies for explicitly flagged probe-label leakage."""
import json
from itertools import product
import numpy as np
from scipy.stats import beta
from v972_v981.model import B,T,probes,score

MASKS=np.array(list(product((0,1),repeat=4)))
STATES=probes(T)
def single():
    best=0.
    for mask in MASKS:
        coeff=mask@B
        op=np.einsum('i,ijk->jk',coeff,STATES)
        best=min(best,np.minimum(np.linalg.eigvalsh(op),0).sum())
    return float(best)

def joint():
    pay=MASKS@B@MASKS.T
    i,j=np.unravel_index(np.argmin(pay),pay.shape)
    return dict(value=float(pay[i,j]),left=MASKS[i].tolist(),right=MASKS[j].tolist())

def copies(n):
    # Full label on Bob is unavailable. Alice instead receives n identical qubits.
    # Bob applies the one-qubit effect projecting onto the antipode of tetrahedral vertex 0.
    weights=B@((1-T@T[0])/2)
    op=np.zeros((2**n,2**n),complex)
    for w,rho in zip(weights,STATES):
        tensor=np.ones((1,1),complex)
        for _ in range(n):tensor=np.kron(tensor,rho)
        op+=w*tensor
    return float(np.minimum(0,np.linalg.eigvalsh(op)).sum())

def unambiguous(n):
    # Columns of the pure preparation kets; per-label equal success is lambda_min.
    ket=np.array([np.linalg.eigh(rho)[1][:,-1] for rho in STATES])
    gram=(ket.conj()@ket.T)**n
    return max(0.,float(min(np.linalg.eigvalsh(gram))))

def run():
    double=joint()
    one=single()
    # Both fault flags provided to both stations; independent of probe labels.
    e=.03
    def floor(q):return (2*e-2*q)*one+q*double['value']
    leak_rate=np.array([.03,.01,.04,.02])
    # Source with label-dependent flagged probabilities shared only via trial seed:
    # For this construction only Alice leaks, Bob uses one projector.
    proj=(1-T@T[0])/2
    costs=leak_rate*(B@proj)
    # label blind marginal at one station from an antipodal sign/key encoding
    # Both stations hold the same random key; conjugate response assignments.
    A=np.array([0,0,1,1]);D=1-A
    masked=(np.outer(A,D)+np.outer(1-A,1-D))/2
    return dict(both=double,one=one,
                correlated=dict(independent=floor(e**2),synchronous=floor(e),exclusive=floor(0)),
                keyed=dict(score=score(masked),marginals=[.5]*4),
                copies=[copies(n) for n in (1,2,3)],usd=[unambiguous(n) for n in (1,2,3,4)],
                unequal=dict(score=float(np.minimum(costs,0).sum()),costs=costs.tolist()),
                distance_budget=4*(.001+.002),
                pilot_zero=float(beta.ppf(.95,1,1000)),
                adaptive=dict(bound_range=12.,trials=int(np.ceil(12**2*np.log(1/.05)/(2*.011625**2)))))

if __name__=='__main__':print(json.dumps(run(),indent=2))
