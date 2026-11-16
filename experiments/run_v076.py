"""Run v0.76 from repository root: python -m experiments.run_v076"""
import json
from pathlib import Path
from models.eft_identity_v076 import summary
data={"version":"v0.76","not_QED":True,**summary()}
path=Path("results/eft_identity_v076_recomputed.json")
path.parent.mkdir(exist_ok=True,parents=True)
path.write_text(json.dumps(data,indent=2),encoding="utf-8")
print(path.read_text())
