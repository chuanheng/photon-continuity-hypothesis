"""Run from repository root: python -m experiments.run_v090"""
import json
from pathlib import Path
from models.eft_audit_v090 import summary
if __name__=='__main__':
    result=summary()
    p=Path('results/eft_audit_v090_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
