"""Run synthetic joint-bootstrap experiment from GitHub repository root.

GitHub companion source differs from the exact locally tested ZIP source.
Outer=60 per budget and B=79 inner joint-resampling replicates.
"""
import json
from pathlib import Path
from models.joint_uncertainty_v099 import audit
if __name__=='__main__':
    result=audit(outer=60,B=79,budgets=(100,1000,10000),seed=99000)
    dest=Path('results/joint_uncertainty_v099_recomputed.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:{f:v[f] for f in ('intrinsic_coverage','period_coverage','mean_estimate','rmse','outer_valid','outer_invalid')}
           for k,v in result['budgets'].items()},indent=2))
