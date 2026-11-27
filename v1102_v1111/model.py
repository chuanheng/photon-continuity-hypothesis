"""Exact finite pure-loss instrument on a binomial logical qubit."""
import json
from math import comb
import numpy as np

V=np.zeros((5,2));V[[0,4],0]=1/np.sqrt(2);V[2,1]=1
A=np.diag(np.sqrt(np.arange(1,5)),1)
def branch(k,t):
    K=np.zeros((5,5))
    for n in range(k,5):
        K[n-k,n]=np.sqrt(comb(n,k)*t**(n-k)*(1-t)**k)
    return K@V

def run():
    t=.8
    B=[branch(k,t) for k in range(5)]
    masses=np.array([np.diag(b.T@b) for b in B])
    avg=masses.mean(axis=1)
    odd=avg[1]+avg[3]
    # False-odd and missed-odd are separately calibrated.
    false,miss=.02,.08
    pflag=odd*(1-miss)+(1-odd)*false
    # An unknown Kerr jump time contributes relative phase 2 chi tau for n=4 vs 2.
    chi=.7;duration=.8
    return dict(jump_KL=dict(mean=np.diag(V.T@A.T@A@V).tolist(),cross=float(np.linalg.norm(V.T@A@V))),
                finite_single=dict(prob=masses[1].tolist(),ratio=float(np.sqrt(masses[1,0]/masses[1,1]))),
                vacuum_record=dict(prob=masses[0].tolist(),difference=float(np.diff(masses[0])[0])),
                filter=dict(one=float(min(masses[1])),all_number_resolved=float(sum(min(row) for row in masses[:3]))),
                odd_alias=dict(prob=odd,three_fraction=avg[3]/odd),
                wrong_flag=dict(total=pflag,single_fraction=(1-miss)*avg[1]/pflag),
                double_jump=dict(prob=masses[2].tolist(),overlap_with_code=float(np.linalg.norm(V.T@B[2]))),
                emitted_info=dict(count_tv=float(abs(masses[:,0]-masses[:,1]).sum()/2)),
                timing=dict(known_visibility=1.,unknown_visibility=float(np.sinc(chi*duration/np.pi))),
                energy=dict(before=np.diag(V.T@np.diag(np.arange(5))@V).tolist(),after=[3.,1.],
                            required_work=[-1.,1.]))
if __name__=='__main__':print(json.dumps(run(),indent=2))
