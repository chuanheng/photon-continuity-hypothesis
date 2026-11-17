"""v2.02-v2.11: finite reference calibration, drift and statistical synthesis.
Synthetic Bernoulli tests; not QED or an identity-specific photon prediction.
Requirements: numpy, scipy. Run python -m models.identity_evidence_v202_v211
"""
import math,json
import numpy as np
from scipy.stats import norm,binom
SEED=20261117;N=5000;P0=.06;P1=.08;ALPHA=.05;REPS=3000
def kl(p,q):
    if p==q:return 0.
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def critical(n,p,alpha=.05):
    return next(k for k in range(n+2) if binom.sf(k-1,n,p)<=alpha)
def asimov(n,m,p,q):
    pooled=(n*p+m*q)/(n+m)
    return {'pooled_null':pooled,'expected_log_lr':n*kl(p,pooled)+m*kl(q,pooled)}
def simulate(m,p,q,rng):
    a=rng.binomial(N,p,size=REPS);b=rng.binomial(m,q,size=REPS)
    pooled=(a+b)/(N+m)
    z=(a/N-b/m)/np.sqrt(np.maximum(1e-30,pooled*(1-pooled)*(1/N+1/m)))
    rejection=float(np.mean(z>norm.isf(ALPHA)))
    se=math.sqrt(rejection*(1-rejection)/REPS)
    return {'rejection_fraction':rejection,'mc_se':se,'mc_95_halfwidth':1.96*se}
def visible(b,eta,dark):return dark+(1-dark)*eta*b
def run():
    rng=np.random.default_rng(SEED)
    k=critical(N,P0)
    sizes=(1000,5000,20000)
    finite={}
    for m in sizes:
        finite[str(m)]={'asimov':asimov(N,m,P1,P0),
                        'null':simulate(m,P0,P0,rng),
                        'alternative':simulate(m,P1,P0,rng)}
    drift={f'{d:.3f}':simulate(5000,P0+d,P0,rng)
           for d in (0,.005,.01,.015,.02)}
    target=visible(.08,.7,.01)
    alt_b=(target-.02)/(.98*.8)
    return {'metadata':{'seed':SEED,'n_main':N,'replicates':REPS},
      'v2.02':{'audited_candidate_count':8},
      'v2.03':{'inert_identity_kl':0.},
      'v2.04':{'fixed_reference_critical':k,'exact_type_I':float(binom.sf(k-1,N,P0)),
               'exact_power':float(binom.sf(k-1,N,P1))},
      'v2.05':{'finite_references':finite},
      'v2.06':{'joint_asimov':{str(m):finite[str(m)]['asimov'] for m in sizes}},
      'v2.07':{'drift':drift},
      'v2.08':{'detected_click':target,'alternate_b':alt_b,
                'alternate_click':visible(alt_b,.8,.02)},
      'v2.09':{'null_rates':{str(m):finite[str(m)]['null'] for m in sizes}},
      'v2.10':{'power':{str(m):finite[str(m)]['alternative'] for m in sizes}},
      'v2.11':{'identity_specific_prediction':False,'full_QED_competition':False,
                'physical_experiment':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
