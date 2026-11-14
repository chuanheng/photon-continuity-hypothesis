"""Run from GitHub repository root: python -m experiments.run_v081"""
import json
from pathlib import Path
from models.correlated_drift_v081 import summary
if __name__=='__main__':
    result=summary()
    path=Path('results/correlated_drift_v081_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
