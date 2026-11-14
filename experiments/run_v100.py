"""Recompute v1.00 Gaussian latent-state marginal HOM audit.

From repository root (NumPy, SciPy):
OPENBLAS_NUM_THREADS=1 python -m experiments.run_v100
The GitHub model/tests are independently authored companions, not byte-identical
to locally executed complete v1.00 ZIP; remote CI has not been verified.
"""
import json
from pathlib import Path
from models.latent_phase_v100 import audit
if __name__=='__main__':
    out=audit(outer=100,repeats=(1,2,20),draws=700,seed=100000)
    p=Path('results/latent_phase_v100_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:{f:v[f] for f in
       ('runs','plugin_covered','latent_covered','plugin_mean','latent_mean',
        'plugin_rmse','latent_rmse','mean_plugin_width','mean_latent_width')}
        for k,v in out['results'].items()},indent=2,ensure_ascii=False))
