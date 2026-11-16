"""v0.97 GitHub counterpart: HOM monitor misspecification.
Uses branch models.fock_calibration_v096; separately authored from the exact
locally tested ZIP source. All generated data synthetic.
"""
from dataclasses import dataclass
import numpy as np
from models.fock_calibration_v096 import (
    Parameters,synthetic_record,infer,parametric_bootstrap,
    optical_probs,triple_click,two_photon_pair_coincidence)

@dataclass(frozen=True)
class CalibrationError:
    phase_noise_sd:float=0.
    phase_bias:float=0.
    pnr_triplet_to_pair:float=0.
    pnr_pair_to_triplet:float=0.
    q_monitor_offset:float=0.
    def validate(self):
        if self.phase_noise_sd<0 or not np.isfinite(self.phase_bias):
            raise ValueError('phase sensor error')
        if not all(0<=x<=1 for x in
            (self.pnr_triplet_to_pair,self.pnr_pair_to_triplet)):
            raise ValueError('PNR confusion')
        if not np.isfinite(self.q_monitor_offset):
            raise ValueError('reference mismatch')
        return self

def pnr_confusion_matrix(err=CalibrationError()):
    err.validate()
    c=np.eye(5)
    c[0,0]=1-err.pnr_pair_to_triplet
    c[0,4]=err.pnr_pair_to_triplet
    c[4,0]=err.pnr_triplet_to_pair
    c[4,4]=1-err.pnr_triplet_to_pair
    return c

def corrupted_record(seed=9700,err=CalibrationError(),truth=Parameters(),
                     shots=25000,source_trials=50000,
                     bg_trials=60000,dark_frames=50000,
                     single_trials=50000):
    err.validate();truth.check()
    qref=truth.extra_click+err.q_monitor_offset
    if not 0<=qref<1:raise ValueError('qref')
    original=synthetic_record(truth,seed,shots,source_trials,bg_trials,
                              dark_frames,single_trials)
    rng=np.random.default_rng(seed+104729)
    actual_phase=np.asarray(original['phase_monitor'])
    original['phase_monitor']=(actual_phase+err.phase_bias+
        rng.normal(0,err.phase_noise_sd,len(actual_phase))).tolist()
    old=np.asarray(original['source_counts'],int)
    new=np.zeros(5,int);C=pnr_confusion_matrix(err)
    for i,n in enumerate(old):
        new+=rng.multinomial(int(n),C[i])
    original['source_counts']=new.tolist()
    p=truth.detector
    baseline=p.dark_a*p.dark_b
    original['matched_bg_count']=int(rng.binomial(bg_trials,
                             baseline+qref*(1-baseline)))
    original['true_source_counts']=old.tolist()
    original['true_phase']=actual_phase.tolist()
    original['true_phase_factor']=float(np.mean(np.exp(-abs(actual_phase))))
    original['reported_phase_factor']=float(np.mean(np.exp(-abs(
        np.asarray(original['phase_monitor'])))))
    original['true_mean']=truth.detector.overlap*original['true_phase_factor']
    original['calibration_error']=err.__dict__
    return original

def population_limit(err=CalibrationError(),truth=Parameters(),seed=9719):
    """Infinite optical & calibration shot limit, conditional fixed phase path."""
    err.validate();truth.check()
    rng=np.random.default_rng(seed);n=truth.blocks
    path=np.r_[0,rng.normal(0,truth.phase_step,n-1)].cumsum()
    p=truth.detector;f=truth.triplet_fraction;q=truth.extra_click
    af=float(np.mean(np.exp(-abs(path))))
    m=p.overlap*af
    near,far=optical_probs(p,f,q,m)
    w=np.array([p.w11-f,p.w20,p.w02,p.w00,f])
    reported=w@pnr_confusion_matrix(err)
    fhat=float(reported[4]);w11hat=float(reported[0]+reported[4])
    qhat=q+err.q_monitor_offset
    near0=(near-qhat)/(1-qhat);far0=(far-qhat)/(1-qhat)
    slope=two_photon_pair_coincidence(0,p)-two_photon_pair_coincidence(1,p)
    trine=triple_click(p,True);trifar=triple_click(p,False)
    mbar=(far0-near0+fhat*(trine-trifar))/((w11hat-fhat)*slope)
    if err.phase_noise_sd==0:
        factor=np.mean(np.exp(-abs(path+err.phase_bias)))
    else:
        nodes,weights=np.polynomial.hermite.hermgauss(40)
        ns=nodes*np.sqrt(2)*err.phase_noise_sd+err.phase_bias
        factor=np.mean(np.exp(-abs(path[:,None]+ns[None,:]))@weights/np.sqrt(np.pi))
    return {'true_intrinsic':p.overlap,'true_mean':m,
        'estimated_mean':float(mbar),'estimated_intrinsic':float(mbar/factor),
        'bias_intrinsic':float(mbar/factor-p.overlap),
        'bias_mean':float(mbar-m),'true_factor':af,'reported_factor':float(factor)}

def evaluate(err=CalibrationError(),outer=24,B=49,seed=97000):
    if outer<1 or B<20:raise ValueError('sample sizes')
    rows=[]
    for i in range(outer):
        r=corrupted_record(seed+1009*i,err)
        fit=parametric_bootstrap(r,B,seed+100000+997*i)
        ic=fit['intrinsic_ci'];mc=fit['mean_ci']
        e=fit['point_intrinsic'];period=fit['point_mean']
        rows.append({'point_intrinsic':e,'point_mean':period,
          'true_mean':r['true_mean'],
          'covered_intrinsic':bool(ic[0]<=.72<=ic[1]),
          'covered_mean':bool(mc[0]<=r['true_mean']<=mc[1])})
    return {'error':err.__dict__,'outer':outer,'B':B,'rows':rows,
        'mean_intrinsic':float(np.mean([r['point_intrinsic'] for r in rows])),
        'mean_true_period':float(np.mean([r['true_mean'] for r in rows])),
        'intrinsic_coverage':float(np.mean([r['covered_intrinsic'] for r in rows])),
        'period_coverage':float(np.mean([r['covered_mean'] for r in rows]))}

SCENARIOS={
 'correct':CalibrationError(),
 'phase_noise_005':CalibrationError(phase_noise_sd=.05),
 'phase_noise_015':CalibrationError(phase_noise_sd=.15),
 'pnr_triplets_10pct':CalibrationError(pnr_triplet_to_pair=.10),
 'pnr_triplets_30pct':CalibrationError(pnr_triplet_to_pair=.30),
 'q_reference_low':CalibrationError(q_monitor_offset=-.004),
 'q_reference_high':CalibrationError(q_monitor_offset=.004),
 'combined':CalibrationError(.15,0,.30,0,-.004),
}
def audit_all(outer=24,B=49,seed=97000):
    return {'version':'v0.97','data_type':'synthetic only',
        'scenarios':{name:evaluate(err,outer,B,seed+1013*i)
            for i,(name,err) in enumerate(SCENARIOS.items())}}
