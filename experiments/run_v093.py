"""Reproduce v0.93 from repository root: python -m experiments.run_v093"""
import json
from pathlib import Path
import numpy as np
from models.hom_wavepackets_v093 import summary,pure_overlap,coincidence,ensemble_overlap
if __name__=="__main__":
    data=summary()
    delays=np.linspace(-3,3,121)
    data["hom_dip_curves"]={}
    for g1,g2 in ((.7,.7),(1,1),(1,2)):
        data["hom_dip_curves"][f"Gamma_{g1}_{g2}"]=[
            {"delay":float(d),"coincidence":coincidence(pure_overlap(g1,g2,delay=float(d)))}
            for d in delays]
    data["jitter_curves"]={}
    for r in (0,.5,.9,1):
        data["jitter_curves"][str(r)]=[
            {"onset_std":float(s),"mean_overlap":ensemble_overlap(onset_std=float(s),
             frequency_std=.3,arrival_correlation=r,frequency_correlation=r)}
            for s in np.linspace(0,.8,81)]
    p=Path("results/hom_wavepackets_v093_recomputed.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in data.items() if k not in ("hom_dip_curves","jitter_curves")},
                     indent=2,ensure_ascii=False))
