"""Per-clocked-trial HBT click probabilities for a specified output receiver."""
import json
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq
from v942_v951.model import finite

def clicks(p,a=.3,b=.2,dark=0.):
    """Exclusive outcome order 00, 10, 01, 11; a,b include splitting."""
    n=np.arange(len(p))
    na=(1-dark)*np.dot(p,(1-a)**n)
    nb=(1-dark)*np.dot(p,(1-b)**n)
    both=(1-dark)**2*np.dot(p,(1-a-b)**n)
    return np.array([both,nb-both,na-both,1-na-nb+both])

def moments(p):
    n=np.arange(len(p))
    return float((n*(n-1))@p/(n@p)**2)

def ratio(c):
    return c[3]/(c[1]+c[2])

def design(settings):
    return np.vstack([np.column_stack([clicks(p,a,b) for p in np.eye(5)]) for a,b in settings])

def run():
    # One photon when a uniformly diluted reciprocal outcome succeeds.
    prob=.093
    single=np.array([1-prob,prob])
    r=.005
    p1=prob/(1+2*r)
    double=np.array([1-p1*(1+r),p1,p1*r])
    m=design([(.3,.2)])
    direction=null_space(m)[:,0]
    p=np.array([.80,.08,.05,.04,.03])
    q=p+.02*direction/max(abs(direction))
    scans=design([(.3,.2),(.15,.10)])
    recovered=np.linalg.lstsq(scans,scans@q,rcond=None)[0]
    dark=brentq(lambda d:ratio(clicks(single,dark=d))-.005,0,.1)
    c=clicks(single)
    # A click on A alone triggers B with probability x.
    x=.005*(c[1]+c[2])/(1.005*c[1])
    # Two alternating brightness regimes; compare same- and next-trial baselines.
    high,low=.12,.04
    lag=(high*low)/((high+low)/2)**2
    # Clock-wide busy flag: only fraction f of trials are live for both arms.
    f=.8
    envelope=np.array([.15,.55,.30])
    wave=np.sqrt(envelope)
    orth=wave*np.array([1,-1,1])
    return dict(single_output=dict(keep=prob/finite(2),events=clicks(single).tolist()),
                ratio_vs_g2=dict(number_ratio=double[2]/double[1],g2=moments(double),click_ratio=ratio(clicks(double))),
                loss_arms=[ratio(clicks(double,a,b)) for a,b in [(.3,.2),(.15,.1),(.4,.1)]],
                hbt_null=dict(max_click_error=float(max(abs(m@(p-q)))),p=p.tolist(),q=q.tolist(),g2_gap=abs(moments(p)-moments(q))),
                scan=dict(rank=int(np.linalg.matrix_rank(scans)),condition=float(np.linalg.cond(scans)),reconstruction_error=float(max(abs(recovered-q)))),
                dark=dark,crosstalk=x,lag_normalization=lag,shared_live_enhancement=1/f,
                envelope=dict(time_prob=abs(orth)**2,hom_overlap=float(abs(wave@orth)**2)))

if __name__=='__main__':
    print(json.dumps(run(),default=lambda x:x.tolist(),indent=2))
