"""Run from repo root: python -m experiments.run_v092"""
import json
from pathlib import Path
import numpy as np
from models.wigner_weisskopf_v092 import compact_summary,finite_evolution,spectrum,excited_population
if __name__=='__main__':
    result=compact_summary()
    times=np.linspace(0,8,81)
    finite=finite_evolution(times)
    result['time_scan']=[{'t':float(t),'finite_atom':float(a),'finite_field':float(b),
             'markov_atom':float(excited_population(t))}
             for t,a,b in zip(times,finite['atomic_population'],finite['field_population'])]
    detunings=np.linspace(-5,5,1001)
    result['spectrum_scan']=[{'detuning':float(d),'spectral_density':float(x)}
                            for d,x in zip(detunings,spectrum(detunings))]
    path=Path('results/wigner_weisskopf_v092_recomputed.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('time_scan','spectrum_scan')},
                     indent=2,ensure_ascii=False))
