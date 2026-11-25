"""Matched-reference Poisson design. All calibration channels are hypothetical."""
from functools import lru_cache
import json
import numpy as np
from scipy.special import ndtr
from scipy.stats import binom,poisson
from v632_v641.model import TRANSMISSION as T

LEAK=ndtr(-4.)
SCATTER=2e-6
BACKGROUND=T*LEAK+SCATTER
ALPHA=.025
DELTA=3e-6

@lru_cache(maxsize=128)
def rejection(kmax,q):
    totals=np.arange(kmax+1)
    return binom.isf(ALPHA,totals,q).astype(int)+1

def power(n,m,sample_rate,reference_rate,q_null=None):
    """Condition on the pooled count, then integrate over its Poisson law."""
    a,b=n*sample_rate,m*reference_rate
    upper=int(poisson.isf(1e-12,a+b))
    totals=np.arange(upper+1)
    q=n/(n+m) if q_null is None else q_null
    thresholds=rejection(upper,q)
    return float(poisson.pmf(totals,a+b)@binom.sf(thresholds-1,totals,a/(a+b)))

def run():
    n=m=10_000_000
    b=BACKGROUND
    # Matching B and C requires exposures T*m and m respectively.
    match=dict(blank_exposure=T*m,scatter_control_exposure=m,expected_blank=T*m*LEAK,
               expected_scatter=m*SCATTER,matched_reference_mean=m*b,sample_null_mean=n*b)
    q=n/(n+m)
    nulls=[power(n,m,h,h) for h in (.5*b,b,2*b)]
    exact=dict(nuisance_rates=[.5*b,b,2*b],conditional_fraction=q,unconditional_sizes=nulls)
    levels=[3e6,1e7,3e7,1e8]
    exposure=dict(equal_arm_exposures=levels,powers=[power(x,x,b+DELTA,b) for x in levels])
    # Factor c is the cost of one unit of matched reference exposure.
    c=1+T
    ratio=np.sqrt(c*(b+DELTA)/b)
    budget=1e8
    choices=[1.,ratio,2.5]
    allocation=[]
    for r in choices:
        ref=budget/(r+c)
        allocation.append(dict(n_over_m=r,sample=r*ref,ref=ref,
                               variance=(b+DELTA)/(r*ref)+b/ref,
                               power=power(r*ref,ref,b+DELTA,b)))
    mismatch=[1.,1.02,1.05,1.10]
    inflated=[power(n,m,T*f*LEAK+SCATTER,b) for f in mismatch]
    bias=dict(sample_leak_multipliers=mismatch,false_positives=inflated)
    factor=1.05
    # Under 1<=f<=factor and s>=0, sample/reference <=factor.
    qrob=n*factor/(n*factor+m)
    robust=dict(allowed_ratio=factor,threshold_fraction=qrob,
                worst_endpoint_size=power(n,m,factor*b,b,qrob),
                nominal_power=power(n,m,b+DELTA,b,qrob))
    floor=(factor-1)*b
    intersection=dict(reference_rate=b,ordinary_max=factor*b,
                      largest_hidden_increment=floor,trial_increment=DELTA,
                      distance_above_ordinary=max(0.,DELTA-floor))
    # Template contamination of fraction eta of the added rate in control.
    fractions=[0.,.25,.5,1.]
    contam=dict(control_fractions=fractions,
                powers=[power(n,m,b+DELTA,b+eta*DELTA) for eta in fractions])
    # Additive background gamma per arm/day: identical means, overdispersion
    # independent between arms vs shared blockwise multiplier.
    rng=np.random.default_rng(651642)
    reps=100000
    means=rng.gamma(400.,1/400.,(2,reps))
    excess={}
    for label,ref_mean in [('shared',means[0]),('independent',means[1])]:
        x=rng.poisson(n*b*means[0]); y=rng.poisson(m*b*ref_mean)
        total=x+y
        rejected=x>=rejection(int(total.max()),q)[total]
        excess[label]=dict(size=rejected.mean(),mc_se=rejected.std()/np.sqrt(reps))
    # Identification counterexample if the matched scatter-control efficiency
    # is unknown. Match all three means with delta=0 by changing efficiency.
    eps=.9
    alternative=[LEAK,eps*SCATTER,b+DELTA]
    s_refit=SCATTER+DELTA
    efficiency=eps*SCATTER/s_refit
    ordinary=[LEAK,efficiency*s_refit,T*LEAK+s_refit]
    refit=dict(alternative=alternative,ordinary=ordinary,
               required_control_efficiency=efficiency,max_gap=max(abs(x-y) for x,y in zip(alternative,ordinary)))
    return {f'v6.{i}':v for i,v in enumerate([match,exact,exposure,allocation,bias,robust,intersection,contam,excess,refit],42)}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
