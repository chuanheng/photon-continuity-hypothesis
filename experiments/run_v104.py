"""v1.04 GitHub companion: limited exact SBC and complex-model diagnostics.

python -m experiments.run_v104 (from repository root, numpy scipy)
Exact local tested source is in photon_v104_complete.zip, NOT this text.
"""
import json
from pathlib import Path
from models.validation_v104 import exact_submodel_sbc,ppc_audit,proposal_audit

if __name__=="__main__":
    sbc=exact_submodel_sbc(n=450,draws=49,seed=10401)
    ppc=ppc_audit(n=75,seed=10420)
    sensitivity=proposal_audit(n=32,draws=90,seed=10480)
    result={'version':'v1.04','SBC_restricted_optical_submodel':sbc,
      'heldout_PPC_not_SBC':ppc,'hyper_ESS_sensitivity_not_SBC':sensitivity,
      'scientific_caution':'No full v1.03 model SBC; no historical-photon identity claim.'}
    file=Path('results/validation_v104_recomputed.json')
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'sbc_covered':sbc['covered'],'sbc_rank_p':sbc['rank_uniformity_p'],
       'ppc_flags':{name:obj['flagged_p_le_0_05'] for name,obj in ppc.items()},
       'proposal_ESS':sensitivity['summary']},indent=2,ensure_ascii=False))
