"""Event audit and calibration design; run from the repo root."""
from collections import Counter
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta, binomtest, norm
from v622_v631.detector import simulate

ROOT=Path(__file__).parent
TRANSMISSION=np.exp(-2.70*.277810274566*.1)
REST=510.99895

def ci(k,n,alpha=.05):
    return [float(beta.ppf(alpha/2,k,n-k+1)) if k else 0.,
            float(beta.ppf(1-alpha/2,k+1,n-k)) if k<n else 1.]

def traces():
    runs=[json.loads((ROOT/f'trace_{s}.json').read_text()) for s in (622628,632641)]
    old=json.loads((ROOT.parent/'v622_v631/geant.json').read_text())
    primaries=[[e for e in run['events'] if e['parent']==0] for run in runs]
    angles=[step['angle'] for e in primaries[0] for step in e['steps']]
    counts=[len(p) for p in primaries]
    energies=[e['energy'] for e in primaries[0]]
    singles=np.array(sum((r['single_losses'] for r in runs),[]))
    loss=60-60/(1+60/REST*(1-np.cos(np.deg2rad(singles[:,0]))))
    n=sum(r['incident'] for r in runs)
    k=sum(counts)
    unique=sum(len(set(e['event'] for e in r['events'])) for r in runs)
    secondary=sum(sum(e['parent']!=0 for e in r['events']) for r in runs)
    return [
      dict(step_angles_range_deg=[min(angles),max(angles)],exit_energy_range=[min(energies),max(energies)],
           largest_exit_angle=max(e['exit_angle'] for e in primaries[0]),path_counts=[
           [e['event'],[s['process'] for s in e['steps']]] for e in primaries[0]]),
      dict(n_single=len(singles),free_max_3deg=60-60/(1+60/REST*(1-np.cos(np.deg2rad(3)))),
           observed_max_loss=float(max(singles[:,1])),max_abs_free_residual=float(max(abs(singles[:,1]-loss))),
           single_over_gate=int(sum(singles[:,1]>=2))),
      dict(counts=counts,paths_by_seed=[dict(Counter("/".join(step["process"] for step in e["steps"]) for e in sample)) for sample in primaries],replay_forward_difference=runs[0]['counts']['primary_forward']-old['forward'],
           replay_line_difference=runs[0]['counts']['primary_line']-old['forward_line'],
           replay_selected_difference=counts[0]-old['selected'],combined_rate=k/n,
           ci=ci(k,n),equal_rate_conditional_p=binomtest(counts[0],k,.5).pvalue),
      dict(secondary_selected=secondary,events_with_any_selected=unique,tracks_selected=k+secondary,
           secondary_event_upper=-np.expm1(np.log(.05)/n) if secondary==0 else None),
      dict(pilot_rate=k/n,incident_for_10pct_relative_se=int(np.ceil((1-k/n)/(.1**2*k/n))),
           incident_at_pilot_lower=int(np.ceil((1-ci(k,n)[0])/(.1**2*ci(k,n)[0]))))]

def drift():
    time=np.arange(4)-1.5
    blank=[0,3]; foil=[1,2]
    def residual(curve):
        return float(TRANSMISSION*(curve[foil].mean()-curve[blank].mean()))
    hazard=norm.cdf(-4)*(1+.05*time)
    return dict(linear_bias=residual(hazard),quadratic_bias=residual(hazard+1e-6*time**2),
                ab_preceding_bias=TRANSMISSION*(hazard[1]-hazard[0]))

def calibration():
    counts=[0,36,87]
    return dict(exposure=2700000,synthetic_counts=counts,
                simultaneous_intervals=[ci(k,2700000,.05/3) for k in counts])

def geometry():
    rows=[]
    for h in (.05,.10):
        for angle in (1.5,3.):
            rates=[simulate(h,.5,angle,s,13).sum(axis=0)[0] for s in range(640,644)]
            rows.append(dict(h_cm=h,angle_deg=angle,rate=np.mean(rates),
                             integration_se=np.std(rates,ddof=1)/2))
    return rows

def linewidth():
    from itertools import product
    rows=[]
    for width,shift in product((0.,.15),(-.05,.05)):
        sigma=np.hypot(.5,width)
        leak=TRANSMISSION*(norm.cdf((-2-shift)/sigma)-norm.cdf((-25-shift)/sigma))
        rows.append(dict(source_sigma=width,shift=shift,rate=leak))
    return dict(corners=rows,conditional_range=[min(r['rate'] for r in rows),max(r['rate'] for r in rows)])

def identifiability(rows):
    ordinary=np.array([r['rate'] for r in rows])
    leak=np.exp(-2.7*.277810274566*np.array([r['h_cm'] for r in rows]))
    design=np.column_stack((ordinary/ordinary.max(),leak))
    def gap(template):
        residual=template-design@np.linalg.lstsq(design,template,rcond=None)[0]
        return np.linalg.norm(residual)/np.linalg.norm(template)
    trial=np.array([1.,1.,2.,2.])
    return dict(shared_template_residual=gap(design[:,0]),linear_thickness_residual=gap(trial),
                free_setting_offsets_residual=0.,rank=int(np.linalg.matrix_rank(design)))

def run():
    rows=geometry()
    values=traces()+[drift(),calibration(),rows,linewidth(),identifiability(rows)]
    return {f'v6.{n}':v for n,v in enumerate(values,32)}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
