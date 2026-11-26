"""Feasible, equal-per-sector unambiguous receivers for the six coherent inputs."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson
from v922_v931.model import STATES

PHASE = np.array(json.loads((Path(__file__).parents[1]/'v932_v941/results.json').read_text())['phases'])
TARGET = .093

def overlap(phases=PHASE):
    modes = STATES * np.exp(1j * phases[:, None])
    return modes.conj() @ modes.T

def rate(blocks):
    return float(sum(max(0., np.linalg.eigvalsh(block)[0]) for block in blocks))

def discrete(k, mu=1., cutoff=24):
    g = overlap()
    blocks = np.zeros((k, 6, 6), complex)
    for n in range(cutoff+1):
        blocks[n % k] += poisson.pmf(n, mu) * g**n
    return rate(blocks)

def finite(ref, signal=1., phases=PHASE, cutoff=None):
    total = ref + signal
    ns = np.arange(1 + int(poisson.isf(1e-14,total) if cutoff is None else cutoff))
    weights = poisson.pmf(ns,total)
    g = (ref + signal*overlap(phases))/total
    return rate([p * g**int(n) for n,p in zip(ns,weights)])

def receiver(delta):
    g = overlap()
    gram = np.exp(g-1)
    cross = np.exp(g*np.exp(1j*delta)-1)
    # Fixed ideal reciprocal receiver tested on a displaced phase alphabet.
    return np.linalg.eigvalsh(gram)[0]*abs(np.linalg.solve(gram,cross))**2

def jitter(sigma):
    nodes, w = np.polynomial.hermite.hermgauss(40)
    t = sum(weight*receiver(np.sqrt(2)*sigma*x) for x,weight in zip(nodes,w))/np.sqrt(np.pi)
    scores = abs(overlap())**2
    return dict(rate=float(t.sum()/6), fidelity=float((t*scores).sum()/t.sum()))

def plates(angle, retard):
    axis = np.array([np.cos(angle),np.sin(angle)])
    return np.eye(2)+(np.exp(1j*retard)-1)*np.outer(axis,axis)

def run():
    # H,V,D,A produced by HWPs; circular pair by QWPs on H.
    modes = np.array([plates(a,d) @ STATES[0] for a,d in
                      [(0,np.pi),(np.pi/4,np.pi),(np.pi/8,np.pi),(-np.pi/8,np.pi),
                       (np.pi/4,np.pi/2),(-np.pi/4,np.pi/2)]])
    relative = np.sum(STATES.conj()*modes,axis=1)
    threshold = brentq(lambda r: finite(r)-TARGET,0,8)
    ref=2.
    return dict(discrete={str(k):discrete(k) for k in (1,2,3,4,8,25)},
                continuous=finite(0),
                finite_ref=finite(ref), ref_threshold=threshold,
                common_drift=finite(ref,phases=PHASE+.7),
                jitter=jitter(.2), jitter_limit=brentq(lambda x:jitter(x)['fidelity']-.93,.01,.8),
                plate_ray_fidelity=abs(relative)**2,plate_usd=rate([np.exp(modes.conj()@modes.T-1)]),
                mode_match_required=threshold/ref,
                signal_transmission_required=brentq(lambda t:finite(ref,t)-TARGET,.05,1),
                false_herald_fraction=(1-.93)/(1-.5),
                shared_pulse_rates=[finite(1/k) for k in (4,5)],
                matched_first_harmonic=[np.exp(-.5*.4**2),np.exp(-2*.4**2),2*np.exp(-.4**2)-1])

if __name__=='__main__':
    print(json.dumps(run(),default=lambda x:x.tolist(),indent=2))
