"""Run from repository root: python -m experiments.run_v078"""
import json
from pathlib import Path
from models.loss_dephasing_v078 import summary
if __name__ == '__main__':
    p=Path('results/loss_dephasing_v078_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps({'version':'v0.78','not_QED':True,**summary()},indent=2)+'\n',encoding='utf-8')
    print(p.read_text())
