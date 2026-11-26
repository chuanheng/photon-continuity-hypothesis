"""Photon-number selective estimation and a six-state USD counterexample."""
import json
import numpy as np
from scipy.stats import poisson

def allocation(mu, efficiency):
    n = np.arange(1, 41)
    mass = poisson.pmf(n,mu)
    accepted = np.clip(mu*efficiency-poisson.sf(n,mu),0,mass)
    return n, mass, accepted

def benchmark(mu, efficiency):
    n, _, accepted = allocation(mu,efficiency)
    return float(accepted @ ((n+1)/(n+2))/(mu*efficiency))

def run():
    mu, eta = 1., .093
    n, mass, accepted = allocation(mu,eta)
    states = np.array([[1,0],[0,1],[1,1],[1,-1],[1,1j],[1,-1j]],complex)
    states /= np.linalg.norm(states,axis=1)[:,None]
    gram = states.conj() @ states.T
    eig = np.linalg.eigvalsh(gram**5)
    x = np.array([[0,1],[1,0]])
    z = np.diag([1,-1])
    y = 1j*x@z
    fidelities = []
    for state in states:
        rho = np.outer(state,state.conj())
        channel = .895*rho + .035*sum(p@rho@p for p in [x,y,z])
        fidelities.append(np.vdot(state,channel@state).real)
    flat = mass @ ((n+1)/(n+2))/(1-np.exp(-mu))
    return dict(benchmark=benchmark(mu,eta),nonempty=eta/(1-np.exp(-mu)),
                fraction2=accepted[1]/mass[1],low_eff=benchmark(mu,.083),
                high_eff=benchmark(mu,.103),ceiling2=-np.expm1(-2)/2,
                flat=float(flat),selection_gain=benchmark(mu,eta)-flat,
                background=2*(1-.93),channel_fidelity=float(np.mean(fidelities)),
                rank4=int(np.linalg.matrix_rank(gram**4)),rank5=int(np.linalg.matrix_rank(gram**5)),
                min_eigenvalue=float(eig[0]),usd_efficiency=poisson.pmf(5,mu)*eig[0]/mu,
                omitted_mass=poisson.sf(40,mu))

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
