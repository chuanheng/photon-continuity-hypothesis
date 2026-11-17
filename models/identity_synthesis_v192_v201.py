"""v1.92-v2.01 audit: constrained vs unconstrained Bernoulli nuisance.
Toy statistical study ONLY; not a photon-identity prediction. NumPy/SciPy.
"""
import math,json
import numpy as np
from scipy.stats import binom
SEED=20261117; ALT=.08; LO=.03; HI=.06; N=5000
CANDIDATES=(
 ('silent_label','observationally equivalent'),
 ('energy_free_hard_photon','energy conservation failure'),
 ('ordinary_dephasing','standard quantum environment'),
 ('ordinary_amplitude_damping','standard dissipative channel'),
 ('matter_memory','standard reversible quantum memory'),
 ('quasistatic_environment','standard non-Markovian noise'),
 ('mode_overlap_shift','standard nuisance reparameterization'),
 ('soft_click_excess','conditional test only with justified null envelope'))
def kl(p,q):
    if p==q:return 0.
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def profile(p,lo,hi):
    q=max(lo,min(p,hi))
    return {'best_q':q,'KL':kl(p,q)}
def threshold(n,p,alpha):
    for k in range(n+1):
        size=float(binom.sf(k-1,n,p))
        if size<=alpha:return (k,size)
    return (n+1,0.)
def run():
    unbounded=profile(ALT,.001,.999)
    bounded=profile(ALT,LO,HI)
    drift=[dict(drift=d,upper=HI+d,**profile(ALT,LO,HI+d))
           for d in (0,.005,.01,.015,.02,.025)]
    k,size=threshold(N,HI,.05);kb,sizeb=threshold(N,HI,.05/3)
    nclick=int(np.random.default_rng(SEED).binomial(N,ALT))
    return {'v1.92':{'candidate_count':len(CANDIDATES),'candidates':CANDIDATES},
      'v1.93':{'energy_deficit':2.,'allowed_closed_system':False},
      'v1.94':{'silent_label_KL':0.,'standard_environment_profile_KL':0.},
      'v1.95':{'candidate_click':ALT,'unbounded_null':unbounded,'bounded_null':bounded},
      'v1.96':{'hypothetical_reference_range':[LO,HI],'profile_KL':bounded['KL'],'physically_justified':False},
      'v1.97':{'n':N,'critical_click_count':k,'type_I':size,'exact_power':float(binom.sf(k-1,N,ALT)),'expected_LLR':N*bounded['KL']},
      'v1.98':{'drift_scan':drift,'degeneracy_threshold':ALT-HI},
      'v1.99':{'bonferroni_tests':3,'per_test_alpha':.05/3,'critical_count':kb,'type_I':sizeb,'exact_power':float(binom.sf(kb-1,N,ALT))},
      'v2.00':{'rng_seed':SEED,'observed_clicks':nclick,'one_sided_pvalue':float(binom.sf(nclick-1,N,HI)),'synthetic_not_preregistered':True},
      'v2.01':{'unique_photon_identity_prediction':False,'full_QED_model':False,'evidence_of_new_physics':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
