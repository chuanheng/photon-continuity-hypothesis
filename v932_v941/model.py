"""Worst success weighting for six published conditional fidelity estimates."""
import json
import numpy as np
from scipy.optimize import linprog
from v922_v931.model import bounds

def run():
    values = np.array([.922,.920,.919,.909,.951,.942])
    solution = linprog(values,A_eq=[np.ones(6)],b_eq=[1.],bounds=(0,1))
    if not solution.success:
        raise RuntimeError(solution.message)
    return dict(equal=float(values.mean()),minimum=float(solution.fun),
                minimizing_weights=solution.x.tolist(),
                margin=solution.fun-bounds(.093)[1],
                low_eff_margin=solution.fun-bounds(.083)[1])

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
