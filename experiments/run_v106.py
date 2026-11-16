"""Run the independently authored v1.06 GitHub counterpart stress experiment.
For byte-exact, actually locally tested 500-trial source, use photon_v106_complete.zip.
"""
import json
from pathlib import Path
from models.continuous_partial_v106 import small_audit

if __name__=="__main__":
    out=small_audit(n=100,seed=106000,particles=160)
    path=Path("results/continuous_partial_v106_recomputed.json")
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:{"n":v["n"],"covered":v["coverage_count"],
       "mean":v["mean_estimate"],"median_ess":v["median_ess"]}
       for k,v in out.items()},indent=2))
