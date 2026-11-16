"""Run from repository root: python -m experiments.run_v079"""
import json
from pathlib import Path
from models.identifiability_v079 import summary
if __name__=="__main__":
    path=Path("results/identifiability_v079_recomputed.json")
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(summary(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(path.read_text())
