"""Three-axis Bell data with explicit trial selection and calibration."""
import json
import numpy as np
from scipy.special import ndtr
from .model import run as prior

def selected(good, bad, corr):
    agree=good*(1+corr)/2
    disagree=bad*(1-corr)/2
    return (agree-disagree)/(agree+disagree)

def paired(window, separation=3., jitter=.5):
    def mass(mean):
        return ndtr((window-mean)/jitter)-ndtr((-window-mean)/jitter)
    return (1+3*selected(mass(0),mass(separation),0))/4

def axes(angle):
    # Reference axes ideal. Readout Y is tilted toward X.
    c,s=np.cos(angle),np.sin(angle)
    return np.array([[1,0,0],[s,c,0],[0,0,1]])

def run():
    h=.093
    k=8
    local=1/np.sqrt(3)
    A=axes(np.pi/12)
    # Coherent branch: swap from signal to ordinary ancillary qubit and back.
    swap=np.eye(4)[[0,2,1,3]]
    phi=np.array([1,0,0,1])/np.sqrt(2)
    vector=np.kron(phi,[1,0])
    stored=(np.kron(np.eye(2),swap)@vector).reshape(2,2,2)
    emitted=(np.kron(np.eye(2),swap)@stored.ravel()).reshape(2,2,2)
    p=.02
    return dict(prior=prior(), outcome_gate=(1+3*selected(k,1,1/3))/4,
                single_arm=(1+3*local)/4, coincidence_scan=[paired(w) for w in (.5,2,6)],
                early_leak=min(1.,p/h), apparent_early=.5+.5*min(1.,p/h),
                axis_bound=(1+np.linalg.norm(A,2))/4,
                source_memory_products=[.8*.75,.6*1.],
                bypass=dict(stored_signal_excited=float(np.sum(abs(stored[:,1,:])**2)),
                            bell_return=float(abs(phi@emitted[:,:,0].ravel())**2)),
                all_trials=dict(min_efficiency=2/3,implied_sum=3*(2*h-1)))

if __name__=='__main__':print(json.dumps(run(),indent=2))
