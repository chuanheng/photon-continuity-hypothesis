"""Recompute the v0.96 companion synthetic experiment from repository root.

The full 44-case local executed version and all 60 detailed records are
provided in the attached photon_v096_complete.zip.
"""
import json
from pathlib import Path
import numpy as np
from models.fock_calibration_v096 import (
    synthetic_record,infer,naive_old_estimator,parametric_bootstrap,
    fock_split,distinguishable_split_three,triple_click,optical_jacobian,
    Config
)

def main(outer=60,B=99,seed=96000):
    rng=np.random.default_rng(seed)
    cases=[]
    for i in range(outer):
        record=synthetic_record(seed=int(rng.integers(1,2**31-1)))
        fit=parametric_bootstrap(record,B=B,seed=seed+i+1)
        true_mean=record['true_mean']
        cases.append({'i':i,'intrinsic_est':fit['point_intrinsic'],
                      'mean_est':fit['point_mean'],
                      'period_truth':true_mean,
                      'old_est':naive_old_estimator(record),
                      'intrinsic_covered':fit['intrinsic_ci'][0]<=.72<=fit['intrinsic_ci'][1],
                      'period_covered':fit['mean_ci'][0]<=true_mean<=fit['mean_ci'][1]})
    result={'version':'v0.96','outer':outer,'B':B,'records':cases,
       'fock_21':fock_split(2,1).tolist(),
       'three_distinguishable':distinguishable_split_three().tolist(),
       'near_triplet_click':triple_click(Config(),True),
       'far_triplet_click':triple_click(Config(),False),
       'jacobian_2by3':optical_jacobian().tolist(),
       'intrinsic_covered':sum(x['intrinsic_covered'] for x in cases),
       'period_covered':sum(x['period_covered'] for x in cases),
       'mean_corrected_intrinsic':float(np.mean([x['intrinsic_est'] for x in cases])),
       'mean_old':float(np.mean([x['old_est'] for x in cases])),
       'mean_true_period':float(np.mean([x['period_truth'] for x in cases])),
       'mean_corrected_period':float(np.mean([x['mean_est'] for x in cases])),
       'science_status':'correctly specified synthetic model with oracle perfect phase monitor'}
    output=Path('results/fock_calibration_v096_recomputed.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','jacobian_2by3')},indent=2))
    return result
if __name__=='__main__':main()
