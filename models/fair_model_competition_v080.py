"""v0.80 fair model competition under explicit nuisance calibration assumptions.

NOT a QED model nor evidence that photon historical identity exists.
Parameters theta=(L,A,beta,kappa,delta):
 L effective loss, A interference amplitude, beta common offset,
 kappa ordinary group-dependent drift, delta hypothetical identity-specific shift.
Data have experiment_type {'test','cal'} and switch z in {0,1}.
Test phase=x+beta+z*(kappa+delta); calibration phase=x+beta+z*kappa.
Critical assumption: test and calibration share ordinary drift kappa and beta.
"""
import numpy as np
from scipy.optimize import minimize

PHASES=(.15,.8,1.7,2.5)
TRUE=np.array([.35,.49,.13,.11,.20])
N_PER_CONDITION=1000

def probabilities(params, x, z, kind):
    L,A,beta,kappa,delta=map(float,params)
    if kind not in ('test','cal') or z not in (0,1):
        raise ValueError('unsupported setting')
    if not (0<L<1 and 0<A<1-L):
        raise ValueError('invalid physical effective parameters')
    phase=x+beta+z*(kappa+(delta if kind=='test' else 0))
    c=A*np.cos(phase)
    return np.array([L,(1-L+c)/2,(1-L-c)/2])

def gradient(params,x,z,kind):
    L,A,beta,kappa,delta=map(float,params)
    phase=x+beta+z*(kappa+(delta if kind=='test' else 0))
    c,s=np.cos(phase),np.sin(phase)
    g=np.zeros((3,5))
    g[:,0]=[1,-.5,-.5]
    g[:,1]=[0,c/2,-c/2]
    g[:,2]=[0,-A*s/2,A*s/2]
    g[:,3]=z*g[:,2]
    g[:,4]=z*g[:,2] if kind=='test' else 0
    return g

def settings(include_cal):
    return [(kind,z,x) for kind in (('test','cal') if include_cal else ('test',))
            for z in (0,1) for x in PHASES]

def fisher(params, include_cal=True, n=N_PER_CONDITION):
    out=np.zeros((5,5))
    for kind,z,x in settings(include_cal):
        p=probabilities(params,x,z,kind)
        g=gradient(params,x,z,kind)
        out += n*(g.T/p)@g
    return out

def numerical_rank(matrix,rtol=1e-9):
    e=np.linalg.eigvalsh(matrix)
    return int(np.sum(e>rtol*max(float(np.max(np.abs(e))),1))),e

def kl(p,q):
    p=np.asarray(p,float);q=np.asarray(q,float)
    if not np.allclose(p.sum(),1) or not np.allclose(q.sum(),1) or np.any(p<0) or np.any(q<0):
        raise ValueError('invalid probability vector')
    if np.any((p>0)&(q==0)):return float('inf')
    m=p>0
    return float(np.sum(p[m]*np.log(p[m]/q[m])))

def asimov_deviance(true, candidate, include_cal=True, n=N_PER_CONDITION):
    return float(2*n*sum(kl(probabilities(true,x,z,kind), probabilities(candidate,x,z,kind))
                         for kind,z,x in settings(include_cal)))

def profile_delta_null(true,include_cal=True,n=N_PER_CONDITION):
    """Fit nuisance L,A,beta,kappa under delta=0 with deterministic Asimov data.

    Relative parameter constraints: 0<L<1, 0<A<1-L. Use SLSQP and
    deterministic multiple starts to guard against local optima.
    """
    def objective(p):
        candidate=np.r_[p,0.]
        return asimov_deviance(true,candidate,include_cal,n)
    bounds=[(.001,.999),(.001,.998),(-np.pi,np.pi),(-np.pi,np.pi)]
    constraints=[{'type':'ineq','fun':lambda p:1-p[0]-p[1]-1e-5}]
    starts=[true[:4].copy(),np.array([true[0],true[1],true[2],true[3]+true[4]]),
            np.array([.4,.4,0.,0.])]
    valid=[]
    for p0 in starts:
        res=minimize(objective,p0,method='SLSQP',bounds=bounds,constraints=constraints,
                     options={'ftol':1e-12,'maxiter':1500})
        if res.success or (res.fun>=-1e-8 and np.isfinite(res.fun)):
            valid.append(res)
    if not valid:raise RuntimeError('profile optimization failed')
    res=min(valid,key=lambda a:a.fun)
    return {'deviance':float(res.fun),'nuisance_fit':res.x.tolist(),
            'optimization_success':bool(res.success)}

def schur_delta_info(matrix):
    a=matrix[:4,:4]
    return float(matrix[4,4]-matrix[4,:4]@np.linalg.pinv(a,rcond=1e-12)@matrix[:4,4])

def unconstrained_ordinary_model_equivalence(params):
    """If ordinary test drift is free, delta simply renames that drift.

    Given identity-model (kappa, delta), ordinary model can set
    kappa_test=kappa+delta, kappa_cal=kappa. Both distributions match.
    """
    L,A,beta,kappa,delta=map(float,params)
    baseline=np.array([L,A,beta,kappa,0.])
    shifted=np.array([L,A,beta,kappa+delta,0.])
    return max(float(np.max(np.abs(
        probabilities(params,x,z,kind)-
        probabilities((shifted if kind=='test' else baseline),x,z,kind))))
        for kind,z,x in settings(True))

def summary():
    f0=fisher(TRUE,False);f1=fisher(TRUE,True)
    r0,e0=numerical_rank(f0);r1,e1=numerical_rank(f1)
    prof0=profile_delta_null(TRUE,False)
    prof1=profile_delta_null(TRUE,True)
    return {'version':'v0.80','true_parameters':dict(zip(['loss','amplitude','beta','ordinary_drift','hypothetical_delta'],TRUE.tolist())),
       'n_per_condition':N_PER_CONDITION,'test_only_rank':r0,'joint_rank':r1,
       'test_only_eigenvalues':e0.tolist(),'joint_eigenvalues':e1.tolist(),
       'test_only_conditional_delta_fisher':schur_delta_info(f0),
       'joint_conditional_delta_fisher':schur_delta_info(f1),
       'test_only_null_fit':prof0,'joint_null_fit':prof1,
       'free_ordinary_test_drift_max_error':unconstrained_ordinary_model_equivalence(TRUE),
       'interpretation':'Calibrated delta only identifiable if ordinary drift shared by test and calibration; otherwise ordinary memory remains equivalent. No photon identity proof.'}

if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2,ensure_ascii=False))
