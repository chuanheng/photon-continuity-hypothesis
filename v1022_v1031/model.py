"""Clocked pair-source calibration with explicit optical reference planes."""
import json
import numpy as np
from scipy.special import ndtr

def no_click(mean,a,b,law):
    x=mean*np.array([a,b,a+b-a*b])
    return np.exp(-x) if law=='poisson' else 1/(1+x)

def invert(f,law):
    x,y,z=-np.log(f) if law=='poisson' else 1/f-1
    overlap=x+y-z
    return np.array([x*y/overlap,overlap/y,overlap/x])

def herald(f):
    return float((1-f[0]-f[1]+f[2])/(1-f[1]))

def run():
    a,b=.48,.35
    single=1-.12*np.array([a,b,a+b-a*b])
    f=no_click(.55,a,b,'poisson')
    thermal=invert(f,'thermal')
    ma,aa,bb=thermal
    # Power is reduced at a calibrated factor, with stationary efficiencies.
    p=no_click(.55/2,a,b,'poisson')
    t=no_click(ma/2,aa,bb,'thermal')
    blank=np.array([.992,.989,.983])  # correlated accidental events; valid Frechet bounds
    occupied=f*blank
    wrong=occupied/np.r_[blank[:2],blank[0]*blank[1]]
    weights=np.array([.5,.5]);herald_arm=np.array([.9,.1]);response=np.array([.3,.8])
    tagged=weights*herald_arm
    # Conditional time density of a true signal relative to herald.
    windows=np.array([.5,1.,2.])
    gates=a*(2*ndtr(windows/.8)-1)
    common_live=.8
    # Observed single-pair clicks: marginals multiplied by live fraction,
    # both clicks require both detectors live. Independent vs common flags.
    return dict(single=dict(raw=herald(single),true=a),
                multipair=dict(naive=herald(f),corrected=invert(f,'poisson').tolist()),
                law_alias=dict(thermal=thermal.tolist(),max_error=float(np.max(abs(no_click(*thermal,'thermal')-f)))),
                power_holdout=dict(max_gap=float(max(abs(p-t))),p00=[p[2],t[2]]),
                correlated_blank=dict(correct=invert(occupied/blank,'poisson')[1],factorized=invert(wrong,'poisson')[1]),
                mode_bias=dict(heralded=float(tagged@response/tagged.sum()),unconditional=float(weights@response)),
                timing=gates.tolist(),live_flags=dict(common=a,independent=a*common_live),
                plane=dict(identical_products=[.8*.6,.96*.5],eta_interval=[a/.92,a/.88]),
                transfer=dict(two_filters=np.linalg.solve([[.9,.1],[.2,.8]],[.35,.7]).tolist(),
                              target=.4*.3+.6*.8))
if __name__=='__main__': print(json.dumps(run(),indent=2))
