"""Locally visible flags: evaluate four sector payoffs with the same local devices."""
import json
import numpy as np
from v972_v981.model import B,T
from v982_v991.model import MASKS,single

def sectors(left,right,u,v):
    a,b=(1+T@u)/2,(1+T@v)/2
    return np.array([a@B@b,left@B@b,a@B@right,left@B@right])

def mix(values,e,q):
    return float(np.array([1-2*e+q,e-q,e-q,q])@values)

def run():
    e=.03
    a=np.array([0,0,1,1]);b=1-a
    axis=a@T
    axis=axis/np.linalg.norm(axis)
    values=sectors(a,b,axis,-axis)
    # Single-flag optimal masks and corresponding negative-eigenprojector directions.
    options=[]
    for mask in MASKS:
        vec=mask@T
        if np.linalg.norm(vec)<1e-12:continue
        n=vec/np.linalg.norm(vec)
        if np.isclose(mask@B@((1-T@n)/2),single()):
            options.append(n)
    min_clean=min((1+i@j)/4 for i in options for j in options)
    return dict(independent_enclosure=bound_independent(e),sync=dict(rate=e,bound=-e/2),
                exclusive=dict(single_optimal_axes=len(options),clean_floor_at_saturation=float(min_clean)),
                independent=dict(sectors=values.tolist(),feasible=mix(values,e,e**2),relaxation=-e/2,
                                 gap_to_relaxation=mix(values,e,e**2)+e/2))



def bound_independent(e,rings=96):
    """Inner/outer convex hull bounds for local binary polarization effects.

    The circumscribed polytope contains every unit Bloch vector by support
    function domination. Bob's continuous effect and response are solved exactly.
    """
    theta=np.linspace(0,np.pi,rings+1)[:,None]
    phi=np.arange(2*rings)*np.pi/rings
    directions=np.stack(np.broadcast_arrays(np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)),axis=-1).reshape(-1,3)
    scores=[]
    for radius in [1/np.cos(np.pi/rings),1.]:
        clean=(1+radius*directions@T.T)/2
        clean=np.vstack([np.zeros(4),np.ones(4),clean])
        best=0.
        for mask in MASKS:
            weights=((1-e)*clean+e*mask)@B
            trace=weights.sum(axis=1)
            length=np.linalg.norm(weights@T,axis=1)
            # Bob independently chooses unflagged qubit effect and flagged mask.
            eig_low=(trace-length)/2
            eig_high=(trace+length)/2
            score=(1-e)*(np.minimum(0,eig_low)+np.minimum(0,eig_high))+e*np.minimum(weights,0).sum(axis=1)
            best=min(best,float(min(score)))
        scores.append(best)
    return dict(lower=scores[0],upper=scores[1],rings=rings)

if __name__=='__main__':print(json.dumps(run(),indent=2))
