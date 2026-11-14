"""From repository root: python -m experiments.run_v085"""
import json
from pathlib import Path
from models.fair_composite_null_v085 import summary
if __name__=="__main__":
    out=summary()
    path=Path("results/fair_composite_null_v085_recomputed.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(path.read_text())
