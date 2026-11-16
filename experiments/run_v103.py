"""Regenerate v1.03 GitHub companion synthetic HOM audit.

Requires repo root with v1.02 companion model:
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v103
This independent companion is not byte identical to the actual tested local ZIP.
"""
import json
from pathlib import Path
from dataclasses import replace
import numpy as np
from models.hyperposterior_v103 import infer
from models.continuous_calibration_v102 import Setup,simulate

def case(name,n,settings,seed,outlier_frac=0.,outlier_sd=0.,draws=120):
    rows=[]
    for i in range(n):
        seed_i=seed+19*i;rec=simulate(seed_i,settings)
        if outlier_frac:
            rng=np.random.default_rng(seed_i+400007)
            mask=rng.random(rec['y'].shape)<outlier_frac
            rec['y']=rec['y']+mask*rng.normal(0,outlier_sd,rec['y'].shape)
        fit=infer(rec,settings,draws,seed+80000+19*i)
        x={'seed':seed_i,'hyper_ess':fit['hyper_ess']}
        for method in ('plugin','joint'):
            z=fit[method];lo,hi=z['ci95']
            x[method]={'mean':z['mean'],'ci95':z['ci95'],
                'covered':bool(lo<=settings.M<=hi),'width':z['width']}
        rows.append(x)
    out={}
    for method in ('plugin','joint'):
        e=np.array([r[method]['mean'] for r in rows])
        out[method]={'covered':int(sum(r[method]['covered'] for r in rows)),
           'mean_estimate':float(e.mean()),
           'RMSE':float(np.sqrt(np.mean((e-settings.M)**2))),
           'mean_ci_width':float(np.mean([r[method]['width'] for r in rows]))}
    return {'name':name,'n':n,'methods':out,
       'median_hyper_ess':float(np.median([r['hyper_ess'] for r in rows])),
       'min_hyper_ess':float(np.min([r['hyper_ess'] for r in rows])),
       'rows':rows}
if __name__=='__main__':
    s=Setup()
    report={'version':'v1.03','synthetic_only':True,'cases':{
       'baseline':case('baseline',70,s,103000),
       'high_variance':case('high_variance',50,replace(s,walk_sd=.18,read_sd=.24,bias=.08),103500),
       'non_gaussian_outliers':case('5% Gaussian mixture outliers',50,s,104000,.05,.55)}}
    p=Path('results/hyperposterior_v103_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:{'plugin':v['methods']['plugin'],'joint':v['methods']['joint'],
      'median_hyper_ess':v['median_hyper_ess']} for k,v in report['cases'].items()},indent=2))
