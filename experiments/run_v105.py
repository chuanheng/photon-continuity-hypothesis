"""Regenerate v1.05 synthetic multi-parameter SBC and robust heldout scores.
This is the GitHub companion; complete originally executed code is in ZIP.
"""
import json
from pathlib import Path
from scipy.stats import binomtest
from models.full_sbc_v105 import audit as run_sbc
from models.robust_sensor_v105 import audit as run_sensor

if __name__=='__main__':
    sbc=run_sbc(n=450,particles=850,draws=49,seed=10501)
    sensor=run_sensor(n=180,seed=105500)
    out={'version':'v1.05','synthetic_only':True,
         'formal_joint_prior_SBC':sbc,
         'heldout_robust_sensor_scoring':sensor}
    folder=Path('results');folder.mkdir(exist_ok=True)
    (folder/'full_sbc_v105_recomputed.json').write_text(
        json.dumps(sbc,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    (folder/'robust_sensor_v105_recomputed.json').write_text(
        json.dumps(sensor,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(json.dumps({'M_covered':sbc['Mcovered'],'SBC_rank_p':sbc['rank_tests'],
      'median_particle_ESS':sbc['median_ESS'],
      'sensor_score_differences':{k:v['mean_student_minus_normal']
        for k,v in sensor.items()}},indent=2))
