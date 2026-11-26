"""Three-time dichotomic records of a two-mode material excitation."""
import json
from itertools import product
import numpy as np
from scipy.optimize import linprog

SIGNS=np.array(list(product([1,-1],repeat=3)))
PAIRS=[(0,1),(1,2),(0,2)]
M=np.array([SIGNS[:,i]*SIGNS[:,j] for i,j in PAIRS])
Z=np.diag([1.,-1.])
def turn(angle):
    c,s=np.cos(angle/2),np.sin(angle/2)
    return np.array([[c,-s],[s,c]])

def pair_table(angle,sharp=1.,offset=0.):
    U=turn(angle)
    effects=[(np.eye(2)+sign*(sharp*Z+offset*np.eye(2)))/2 for sign in (1,-1)]
    out=np.empty((2,2))
    for i,effect in enumerate(effects):
        post=effect/2  # Square-root instrument acting on I/2.
        for j,final in enumerate(effects):out[i,j]=np.trace(final@U@post@U.T)
    return out

def run():
    theta=np.pi/3
    cor=np.array([np.cos(theta),np.cos(theta),np.cos(2*theta)])
    signed=np.array([1,1,-1])
    # Minimum total negative mass of a signed joint distribution.
    mat=np.vstack([np.ones(8),SIGNS.T,M])
    lp=linprog(np.r_[np.zeros(8),np.ones(8)],A_eq=np.c_[mat,-mat],
               b_eq=np.r_[1,np.zeros(3),cor],bounds=(0,None))
    if not lp.success:raise ValueError(lp.message)
    full=pair_table(theta)@(2*pair_table(theta))
    direct=pair_table(2*theta)
    v=np.sqrt(3)-1
    sharp=.8;offset=.07
    read=pair_table(theta,sharp,offset)
    # Three equally likely classical paths up to global sign, each fails one signed constraint.
    legal=SIGNS[(signed@M)==1]
    product_scores=np.array([legal[:,i]*legal[:,j] for i,j in PAIRS])*signed[:,None]
    good=(product_scores==1).mean(axis=1)
    # Select keep_bad so each retained agreement probability equals 3/4.
    target_keep=good*(1-.75)/(.75*(1-good))
    return dict(leggett=dict(correlations=cor.tolist(),K=float(signed@cor),classical_max=float(max(signed@M))),
                insertion=dict(direct=direct.tolist(),with_meter=full.tolist()),
                nsit=dict(single_max=float(max(abs(direct.sum(axis=0)-full.sum(axis=0)))),
                          pair_tv=float(abs(direct-full).sum()/2)),
                signed_mass=float(lp.fun),phase_noise=dict(threshold=v,K=v+.5*v*v),
                unsharp=dict(pair=float((Z.diagonal()@pair_table(theta,.8))@Z.diagonal()),threshold=np.sqrt(2/3)),
                asymmetric=dict(measured=float(Z.diagonal()@read@Z.diagonal()),offset=offset,sharp=sharp),
                selection=dict(acceptance=(good+(1-good)*target_keep).tolist(),keep_unfavorable=target_keep.tolist()),
                classical_meter=[(2*pair_table(k*theta)).tolist() for k in [1,2]],
                invasive_fraction=(signed@cor-1)/2)
if __name__=='__main__':print(json.dumps(run(),indent=2))
