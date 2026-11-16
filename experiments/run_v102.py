"""GitHub companion: main and former-v1.01-outside-grid synthetic audits.

Run from repository root: OPENBLAS_NUM_THREADS=1 python -m experiments.run_v102
The exact 37-test executed source and full 120-dataset records are in
the downloadable local photon_v102_complete.zip; byte identity not claimed.
"""
import json
from pathlib import Path
from dataclasses import replace
from models.continuous_calibration_v102 import Setup,audit,jacobian

if __name__=="__main__":
    s=Setup()
    base=audit(outer=80,draws=180,seed=102000,s=s)
    stress=audit(outer=40,draws=180,seed=102500,
                 s=replace(s,walk_sd=.18,read_sd=.24,bias=.08))
    import numpy as np
    j=jacobian()
    result={'version':'v1.02','main':base,'outside_former_grid':stress,
      'jacobian':j.tolist(),'rank':int(np.linalg.matrix_rank(j)),
      'method':'continuous sensor hyper MLE plug-in; calibrated detector/source nuisance particles',
      'warning':'not fully joint hyperparameter posterior and not historical photon identity evidence'}
    dest=Path('results/continuous_calibration_v102_recomputed.json')
    dest.parent.mkdir(exist_ok=True,parents=True)
    dest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({name:{k:value[k] for k in
       ('outer','covered','mean','rmse','mean_width','mean_hyper')}
       for name,value in [('baseline',base),('outside_grid',stress)]},indent=2))
