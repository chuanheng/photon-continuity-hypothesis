"""From GitHub repository root: python -m experiments.run_v082"""
import json
from pathlib import Path
from models.count_hierarchy_v082 import summary
if __name__ == '__main__':
    result=summary(replications=60)
    path=Path('results/count_hierarchy_v082_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='null_bootstrap'},indent=2))
    print({k:v for k,v in result['null_bootstrap'].items() if k!='null_stats'})
