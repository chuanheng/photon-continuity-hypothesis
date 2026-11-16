"""v0.97 GitHub companion run. Recomputes synthetic detector-monitor stress tests.
From repository root: python -m experiments.run_v097
Heavy run: 8 conditions x 60 outer experiments x 79 bootstrap replications.
"""
import json
from pathlib import Path
from models.calibration_stress_v097 import audit_all,SCENARIOS,population_limit

def main(outer=60,B=79):
    data=audit_all(outer=outer,B=B)
    data["conditional_population_limit"]={
        key:population_limit(stress) for key,stress in SCENARIOS.items()}
    dest=Path('results/calibration_stress_v097_recomputed.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    compact={k:{'mean_intrinsic':v['mean_intrinsic'],
      'intrinsic_coverage':v['intrinsic_coverage'],
      'period_coverage':v['period_coverage']}
      for k,v in data['scenarios'].items()}
    print(json.dumps(compact,indent=2,ensure_ascii=False))
    return data
if __name__=='__main__':main()
