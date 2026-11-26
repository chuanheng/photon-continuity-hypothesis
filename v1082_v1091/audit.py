"""Profile all classical joint Pauli laws at calibrated single-gate marginals."""
import json
import numpy as np
from scipy.optimize import linprog
from .model import branches,bell_pt,run as prefix
from v1072_v1081.model import PAULI

def profile(h):
    mask=np.zeros((4,16))
    for i,a in enumerate(PAULI):
        for j,b in enumerate(PAULI):
            if np.allclose(a@b,b@a):
                k=np.argmax([abs(np.trace(p@a@b)) for p in PAULI])
                mask[k,4*i+j]=1
    eq=np.vstack([np.repeat(np.eye(4),4,axis=1),np.tile(np.eye(4),4),mask.sum(axis=0)])
    rhs=np.r_[np.ones(8)/4,h]
    fits=[linprog(-c,A_eq=eq,b_eq=rhs) for c in mask]
    best=max(fits,key=lambda f:-f.fun)
    least=linprog(np.r_[np.zeros(16),1],A_eq=np.c_[eq,np.zeros(9)],b_eq=rhs,
                   A_ub=np.c_[mask,-np.ones(4)],b_ub=np.zeros(4))
    if not all(f.success for f in fits+[least]):raise ValueError('infeasible constraints')
    tables=[best.x,least.x[:16]]
    return dict(pt_range=[float(h/2+best.fun),float(h/2-least.fun)],
                residual=max(float(max(abs(eq@x-rhs))) for x in tables),
                examples=[x.reshape(4,4).tolist() for x in tables])

def run():
    f=branches(shared=.15)
    h=f[0].sum()
    # True plus accepted at 0.88, false plus from minus at 0.14.
    obs=.88*f[0]+.14*f[1]
    # In a pump cycle w is zero or 0.3 with equal probability.
    halves=[branches(shared=w)[0] for w in (0,.3)]
    mixture=np.mean(halves,axis=0)
    # Matched independent joint-error calibration: identity iff the two errors coincide.
    d=f[0,0]
    rng=np.random.default_rng(10871091)
    ket=rng.normal(size=2)+1j*rng.normal(size=2);ket/=np.linalg.norm(ket)
    rho=np.outer(ket,ket.conj())
    mat=np.array([[1,1j],[1j,1]])/np.sqrt(2)
    output=lambda ops,input_:sum(w*p@input_@p.conj().T for w,p in zip(f[0],ops))
    ref=output(PAULI,rho)
    other=mat.conj().T@output([mat@p@mat.conj().T for p in PAULI],mat@rho@mat.conj().T)@mat
    return dict(prior=prefix(),profile=profile(h),
                flag=dict(true_pt=min(bell_pt(f[0])),read_pt=min(bell_pt(obs)),
                          false_plus_threshold=.88*(2*d-h)/f[1].sum()),
                drift=dict(block_min=[float(min(bell_pt(u))) for u in halves],
                           pooled_min=min(bell_pt(mixture)),herald_weight=halves[1].sum()/sum(u.sum() for u in halves)),
                audit_margin=dict(same_error=d,plus=h,slack=d-h/2,
                                  robust_slack=(d-.01)-(h+.01)/2),
                heldout=dict(seed=10871091,max_error=float(np.max(abs(other-ref))),rate=float(ref.trace().real)))
if __name__=='__main__':print(json.dumps(run(),indent=2))
