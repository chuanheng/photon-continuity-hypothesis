"""Regenerate a synthetic mixed-state HOM experiment from GitHub repository root.

The original fully tested 52-case local release is in photon_v094_complete.zip.
"""
import json
from dataclasses import asdict
from pathlib import Path
from models.mixed_hom_v094 import (
    Config,mixed_hom_overlap,coincidence_probability,
    simulate_records,estimate_records,parametric_bootstrap,
    jacobian,ordinary_identity_equivalence
)
import numpy as np

def main():
    p=Config()
    r=simulate_records(p,seed=9401)
    fit=estimate_records(r)
    bootstrap=parametric_bootstrap(r,replications=500,seed=9402)
    out={
        'version':'v0.94',
        'data_type':'synthetic, no laboratory measurements',
        'truth':asdict(p),'truth_w00':p.w00,
        'predicted_near':coincidence_probability(p),
        'predicted_far':coincidence_probability(p,True),
        'observed_records':r,'point_estimate':fit,
        'bootstrap':bootstrap,
        'naive_lossless_estimate_from_raw_near_coincidence':1-2*r['near']/r['shots'],
        'one_setting_rank':int(np.linalg.matrix_rank(jacobian(p,False))),
        'two_setting_rank':int(np.linalg.matrix_rank(jacobian(p,True))),
        'ordinary_identity_equivalence':ordinary_identity_equivalence(.9,.8),
        'limitations':[
            'idealized independent photon-number-resolving source-class calibration',
            'one time-gate per trial; threshold detectors with independent dark clicks',
            'only (1,1),(2,0),(0,2),(0,0) input photon-number classes',
            'no dead time, cross-talk, higher photon counts or arbitrary environment memory',
            'no independent historical-photon identity prediction']}
    path=Path('results/mixed_hom_v094_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k in (
        'predicted_near','predicted_far','point_estimate','one_setting_rank',
        'two_setting_rank','naive_lossless_estimate_from_raw_near_coincidence')},indent=2))
    return out
if __name__=='__main__':main()
