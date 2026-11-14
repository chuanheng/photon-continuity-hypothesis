"""v0.99 GitHub companion: conditional joint calibration bootstrap.

The actual 31/31 locally executed source is in photon_v099_complete.zip.
This independent implementation uses the separately authored GitHub interfaces
from models/fock_calibration_v096.py, calibration_stress_v097.py, and
joint_calibration_v098.py. No remote CI result is claimed.
"""
from dataclasses import dataclass,asdict
import numpy as np
from models.joint_calibration_v098 import Budget,external_references,corrected_inference,source_inverse
from models.calibration_stress_v097 import CalibrationError,corrupted_record
from models.fock_calibration_v096 import Parameters,synthetic_record
from models.mixed_hom_v094 import Config

@dataclass(frozen=True)
class Design:
    n:int=1000
    phase_repeats:int=2
    def budget(self):return Budget(self.n,self.n,self.phase_repeats,10*self.n)
    @property
    def shots(self):return self.budget().reference_shots

def fitted(record,refs):
    point=corrected_inference(record,refs)
    counts,cond=source_inverse(record['source_counts'],refs)
    w=np.asarray(counts,float)/record['source_trials']
    d=np.asarray(record['dark_counts'],float)/record['dark_frames']
    eta=(np.asarray(record['single_counts'])/record['single_trials']-d)/(1-d)
    baseline=d[0]*d[1]
    q=(refs['online_count']/refs['online_trials']-baseline)/(1-baseline)
    phase=np.asarray(refs['phase_observations']).mean(axis=1)-refs['phase_bias']
    if min(w)<-1e-9 or not 0<=q<1:raise ValueError('invalid fitted source/electronics')
    return {'point':point,'w':w,'eta':eta,'dark':d,'q':float(q),
            'phase':phase,'phase_bias':float(refs['phase_bias']),
            'phase_sd':float(refs['phase_noise_sd']),'condition':float(cond)}

def replicate(record,refs,seed,nphase):
    f=fitted(record,refs)
    rng=np.random.default_rng(seed)
    w=f['w']
    params=Config(eta_a=float(f['eta'][0]),eta_b=float(f['eta'][1]),
        dark_a=float(f['dark'][0]),dark_b=float(f['dark'][1]),
        w11=float(w[0]+w[4]),w20=float(w[1]),w02=float(w[2]),
        overlap=float(np.clip(f['point']['intrinsic_overlap'],.001,.999)))
    tr=Parameters(params,float(w[4]),float(f['q']),0.,len(f['phase']))
    r=synthetic_record(tr,seed=int(rng.integers(1,2**31-1)),
        shots=record['shots'],source_trials=record['source_trials'],
        bg_trials=record['matched_bg_trials'],
        dark_frames=record['dark_frames'],single_trials=record['single_trials'],
        phase=f['phase'])
    matrix=np.eye(5)
    matrix[0]=np.asarray(refs['row0'])/refs['n']
    matrix[4]=np.asarray(refs['row4'])/refs['n']
    noisy=np.zeros(5,int)
    for i,n in enumerate(r['source_counts']):
        noisy+=rng.multinomial(n,matrix[i])
    r['source_counts']=noisy.tolist()
    r['true_phase']=f['phase'].tolist()
    r['phase_monitor']=(f['phase']+f['phase_bias']+
        rng.normal(0,f['phase_sd'],len(f['phase']))).tolist()
    r['phase_reference_count']=nphase
    rows=[rng.multinomial(refs['n'],matrix[j]).tolist() for j in (0,4)]
    phase_zero=rng.normal(f['phase_bias'],f['phase_sd'],nphase)
    reads=f['phase'][:,None]+f['phase_bias']+rng.normal(0,f['phase_sd'],
        np.asarray(refs['phase_observations']).shape)
    base=params.dark_a*params.dark_b
    online=rng.binomial(refs['online_trials'],base+f['q']*(1-base))
    refnew={'row0':rows[0],'row4':rows[1],'n':refs['n'],
        'phase_bias':float(phase_zero.mean()),
        'phase_noise_sd':float(phase_zero.std(ddof=1)),
        'phase_observations':reads.tolist(),
        'online_count':int(online),'online_trials':refs['online_trials']}
    return r,refnew

def joint_interval(record,refs,B=79,seed=9901,nphase=1000):
    if B<20 or nphase<2:raise ValueError('B>=20 and phase reference >=2')
    point=fitted(record,refs)['point']
    rng=np.random.default_rng(seed);samples=[];failures=0
    for _ in range(B):
        try:
            a,b=replicate(record,refs,int(rng.integers(1,2**31-1)),nphase)
            fit=corrected_inference(a,b)
            samples.append([fit['intrinsic_overlap'],fit['mean_overlap']])
        except (ValueError,np.linalg.LinAlgError,ZeroDivisionError):
            failures+=1
    if len(samples)<B/2:raise ValueError('too many invalid replicates')
    arr=np.array(samples);endpoints=np.quantile(arr,[.025,.975],axis=0)
    return {'intrinsic':float(point['intrinsic_overlap']),
       'period':float(point['mean_overlap']),
       'intrinsic_ci':endpoints[:,0].tolist(),
       'period_ci':endpoints[:,1].tolist(),
       'valid':len(samples),'invalid':failures,
       'fixed_plugin_true_phase':True}

def one_dataset(n=1000,B=79,seed=99000):
    design=Design(n,max(1,n//500))
    error=CalibrationError(.15,0,.3,0,-.004)
    record=corrupted_record(seed=seed,err=error)
    refs=external_references(record,error,design.budget(),seed+3)
    result=joint_interval(record,refs,B,seed+17,nphase=n)
    lo,hi=result['intrinsic_ci'];a,b=result['period_ci']
    result.update({'intrinsic_truth':.72,'period_truth':record['true_mean'],
        'intrinsic_covered':bool(lo<=.72<=hi),
        'period_covered':bool(a<=record['true_mean']<=b)})
    return result

def audit(outer=60,B=79,budgets=(100,1000,10000),seed=99000):
    if outer<2:raise ValueError('outer>=2')
    out={}
    for n in budgets:
        rows=[];failed=0
        for i in range(outer):
            try:rows.append(one_dataset(n,B,seed+1009*i))
            except (ValueError,ZeroDivisionError,np.linalg.LinAlgError):failed+=1
        if not rows:raise ValueError('no valid simulations')
        arr=np.asarray([row['intrinsic'] for row in rows])
        out[str(n)]={'reference_shots':13*n,
           'extra_phase_reads':40*max(1,n//500),
           'outer_valid':len(rows),'outer_invalid':failed,
           'intrinsic_coverage':float(np.mean([r['intrinsic_covered'] for r in rows])),
           'period_coverage':float(np.mean([r['period_covered'] for r in rows])),
           'mean_estimate':float(arr.mean()),
           'rmse':float(np.sqrt(np.mean((arr-.72)**2))),
           'rows':rows}
    return {'version':'v0.99','synthetic_only':True,'budgets':out,
       'limitation':'conditional plug-in path, NOT a latent-state joint posterior'}
