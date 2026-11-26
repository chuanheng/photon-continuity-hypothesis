"""Conditional fidelity bounds for six known polarizations, with abstention."""
import json
from math import comb
import numpy as np
from scipy.stats import poisson

STATES = np.array([[1,0],[0,1],[1,1],[1,-1],[1,1j],[1,-1j]],complex)
STATES /= np.linalg.norm(STATES,axis=1)[:,None]

def sector(n):
    vectors = np.array([[np.sqrt(comb(n,k))*a**(n-k)*b**k for k in range(n+1)]
                        for a,b in STATES])
    projectors = np.einsum('ia,ib->iab',vectors,vectors.conj())
    total = projectors.sum(axis=0)
    effects = projectors*(n+1)/6
    transition = np.einsum('iab,jba->ij',projectors,effects).real
    overlap = abs(STATES.conj()@STATES.T)**2
    return (float((transition*overlap).sum()/6),
            float(np.linalg.norm(total-6*np.eye(n+1)/(n+1))))

def bounds(eta):
    # mu=1, whole upper tail is retained at the audited efficiencies.
    tail = poisson.sf(3,1)
    p3 = poisson.pmf(3,1)
    p2 = eta-tail-p3
    assert 0 <= p2 <= poisson.pmf(2,1)
    shared = p3*sector(3)[0]+p2*sector(2)[0]
    return ((shared+tail*sector(3)[0])/eta, (shared+tail)/eta)

def run():
    lower,upper=bounds(.093)
    overlap=abs(STATES.conj()@STATES.T)**2
    # Random axis, use its positive/negative outcome to guess that eigenstate.
    axis=float((overlap**2).sum()/18)
    return dict(single=sector(1)[0],two=sector(2)[0],isotropy_error=sector(3)[1],
                three=(1+1/1.5)/2,povm3=sector(3)[0],axis=axis,
                upper=upper,lower=lower,upper_low=bounds(.083)[1],
                upper_high=bounds(.103)[1],margin=.93-upper)

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
