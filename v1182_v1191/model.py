"""Reachable phase references, unit-efficiency two-photon trials."""
import json
import numpy as np
from scipy.stats import binom
from v1172_v1181.model import count_probabilities


def run():
    angle=.33
    ref=np.array([.5,1/np.sqrt(2),.5])
    direct,mirror=[count_probabilities(ref,angle,p)[0] for p in (0,np.pi)]
    grid=2*np.pi*np.arange(32)/32
    relative=[count_probabilities(ref*np.exp(1j*p*np.arange(3)),angle,0)[0] for p in grid]
    common=[count_probabilities(ref*np.exp(2j*p),angle,0)[0] for p in grid]
    # Orthogonal input supermodes + and - with spectral overlap v.
    q=(1+np.sin(2*angle))/2
    overlap=.7
    paired=(1+overlap**2)*q*(1-q)
    n=24
    # Bounded additive calibration errors, independently verified only in a real experiment.
    low=min(1.,mirror+.05)
    high=max(0.,direct-.05)
    k=next(k for k in range(n+2) if binom.sf(k-1,n,low)<=.01)
    return {'reachable':[float(direct),float(mirror)],
            'twirls':[float(np.mean(relative)),float(np.mean(common))],
            'orthogonal_ports':[float(paired),float((1+overlap**2)*(1-q)*q)],
            'count_test':{'n':n,'threshold':k,'worst_false_positive':float(binom.sf(k-1,n,low)),
                          'minimum_power':float(binom.sf(k-1,n,high))}}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
