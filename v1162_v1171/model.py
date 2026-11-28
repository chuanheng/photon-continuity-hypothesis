"""Two excitations in a symmetric dimer. Energies in hopping units."""
import json
import numpy as np
from scipy.linalg import expm


def hamiltonian(interaction, bias=0., hopping=1.):
    # |20>, |11>, |02>; bias is the single-particle energy difference.
    link = np.sqrt(2)*hopping
    return np.array([[interaction+bias,link,0.],[link,0.,link],[0.,link,interaction-bias]])


def state(interaction, time, bias=0.):
    return expm(-1j*time*hamiltonian(interaction,bias))[:,0]


def solve(interaction=8.):
    h = hamiltonian(interaction)
    dark = np.array([1,0,-1])/np.sqrt(2)
    spectrum = np.linalg.eigvalsh(h)
    gap = np.sqrt(interaction**2+16)
    plus, minus = state(interaction,.4), state(-interaction,.4)
    phase_probe = np.array([1,1,0])/np.sqrt(2)
    resonance = [abs(state(interaction,.9,b)[1])**2 for b in (0.,-interaction)]
    # No-pair-loss sector under jumps sqrt(kappa/2) a_j^2 into vacuum.
    loss = .18
    survival = expm((-1j*h-loss*np.diag([1,0,1])/2)*.7)[:,0]
    rng = np.random.default_rng(116271)
    holdout = rng.uniform(.2,2.,16)
    candidates = [abs(state(2.+6.,t))**2 for t in holdout]
    ordinary = [abs(state(8.,t))**2 for t in holdout]
    # Local dephasing after a balanced beam splitter leaves all number counts fixed.
    pair = state(0.,np.pi/4)
    rho = np.outer(pair,pair.conjugate())
    incoherent = np.diag(np.diag(rho))
    return {
        'enhanced_entry':float(h[1,0]),
        'dark_eigen_error':float(np.linalg.norm(h@dark-interaction*dark)),
        'pair_splitting':[float(spectrum[-1]-interaction),4./interaction],
        'breakup_peak':float(abs(state(interaction,np.pi/gap)[1])**2),
        'sign_counts':float(np.max(abs(abs(plus)**2-abs(minus)**2))),
        'phase_probe':[float(abs(phase_probe@v)**2) for v in (plus,minus)],
        'tilt_resonance':resonance,
        'pair_loss':[float(np.vdot(survival,survival).real),float(abs(survival[1])**2)],
        'shared_kerr':float(np.max(abs(np.array(candidates)-ordinary))),
        'dephased_counts':{'count_error':float(np.max(abs(np.diag(rho-incoherent)))),
                           'return_pure':float(np.vdot(pair,rho@pair).real),
                           'return_dephased':float(np.vdot(pair,incoherent@pair).real)}}


def run():
    return solve()


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
