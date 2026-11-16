"""Reproduce full v0.84 study from repository root: python -m experiments.run_v084"""
import json
from pathlib import Path
from models.robustness_v084 import audit_outer
if __name__=='__main__':
    results=audit_outer()
    path=Path('results/robustness_v084_recomputed.json')
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:{name:val for name,val in entry.items() if name!='pvalues'}
       for k,entry in results['scenario_results'].items()},indent=2))
