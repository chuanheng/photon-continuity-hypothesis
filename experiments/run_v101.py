"""v1.01 GitHub companion experiment.

From repository root:
  OPENBLAS_NUM_THREADS=1 python -m experiments.run_v101
The original actually tested 38-case project is in photon_v101_complete.zip;
GitHub file contents were independently authored and are NOT byte-identical.
"""
import json
from pathlib import Path
from models.hierarchical_v101 import audit
if __name__=="__main__":
    result=audit(outer=40,repeats=(1,2,10),draws=240,seed=101000)
    p=Path("results/hierarchical_v101_recomputed.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:{m:{field:v[m][field] for field in
        ("covered","mean","rmse","mean_width")}
        for m in ("plugin","joint")}
        for k,v in result["results"].items()},indent=2,ensure_ascii=False))
