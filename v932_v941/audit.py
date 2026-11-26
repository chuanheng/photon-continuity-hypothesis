"""Six-state sensitivity and optical phase-reference audit."""
import json
from itertools import product
import numpy as np
from scipy.stats import norm,poisson
from v922_v931.model import STATES
from .model import run as weights

F = np.array([.922,.920,.919,.909,.951,.942])
SD = np.array([.004,.004,.005,.004,.004,.004])
def upper(eta):
    n=np.arange(1,41)
    mass=np.clip(eta-poisson.sf(n,1),0,poisson.pmf(n,1))
    scores=np.select([n==1,n==2,n==3],[2/3,3/4,5/6],default=1.)
    return float(mass@scores/eta)

def usd(phases):
    modes=STATES*np.exp(1j*phases[:,None])
    gram=np.exp(modes.conj()@modes.T-1)
    return float(np.linalg.eigvalsh(gram)[0])

def run():
    z=norm.isf(.05/7)
    eta=.093-.01*z
    rng=np.random.default_rng(939940)
    phases=rng.uniform(-np.pi,np.pi,(256,6))
    values=[usd(p) for p in phases]
    best=max(values)
    return dict(v932=weights(),floor=float(min(F-SD*norm.isf(.05/6))),
                eta_floor=eta,joint_margin=min(F-z*SD)-upper(eta),
                bias_budget=min(F)-upper(.083),
                ratio_floor=min(np.average(F,weights=r) for r in product([1,2],repeat=6)),
                independent_sd=np.linalg.norm(SD)/6,common_sd=SD.mean(),
                phase_gain=np.exp(-1)/2-(1-np.sqrt(1-np.exp(-2)))/2,
                usd=usd(np.zeros(6)),best_usd=best,phases=phases[np.argmax(values)].tolist(),
                attainable=.5+.5*min(1,best/.093))

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
