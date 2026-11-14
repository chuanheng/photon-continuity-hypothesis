"""v0.96 GitHub companion: exact ideal Fock |2,1> splitter probabilities,
matched-trigger noise monitoring, PNR category calibration and two estimands.
Synthetic math only; complete 44-case tested package is the downloadable ZIP.
"""
from dataclasses import dataclass, replace
from math import comb, factorial
import numpy as np
from models.mixed_hom_v094 import (Config, click_probability,
    two_photon_pair_coincidence,source_component_probabilities,
    estimate_records as old_estimator)

def fock_split(na,nb):
    if not isinstance(na,int) or not isinstance(nb,int) or min(na,nb)<0 or na+nb>10:
        raise ValueError('occupancies must be nonnegative integers with sum <= 10')
    N=na+nb
    output=[]
    for k in range(N+1):
        coeff=sum(comb(na,j)*comb(nb,k-j)*(-1)**(nb-k+j)
            for j in range(max(0,k-nb),min(na,k)+1))
        output.append(coeff**2*factorial(k)*factorial(N-k)/
                      (factorial(na)*factorial(nb)*2**N))
    return np.asarray(output,float)

def distinguishable_split_three():
    return np.asarray([comb(3,k)/8 for k in range(4)],float)

def n_click(n,eta,dark):
    if not isinstance(n,int) or n<0 or not 0<=eta<=1 or not 0<=dark<=1:
        raise ValueError('invalid click setting')
    return 1-(1-dark)*(1-eta)**n

def triple_click(p,near=True):
    distribution=fock_split(2,1) if near else distinguishable_split_three()
    return float(sum(v*n_click(k,p.eta_a,p.dark_a)*
                      n_click(3-k,p.eta_b,p.dark_b)
                     for k,v in enumerate(distribution)))

@dataclass(frozen=True)
class Parameters:
    detector:Config=Config()
    triplet_fraction:float=.065
    extra_click:float=.014
    phase_step:float=.095
    blocks:int=40
    def check(self):
        self.detector.validate()
        if not 0<=self.triplet_fraction<=self.detector.w11 or not 0<=self.extra_click<1 or self.phase_step<0 or self.blocks<2:
            raise ValueError('invalid physical parameters')
        return self

def optical_probs(p,f,q,mode):
    p.validate()
    if not 0<=f<=p.w11 or not 0<=q<1 or not 0<=mode<=1:
        raise ValueError('invalid optics')
    weights=np.array([p.w11-f,p.w20,p.w02,p.w00])
    near=source_component_probabilities(mode,p)@weights+f*triple_click(p,True)
    far=source_component_probabilities(0,p)@weights+f*triple_click(p,False)
    return np.array([near+q*(1-near),far+q*(1-far)])

def optical_jacobian(p=Config(),f=.065,q=.014,m=.55,h=1e-5):
    a=np.array([m,f,q],float)
    cols=[]
    for j in range(3):
        plus=a.copy();minus=a.copy()
        plus[j]+=h;minus[j]-=h
        cols.append((optical_probs(p,plus[1],plus[2],plus[0])-
                    optical_probs(p,minus[1],minus[2],minus[0]))/(2*h))
    return np.column_stack(cols)

def synthetic_record(config=Parameters(),seed=9601,shots=25000,
                     source_trials=50000,bg_trials=60000,
                     dark_frames=50000,single_trials=50000,phase=None):
    config.check()
    if min(shots,source_trials,bg_trials,dark_frames,single_trials)<=0:
        raise ValueError('positive trials required')
    p=config.detector;rng=np.random.default_rng(seed)
    if phase is None:
        phase=np.r_[0.,rng.normal(0,config.phase_step,config.blocks-1)].cumsum()
    else:
        phase=np.asarray(phase,float)
        if len(phase)!=config.blocks:raise ValueError('phase length')
    factor=float(np.mean(np.exp(-abs(phase))))
    mbar=p.overlap*factor
    near,far=optical_probs(p,config.triplet_fraction,config.extra_click,mbar)
    source=rng.multinomial(source_trials,[p.w11-config.triplet_fraction,p.w20,p.w02,p.w00,config.triplet_fraction])
    dark=rng.binomial(dark_frames,[p.dark_a,p.dark_b])
    single=rng.binomial(single_trials,[click_probability(1,p.eta_a,p.dark_a),
                                       click_probability(1,p.eta_b,p.dark_b)])
    monitor_prob=p.dark_a*p.dark_b+config.extra_click*(1-p.dark_a*p.dark_b)
    bg=rng.binomial(bg_trials,monitor_prob)
    counts=rng.binomial(shots,[near,far])
    return dict(near=int(counts[0]),far=int(counts[1]),shots=shots,
                source_counts=source.tolist(),source_trials=source_trials,
                dark_counts=dark.tolist(),dark_frames=dark_frames,
                single_counts=single.tolist(),single_trials=single_trials,
                matched_bg_count=int(bg),matched_bg_trials=bg_trials,
                phase_monitor=phase.tolist(),true_mean=mbar,
                true_intrinsic=p.overlap)

def infer(record):
    dark=np.array(record['dark_counts'])/record['dark_frames']
    eta=(np.array(record['single_counts'])/record['single_trials']-dark)/(1-dark)
    counts=np.array(record['source_counts'])/record['source_trials']
    if len(counts)!=5 or np.any((eta<0)|(eta>1)):
        raise ValueError('calibration')
    p=Config(eta_a=float(eta[0]),eta_b=float(eta[1]),
       dark_a=float(dark[0]),dark_b=float(dark[1]),
       w11=float(counts[0]+counts[4]),w20=float(counts[1]),w02=float(counts[2]),overlap=.5)
    f=float(counts[4]);bg=record['matched_bg_count']/record['matched_bg_trials']
    q=(bg-dark[0]*dark[1])/(1-dark[0]*dark[1])
    if not 0<=q<1:raise ValueError('q')
    cnear=(record['near']/record['shots']-q)/(1-q)
    cfar=(record['far']/record['shots']-q)/(1-q)
    slope=two_photon_pair_coincidence(0,p)-two_photon_pair_coincidence(1,p)
    mean=(cfar-cnear+f*(triple_click(p,True)-triple_click(p,False)))/((p.w11-f)*slope)
    factor=float(np.mean(np.exp(-abs(np.asarray(record['phase_monitor'])))))
    return dict(mean_overlap=float(mean),intrinsic_overlap=float(mean/factor),
       drift_factor=factor,triplet=f,online_click=float(q),detector=p)

def naive_old_estimator(record):
    r=dict(record);c=record['source_counts']
    r['source_counts']=[c[0]+c[4],c[1],c[2],c[3]]
    r['efficiency_trials']=record['single_trials']
    return float(old_estimator(r)['overlap'])

def parametric_bootstrap(record,B=99,seed=9602):
    if B<20:raise ValueError('minimum 20 resamples')
    est=infer(record);p=replace(est['detector'],
        overlap=float(np.clip(est['intrinsic_overlap'],0,1)))
    cfg=Parameters(p,est['triplet'],est['online_click'],0,len(record['phase_monitor']))
    rng=np.random.default_rng(seed);values=[]
    for _ in range(B):
        new=synthetic_record(cfg,int(rng.integers(1,2**31-1)),record['shots'],
             record['source_trials'],record['matched_bg_trials'],
             record['dark_frames'],record['single_trials'],record['phase_monitor'])
        e=infer(new);values.append([e['mean_overlap'],e['intrinsic_overlap']])
    ci=np.quantile(values,[.025,.975],axis=0)
    return {'mean_ci':ci[:,0].tolist(),'intrinsic_ci':ci[:,1].tolist(),
      'point_mean':est['mean_overlap'],'point_intrinsic':est['intrinsic_overlap'],
      'B':B,'conditioned_exact_phase_monitor':True}
