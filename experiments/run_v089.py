"""Run from repository root: python -m experiments.run_v089"""
import json
from pathlib import Path
from models.process_access_v089 import summary,tomography_signature
if __name__=='__main__':
    data=summary()
    data['fixed_signature_64']=tomography_signature(True).tolist()
    data['fresh_signature_64']=tomography_signature(False).tolist()
    path=Path('results/process_access_v089_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(data,indent=2,ensure_ascii=False))
