"""v0.95 GitHub counterpart: calibrated HOM under ordinary model misspecification.

Requires models.mixed_hom_v094 on same branch. The full 30-test actually
executed source and 300-dataset numerical audit are in photon_v095_complete.zip.
These are synthetic scenarios, NOT observations of actual photons.
"""
from dataclasses import dataclass,replace
import math
import numpy as np
from models.mixed_hom_v094 import (
    Config,coincidence_probability,click_probability,
    estimate_records,parametric_bootstrap,ordinary_identity_equivalence
)

@dataclass(frozen=True)
class Stress:
    correlated_live_click:float=0.
    triple_fraction:float=0.
    mode_random_walk_step:float=0.
    def validate(self):
        if not (0<=self.correlated_live_click<1 and
                0<=self.triple_fraction<.2 and
                0<=self.mode_random_walk_step<=.5):
            raise ValueError('invalid stress parameters')
        return self

def n_photon_click(n,eta,dark):
    return 1-(1-dark)*(1-eta)**n

def triplet_coincidence(p):
    """Explicit assumption: three mutually distinguishable contamination
    photons independently choose either port with probability 1/2. Not a
    full three-identical-boson beamsplitter calculation."""
    return sum(math.comb(3,k)/8*n_photon_click(k,p.eta_a,p.dark_a)*
               n_photon_click(3-k,p.eta_b,p.dark_b) for k in range(4))

def correlated_click(p,q):
    return p+q*(1-p)

def drifted_overlap(p,step,rng,blocks=40):
    if step<0 or blocks<2:raise ValueError('drift parameters')
    path=np.r_[0,rng.normal(0,step,blocks-1)].cumsum()
    return p.overlap*np.exp(-np.abs(path))

def stressed_probabilities(p,stress,modes):
    stress.validate();p.validate()
    if stress.triple_fraction>p.w11:raise ValueError('triplet events replace source pairs')
    m=np.asarray(modes,float)
    if len(m)<2 or np.any((m<0)|(m>1)):raise ValueError('mode probabilities')
    # Remove triplets from the true pair sector; four-category source
    # calibration will mistakenly classify triplets as (1,1).
    reduced=replace(p,w11=p.w11-stress.triple_fraction)
    triple=stress.triple_fraction*triplet_coincidence(p)
    near=np.array([coincidence_probability(replace(reduced,overlap=float(v)))+triple for v in m])
    far=coincidence_probability(reduced,True)+triple
    q=stress.correlated_live_click
    return correlated_click(near,q),correlated_click(far,q)

def simulate_stressed(p=Config(),stress=Stress(),seed=9501,
    shots=16000,dark_frames=5000,efficiency_trials=5000,source_trials=10000,blocks=40):
    p.validate();stress.validate()
    if min(shots,dark_frames,efficiency_trials,source_trials,blocks-1)<=0:raise ValueError('trials')
    rng=np.random.default_rng(seed)
    source=rng.multinomial(source_trials,[p.w11,p.w20,p.w02,p.w00])
    dark=[rng.binomial(dark_frames,v) for v in (p.dark_a,p.dark_b)]
    singles=[rng.binomial(efficiency_trials,click_probability(1,e,d))
             for e,d in ((p.eta_a,p.dark_a),(p.eta_b,p.dark_b))]
    mode=drifted_overlap(p,stress.mode_random_walk_step,rng,blocks)
    near,far=stressed_probabilities(p,stress,mode)
    ns=np.full(blocks,shots//blocks,int);ns[:shots%blocks]+=1
    y_near=int(sum(rng.binomial(int(n),float(v)) for n,v in zip(ns,near)))
    y_far=int(rng.binomial(shots,float(far)))
    return {'near':y_near,'far':y_far,'shots':shots,
        'source_counts':list(map(int,source)),'source_trials':source_trials,
        'dark_counts':list(map(int,dark)),'dark_frames':dark_frames,
        'single_counts':list(map(int,singles)),'efficiency_trials':efficiency_trials,
        'true_mean_mode_overlap':float(np.average(mode,weights=ns)),
        'model_near_probability':float(np.average(near,weights=ns)),
        'model_far_probability':float(far)}

def audit_one(stress=Stress(),outer=60,inner=79,seed=95000,p=Config()):
    if outer<1 or inner<20:raise ValueError('audit size')
    rows=[]
    for i in range(outer):
        rec=simulate_stressed(p,stress,seed+i)
        fit=parametric_bootstrap(rec,replications=inner,seed=seed+100000+i)
        lo,hi=fit['percentile_ci_95_unbounded']
        est=fit['point']['overlap']
        rows.append({'index':i,'estimate':float(est),'interval':[float(lo),float(hi)],
            'covers_intrinsic':bool(lo<=p.overlap<=hi),
            'true_mean_mode_overlap':rec['true_mean_mode_overlap'],
            'covers_mean_mode':bool(lo<=rec['true_mean_mode_overlap']<=hi)})
    values=np.array([r['estimate'] for r in rows])
    hit=sum(r['covers_intrinsic'] for r in rows)
    return {'stress':stress.__dict__,'outer':outer,'inner':inner,
       'covered':hit,'coverage_intrinsic':hit/outer,
       'mean_estimate':float(values.mean()),'bias':float(values.mean()-p.overlap),
       'sd_estimate':float(values.std(ddof=1)),
       'mean_actual_mode':float(np.mean([r['true_mean_mode_overlap'] for r in rows])),
       'coverage_actual_mean':float(np.mean([r['covers_mean_mode'] for r in rows])),
       'rows':rows}

def audit_all(outer=60,inner=79,seed=95000):
    cases={'correct_model':Stress(),
       'live_correlated_click':Stress(correlated_live_click=.014),
       'unresolved_triplets':Stress(triple_fraction=.065),
       'nonstationary_mode_drift':Stress(mode_random_walk_step=.095),
       'combined_misspecification':Stress(.014,.065,.095)}
    return {'version':'v0.95','intrinsic_overlap_target':.72,
       'all_data_synthetic':True,'outer':outer,'inner_bootstraps':inner,
       'scenarios':{name:audit_one(cfg,outer,inner,seed+1000*i)
                    for i,(name,cfg) in enumerate(cases.items())},
       'caution':'Off-model bootstrap coverage is not credible. Random walk changes measured period average vs intrinsic zero-drift target.'}
