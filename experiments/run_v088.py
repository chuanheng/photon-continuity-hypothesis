"""Reproduce v0.88 result from GitHub repository root: python -m experiments.run_v088"""
import json
from pathlib import Path
from models.originality_process_v088 import state_readout_vs_process_readout
if __name__=="__main__":
    result=state_readout_vs_process_readout()
    path=Path('results/multitime_process_v088.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
