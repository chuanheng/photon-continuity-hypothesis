"""Reproduce v0.83 from GitHub repository root: python -m experiments.run_v083"""
import json
from pathlib import Path
from models.calibrated_bootstrap_v083 import (
    simulate_calibration, bootstrap_with_refit,
    covariance_model_mismatch_example,
)
from models.count_hierarchy_v082 import simulate_data,profile_statistic

def main():
    calibration,_=simulate_calibration(length=120,seed=510)
    null_data=simulate_data(t=10,delta=0,seed=511)
    signal_data=simulate_data(t=10,delta=.18,seed=512)
    bootstrap=bootstrap_with_refit(null_data,calibration,replications=24,seed=513)
    params=bootstrap['calibration_fit']
    optical_parameters={'rho':params['rho'],'sigma':params['sigma']}
    signal=profile_statistic({**signal_data,**optical_parameters})
    mismatched,bias=covariance_model_mismatch_example()
    mismatch_stat=profile_statistic({**mismatched,**optical_parameters})
    result={'version':'v0.83',
       'hypothesis':'identity phase versus ordinary memory nuisance',
       'calibration':'independent noisy AR1 sensor; Kalman MLE rho,sigma; known readout sd .03',
       'bootstrap':'new sensor+photon data, re-estimate rho/sigma, refit two photon MAP models',
       'null_bootstrap':bootstrap,'signal_dataset_statistic':signal['statistic'],
       'misspecification_example':{
         'random_walk_plus_ordinary_test_bias':bias,
         'penalized_statistic':mismatch_stat['statistic'],
         'not_population_false_positive_rate':True},
       'fundamental_unidentifiability':'ordinary test-specific bias exactly absorbs delta',
       'caveats':['B=24 coarse p-value resolution 1/25',
         'sensor noise known and AR1 distribution shared, but sensor/photon trajectories independent',
         'penalized MAP rather than marginalized likelihood; simulations not QED']}
    p=Path('results/calibrated_bootstrap_v083_recomputed.json')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='null_bootstrap'},indent=2))
    print({k:v for k,v in bootstrap.items() if k not in ('null_bootstrap_stats','refitted_hyperparameters')})

if __name__=='__main__':main()
