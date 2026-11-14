"""v0.98 GitHub companion: independent source, phase and electronics calibration.
This is a synthetic identifiability model, not historical photon identity physics.
The byte-exact 34/34 locally tested source resides in photon_v098_complete.zip.
"""
from dataclasses import dataclass,asdict
import numpy as np
from models.calibration_stress_v097 import CalibrationError,corrupted_record
from models.fock_calibration_v096 import infer

@dataclass(frozen=True)
class Budget:
    pnr_per_class:int=1000
    phase_references:int=1000
    phase_repeats:int=4
    q_online_references:int=10000
    def validate(self):
        if min(self.pnr_per_class,self.phase_references,self.phase_repeats,
               self.q_online_references)<1:raise ValueError('positive calibration samples')
        return self
    @property
    def reference_shots(self):
        return 2*self.pnr_per_class+self.phase_references+self.q_online_references

def confusion(error):
    error.validate()
    c=np.eye(5)
    c[0,0]=1-error.pnr_pair_to_triplet;c[0,4]=error.pnr_pair_to_triplet
    c[4,0]=error.pnr_triplet_to_pair;c[4,4]=1-error.pnr_triplet_to_pair
    return c

def external_references(record,error,budget,seed):
    budget.validate()
    rng=np.random.default_rng(seed)
    c=confusion(error)
    count0=rng.multinomial(budget.pnr_per_class,c[0])
    count4=rng.multinomial(budget.pnr_per_class,c[4])
    ref=rng.normal(error.phase_bias,error.phase_noise_sd,budget.phase_references)
    phase=np.asarray(record['true_phase'],float)
    observed_phase=phase[:,None]+error.phase_bias+rng.normal(
       0,error.phase_noise_sd,(len(phase),budget.phase_repeats))
    # Additional special reference matches ONLINE electronic triggering.
    # This is a strong experimental assumption, not ordinary dark frames.
    from models.fock_calibration_v096 import Parameters
    p=Parameters().detector
    q_online=Parameters().extra_click
    pbg=p.dark_a*p.dark_b
    p_click=pbg+q_online*(1-pbg)
    matched=int(rng.binomial(budget.q_online_references,p_click))
    return dict(row0=count0.tolist(),row4=count4.tolist(),
       n=budget.pnr_per_class,phase_bias=float(ref.mean()),
       phase_noise_sd=float(ref.std(ddof=1)) if len(ref)>1 else float('nan'),
       phase_observations=observed_phase.tolist(),
       online_count=matched,online_trials=budget.q_online_references)

def source_inverse(observed,refs):
    c=np.eye(5)
    c[0]=np.asarray(refs['row0'])/refs['n']
    c[4]=np.asarray(refs['row4'])/refs['n']
    cond=np.linalg.cond(c)
    if not np.isfinite(cond) or cond>100:raise ValueError('singular PNR response')
    out=np.linalg.solve(c.T,np.asarray(observed,float))
    if (out<-1e-8).any():raise ValueError('unphysical PNR inverse')
    return out,cond

def corrected_inference(record,refs):
    counts,cond=source_inverse(record['source_counts'],refs)
    corrected=dict(record)
    corrected['source_counts']=counts.tolist()
    corrected['phase_monitor']=(np.asarray(refs['phase_observations']).mean(axis=1)
                                -refs['phase_bias']).tolist()
    corrected['matched_bg_count']=refs['online_count']
    corrected['matched_bg_trials']=refs['online_trials']
    x=infer(corrected)
    x['pnr_condition_number']=float(cond)
    x['phase_bias_calibrated']=refs['phase_bias']
    return x

def one_trial(error=CalibrationError(.15,0,.3,0,-.004),
              budget=Budget(),seed=9811):
    record=corrupted_record(seed=seed,err=error)
    reference=external_references(record,error,budget,seed+3)
    old=infer(record)
    fixed=corrected_inference(record,reference)
    return {'true_intrinsic':record['true_intrinsic'],
        'true_period':record['true_mean'],
        'naive_intrinsic':old['intrinsic_overlap'],
        'corrected_intrinsic':fixed['intrinsic_overlap'],
        'naive_period':old['mean_overlap'],
        'corrected_period':fixed['mean_overlap'],
        'reference_shots':budget.reference_shots,
        'phase_repeat_reads':len(record['true_phase'])*budget.phase_repeats}

def paired_audit(n=300,budgets=(100,1000,10000),seed=9800):
    if n<2:raise ValueError('n>=2')
    errors=CalibrationError(.15,0,.3,0,-.004)
    results={}
    for b in budgets:
        budget=Budget(b,b,max(1,b//500),10*b)
        records=[];failed=0
        for i in range(n):
            try:records.append(one_trial(errors,budget,seed+17*i))
            except (ValueError,np.linalg.LinAlgError,ZeroDivisionError):failed+=1
        if not records:raise ValueError('all trials invalid')
        metrics={}
        for name in ('naive_intrinsic','corrected_intrinsic'):
            vals=np.asarray([r[name] for r in records])
            diff=vals-.72
            metrics[name]={'mean':float(vals.mean()),'bias':float(diff.mean()),
               'rmse':float(np.sqrt(np.mean(diff**2)))}
        results[str(b)]={'reference_shots':budget.reference_shots,
          'phase_repeat_reads':40*budget.phase_repeats,
          'valid':len(records),'failed':failed,'metrics':metrics}
    return {'version':'v0.98','synthetic_only':True,'results':results,
       'caveat':'Corrected point estimation only; no demonstrated 95-percent confidence interval coverage.'}
