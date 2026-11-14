"""Reproduce v0.91 from GitHub repository root."""
import json
from pathlib import Path
import numpy as np
from models.absorption_emission_v091 import summary,trajectory,observables
if __name__=='__main__':
    result=summary()
    result['absorption_probability_scan']=[{
        'area':float(t),
        'atom_excitation':observables(trajectory(absorption=t)['stored'])['P_e']
    } for t in np.linspace(0,np.pi/2,11)]
    output=Path('results/absorption_emission_v091_recomputed.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
