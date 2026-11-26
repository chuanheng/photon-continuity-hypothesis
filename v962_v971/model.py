"""Classical-memory simulation with hidden-basis selection at fixed herald rates."""
import json
import numpy as np
from scipy.optimize import linprog

def receiver(kappa, eta=.093):
    # Rows: classical memory's dephasing axis. Columns: chosen readout basis.
    w=np.full((3,3),3*eta/(kappa+2))
    np.fill_diagonal(w,kappa*w[0,1])
    successes=w.mean(axis=0)
    signed_corr=np.diag(w)/(3*successes)
    return successes,signed_corr

def extremum(kappa):
    # Vertices suffice: each product state's signed-correlation vector has l1<=1.
    # Mass[j,b]=Pr(hidden best axis j)*Pr(accept b | j).
    rows=[]
    for j in range(3):
        for a in range(3):
            for b in range(3):
                if a==b: continue
                row=np.zeros((3,3))
                row[j,a]=1
                row[j,b]=-kappa
                rows.append(row.ravel())
    res=linprog(-np.eye(3).ravel(),A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.tile(np.eye(3),(1,3)),b_eq=np.ones(3))
    if not res.success: raise RuntimeError(res.message)
    return (1-res.fun)/4

def run():
    h,c=receiver(8)
    return dict(basis_rates=h.tolist(),signed_correlations=c.tolist(),apparent_overlap=float((1+c.sum())/4),
                sharp_bounds={str(k):extremum(k) for k in (1,2,4,8,32)},
                ratio_to_fake_093_fidelity=(4*.93-1)/(2*(1-.93)))

if __name__=='__main__': print(json.dumps(run(),indent=2))
