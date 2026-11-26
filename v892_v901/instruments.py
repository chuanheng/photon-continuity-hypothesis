"""Two-time path records with an intervening controlled phase."""
import json
import numpy as np
from scipy.linalg import sqrtm, expm
from .model import I, X, Z, run as reachable_run

SIGNS = np.array([1, -1])
def joint(sign, strength=1., reset=False):
    phase = I if sign == 1 else Z
    records = np.zeros((2, 2))
    for i, a in enumerate(SIGNS):
        k = sqrtm((I + a * strength * X) / 2)
        state = k @ (I / 2) @ k.conj().T
        if reset:
            state = state.trace() * (I + X) / 2
        state = phase @ state @ phase
        for j, b in enumerate(SIGNS):
            records[i,j] = np.trace((I + b*X) @ state / 2).real
    return records

def tv(a,b):
    return float(abs(a-b).sum()/2)

def run():
    plus, minus = joint(1), joint(-1)
    reset = joint(1, reset=True)
    switch = (1-np.exp(-np.log(2)))/2
    spin = np.array([1.,0.])
    rotate = lambda angle: expm(-0.5j*angle*X)
    coherence = lambda psi: float(np.vdot(psi,Z@psi).real)
    half = rotate(np.pi/4)
    readout = np.array([[.9,.2],[.1,.8]])
    residuals = []
    for strength in np.linspace(0,1,33):
        for sign in SIGNS:
            classical = (1+np.outer(SIGNS,SIGNS)*sign*strength)/4
            residuals.append(abs(readout @ (joint(sign,strength)-classical) @ readout.T).max())
    return {'v8.92':reachable_run(), 'resolved_tv':tv(plus,minus),
            'discarded_tv':tv(plus.sum(axis=0),minus.sum(axis=0)),
            'weak_tv':tv(joint(1,.6),joint(-1,.6)),
            'reset_cov':float(SIGNS@reset@SIGNS-(SIGNS@reset.sum(axis=1))*(reset.sum(axis=0)@SIGNS)),
            'telegraph_tv':tv((1-switch)*plus+switch*minus,(1-switch)*minus+switch*plus),
            'revival':abs(coherence(rotate(np.pi)@spin))-abs(coherence(rotate(np.pi/2)@spin)),
            'echo_gain':(coherence(half@Z@half@spin)-coherence(half@half@spin))/2,
            'readout_tv':tv(readout@plus@readout.T,readout@minus@readout.T),
            'loss_tv':tv(np.r_[.4*plus.ravel(),.6],np.r_[.4*minus.ravel(),.6]),
            'ordinary_error':float(max(residuals))}

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
