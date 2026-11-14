"""v0.94: two-photon mixed-state HOM with threshold detectors and independent calibration.
Synthetic research model; not a photon-history identity theory.
"""
from dataclasses import dataclass,replace
import numpy as np

@dataclass(frozen=True)
class Config:
    eta_a:float=.74
    eta_b:float=.68
    dark_a:float=.002
    dark_b:float=.003
    w11:float=.90
    w20:float=.04
    w02:float=.04
    overlap:float=.72
    @property
    def w00(self):return 1-self.w11-self.w20-self.w02
    def validate(self):
        params=[self.eta_a,self.eta_b,self.dark_a,self.dark_b,self.w11,self.w20,self.w02,self.overlap]
        if any(not np.isfinite(x) or x<0 or x>1 for x in params) or self.w00< -1e-10:
            raise ValueError('parameters or event weights not physical')
        return self

def mixed_hom_overlap(rho1,rho2):
    a,b=np.asarray(rho1,complex),np.asarray(rho2,complex)
    if a.ndim!=2 or a.shape!=b.shape or a.shape[0]!=a.shape[1] or a.shape[0]<2:
        raise ValueError('density matrices must have same dimensions')
    for r in (a,b):
        if not np.allclose(r,r.conj().T) or not np.isclose(np.trace(r),1) or np.linalg.eigvalsh(r).min()<-1e-10:
            raise ValueError('normalized Hermitian positive density required')
    return float(np.trace(a@b).real)

def purity(rho):return mixed_hom_overlap(rho,rho)

def click_probability(n,eta,dark):
    if n not in (0,1,2) or not(0<=eta<=1 and 0<=dark<=1):
        raise ValueError('invalid threshold settings')
    return 1-(1-dark)*(1-eta)**n

def output_coincidence(n_a,n_b,p):
    p.validate()
    return click_probability(n_a,p.eta_a,p.dark_a)*click_probability(n_b,p.eta_b,p.dark_b)

def two_photon_pair_coincidence(m,p):
    if not 0<=m<=1:raise ValueError('overlap')
    c11=output_coincidence(1,1,p)
    cb=(output_coincidence(2,0,p)+output_coincidence(0,2,p))/2
    return (1-m)/2*c11+(1+m)/2*cb

def components(m,p):
    c11=output_coincidence(1,1,p)
    c20=output_coincidence(2,0,p);c02=output_coincidence(0,2,p)
    extra=.5*c11+.25*(c20+c02)
    return np.array([two_photon_pair_coincidence(m,p),extra,extra,output_coincidence(0,0,p)])

def coincidence_probability(p,far=False):
    return float(components(0 if far else p.overlap,p)@
                 np.array([p.w11,p.w20,p.w02,p.w00]))

def contrast_slope(p):
    return p.w11*(two_photon_pair_coincidence(0,p)-two_photon_pair_coincidence(1,p))

def jacobian(p,two_settings=False,step=1e-5):
    rows=[]
    for far in ((False,True) if two_settings else (False,)):
        entries=[]
        for key in ('w11','overlap'):
            x=getattr(p,key)
            f=lambda v: coincidence_probability(replace(p,**{key:v}),far)
            entries.append((f(x+step)-f(x-step))/(2*step))
        rows.append(entries)
    return np.array(rows)

def simulate_records(p,seed=9401,shots=80000,dark_frames=10000,efficiency_trials=10000,source_trials=20000):
    p.validate()
    if min(shots,dark_frames,efficiency_trials,source_trials)<=0:raise ValueError('shot counts')
    rng=np.random.default_rng(seed)
    return {'near':int(rng.binomial(shots,coincidence_probability(p))),
      'far':int(rng.binomial(shots,coincidence_probability(p,True))),
      'shots':shots,
      'dark_counts':[int(rng.binomial(dark_frames,p.dark_a)),int(rng.binomial(dark_frames,p.dark_b))],
      'dark_frames':dark_frames,
      'single_counts':[int(rng.binomial(efficiency_trials,click_probability(1,p.eta_a,p.dark_a))),
                       int(rng.binomial(efficiency_trials,click_probability(1,p.eta_b,p.dark_b)))],
      'efficiency_trials':efficiency_trials,
      'source_counts':rng.multinomial(source_trials,[p.w11,p.w20,p.w02,p.w00]).tolist(),
      'source_trials':source_trials}

def estimate_records(rec):
    d=np.asarray(rec['dark_counts'])/rec['dark_frames']
    one=np.asarray(rec['single_counts'])/rec['efficiency_trials']
    eta=(one-d)/(1-d)
    w=np.asarray(rec['source_counts'])/rec['source_trials']
    if np.any((eta<0)|(eta>1)):raise ValueError('invalid fluctuated calibration')
    p=Config(eta_a=float(eta[0]),eta_b=float(eta[1]),dark_a=float(d[0]),dark_b=float(d[1]),
             w11=float(w[0]),w20=float(w[1]),w02=float(w[2]),overlap=.5)
    cf=components(0,p);vac=cf[3]
    near=rec['near']/rec['shots'];far=rec['far']/rec['shots']
    w11=(far-vac-(w[1]+w[2])*(cf[1]-vac))/(cf[0]-vac)
    s=w11*(two_photon_pair_coincidence(0,p)-two_photon_pair_coincidence(1,p))
    return {'overlap':float((far-near)/s),'w11_from_far':float(w11),
            'w11_from_source_cal':float(w[0]),'w20':float(w[1]),'w02':float(w[2]),
            'eta_a':float(eta[0]),'eta_b':float(eta[1]),
            'dark_a':float(d[0]),'dark_b':float(d[1]),
            'near_observed':float(near),'far_observed':float(far)}

def parametric_bootstrap(rec,replications=300,seed=9402):
    if replications<20:raise ValueError('minimum 20 replicates')
    est=estimate_records(rec)
    w20,w02=est['w20'],est['w02']
    p=Config(eta_a=est['eta_a'],eta_b=est['eta_b'],dark_a=est['dark_a'],dark_b=est['dark_b'],
             w11=float(np.clip(est['w11_from_far'],.01,.98-w20-w02)),
             w20=w20,w02=w02,overlap=float(np.clip(est['overlap'],0,1)))
    rng=np.random.default_rng(seed);samples=[]
    for _ in range(replications):
        z=simulate_records(p,seed=int(rng.integers(1,2**31-1)),shots=rec['shots'],
            dark_frames=rec['dark_frames'],efficiency_trials=rec['efficiency_trials'],
            source_trials=rec['source_trials'])
        samples.append(estimate_records(z)['overlap'])
    return {'point':est,'bootstrap_count':replications,
            'percentile_ci_95_unbounded':np.quantile(samples,[.025,.975]).tolist(),
            'bootstrap_overlap_sd':float(np.std(samples,ddof=1)),
            'refitted_calibrations_each_replication':True}

def ordinary_identity_equivalence(mode_overlap,identity_attenuation):
    if not all(0<=z<=1 for z in (mode_overlap,identity_attenuation)):raise ValueError('factors')
    m=mode_overlap*identity_attenuation
    rho1=np.diag([1.,0.]);rho2=np.diag([m,1-m])
    return {'claimed_effective_overlap':m,'ordinary_mixed_state_overlap':mixed_hom_overlap(rho1,rho2)}

if __name__=='__main__':
    p=Config()
    print('mixed state overlap',mixed_hom_overlap(np.diag([1,0]),np.diag([.72,.28])))
    print('near,far',coincidence_probability(p),coincidence_probability(p,True))
