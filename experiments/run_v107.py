"""Execute the independently authored v1.07 GitHub *simplified* companion.
For all 600 real local synthetic posterior fits with sensor/PNR nuisance,
use the exact locally tested ZIP photon_v107_complete.zip.
"""
import json
from pathlib import Path
from models.gram_v107 import gram_phase_demo
from models.rho_reference_v107 import paired_demo

if __name__=="__main__":
    demo=paired_demo(n=100,seed=10701)
    gram=gram_phase_demo()
    out={'version':'v1.07','companion_known_nuisance':True,
         'paired_inferences':demo,'generic_gram_counterexample':gram,
         'not_the_same_as_local_full_model':True}
    path=Path('results/rho_gram_v107_companion_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:{'n':v['n'],'M_mean':v['mean_M'],'covered':v['covered']}
          for k,v in demo.items()},indent=2))
    print('Gram example:',json.dumps(gram,indent=2))
