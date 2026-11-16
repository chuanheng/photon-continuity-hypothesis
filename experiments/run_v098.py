"""Run v0.98 joint calibration cost study from repo root.

python -m experiments.run_v098
"""
import json
from pathlib import Path
from models.joint_calibration_v098 import paired_audit
if __name__=="__main__":
    result=paired_audit(n=300,budgets=(100,1000,10000),seed=9800)
    path=Path("results/joint_calibration_v098_recomputed.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result["results"],indent=2))
