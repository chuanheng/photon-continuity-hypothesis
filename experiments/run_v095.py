"""Recompute v0.95 synthetic misspecification audit from GitHub repository root.
Python 3.10+, NumPy and SciPy; 5 scenarios x 60 datasets x 79 bootstraps.
"""
import json
from pathlib import Path
from models.robustness_v095 import audit_all
if __name__=='__main__':
    data=audit_all(outer=60,inner=79,seed=95000)
    p=Path('results/robustness_v095_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(json.dumps({k:{field:d[field] for field in ('covered','coverage_intrinsic',
        'mean_estimate','bias','mean_actual_mode','coverage_actual_mean')}
        for k,d in data['scenarios'].items()},indent=2))
